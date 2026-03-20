#!/usr/bin/env python3
"""
scripts/lint/check_imports.py

Structural import linter — enforces the layered domain architecture defined in ARCHITECTURE.md.

Dependency rules (within any domain, dependencies may only flow FORWARD):
  Types → Config → Repo → Service → Runtime → UI

Folder names are project-specific. Map your actual folder names to canonical layer names
in .harness.json at the project root. See ARCHITECTURE.md § Adapting to Your Project.

Usage:
  python scripts/lint/check_imports.py [--root ./] [--verbose]

Supported file types:
  Python (.py):               full AST-based import analysis
  TypeScript/JS (.ts, .tsx, .js, .jsx): regex-based import analysis

Exit codes:
  0 — all checks pass
  1 — violations found (details printed to stdout)

Known limitations:
  - Layer detection is path-based: files must live under a mapped layer directory.
    Files not under a recognised layer folder are silently skipped.
  - TypeScript path aliases (e.g. @app/...) are resolved only if the alias contains
    a word that maps to a layer name.
"""

import ast
import re
import sys
import json
import argparse
from pathlib import Path
from dataclasses import dataclass, field

# ─────────────────────────────────────────────────────────────────────────────
# Canonical layer names and their ordering.
# Higher index = further downstream. ARCH-01: may only import from lower-index layers.
CANONICAL_LAYERS: dict[str, int] = {
    "types":   0,
    "config":  1,
    "repo":    2,
    "service": 3,
    "runtime": 4,
    "ui":      5,
}

# Runtime and UI are sibling entry points — neither may import the other.
# ARCH-01 catches runtime→ui but NOT ui→runtime (see ARCH-05).
SIBLING_ENTRY_POINTS = {"runtime", "ui"}

# UI is forbidden from directly importing these canonical layers
UI_FORBIDDEN_IMPORTS = {"infra", "repo"}

CONFIG_FILE = ".harness.json"


# ─────────────────────────────────────────────────────────────────────────────
def load_config(root: Path) -> dict[str, int]:
    """
    Load .harness.json from the project root and merge custom folder name → layer
    mappings into the canonical layer order map.

    Returns a name→index mapping that includes both canonical names and all
    project-specific aliases defined in layer_mappings.

    Example .harness.json:
      {
        "layer_mappings": {
          "workers":      "runtime",
          "consumers":    "runtime",
          "jobs":         "runtime",
          "controllers":  "ui",
          "routes":       "ui",
          "api":          "ui",
          "handlers":     "ui",
          "repositories": "repo",
          "dal":          "repo",
          "models":       "types",
          "schemas":      "types",
          "core":         "service",
          "domain":       "service"
        }
      }
    """
    layer_map = dict(CANONICAL_LAYERS)  # start with canonical names

    config_path = root / CONFIG_FILE
    if not config_path.exists():
        return layer_map

    try:
        config = json.loads(config_path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"⚠️  Warning: could not parse {CONFIG_FILE}: {e}")
        return layer_map

    mappings: dict = config.get("layer_mappings", {})
    unknown_canonical = []

    for alias, canonical in mappings.items():
        if canonical not in CANONICAL_LAYERS:
            unknown_canonical.append(f"  '{alias}' → '{canonical}' (unknown canonical layer)")
            continue
        layer_map[alias.lower()] = CANONICAL_LAYERS[canonical]

    if unknown_canonical:
        print(f"⚠️  Warning: {CONFIG_FILE} contains unknown canonical layer names:")
        for msg in unknown_canonical:
            print(msg)
        print(f"   Valid canonical names: {list(CANONICAL_LAYERS.keys())}\n")

    return layer_map


# ─────────────────────────────────────────────────────────────────────────────
@dataclass
class Violation:
    file: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"  [{self.rule}] {self.file}:{self.line}\n    → {self.message}"


@dataclass
class LintResult:
    violations: list[Violation] = field(default_factory=list)

    def add(self, file: str, line: int, rule: str, message: str) -> None:
        self.violations.append(Violation(file=file, line=line, rule=rule, message=message))

    @property
    def passed(self) -> bool:
        return len(self.violations) == 0


# ─────────────────────────────────────────────────────────────────────────────
def get_layer(path: Path, root: Path, layer_map: dict[str, int]) -> str | None:
    """
    Infer which canonical layer a file belongs to based on its directory path.
    Returns the canonical layer name (e.g. 'runtime'), or None if unrecognised.

    Supported structures:
      <root>/domains/<domain>/<layer-folder>/...   (multi-domain monorepo)
      <root>/src/<layer-folder>/...                 (flat single-domain)
      <root>/<layer-folder>/...                     (flat fallback)

    <layer-folder> can be any name registered in layer_map (canonical or alias).
    """
    try:
        rel = path.relative_to(root)
    except ValueError:
        return None

    parts = rel.parts

    def resolve(name: str) -> str | None:
        """Return canonical layer name for folder name, or None."""
        n = name.lower()
        if n not in layer_map:
            return None
        # Reverse lookup: find canonical name for this index
        idx = layer_map[n]
        for canon, canon_idx in CANONICAL_LAYERS.items():
            if canon_idx == idx:
                return canon
        return None

    # domains/<domain>/<layer>/...
    if len(parts) >= 3 and parts[0] == "domains":
        return resolve(parts[2])

    # src/<layer>/...
    if len(parts) >= 2 and parts[0] == "src":
        return resolve(parts[1])

    # flat: <layer>/...
    if len(parts) >= 1:
        return resolve(parts[0])

    return None


def get_imported_layer(import_path: str, layer_map: dict[str, int]) -> str | None:
    """
    Infer the canonical layer from an import string by scanning for any registered
    layer name (canonical or alias) in the path segments.

    Works for:
      Python dotted modules:  'domains.billing.repo.invoice'  → 'repo'
      Python alias:           'domains.billing.dal.invoice'   → 'repo'  (if dal→repo configured)
      TS/JS relative paths:   '../../billing/workers/job'     → 'runtime' (if workers→runtime)
      TS path aliases:        '@/domains/orders/api/routes'   → 'ui'    (if api→ui)
    """
    # Normalise: replace path separators, dots, dashes with spaces, lowercase
    normalised = re.sub(r"[/.\-@]", " ", import_path).lower()
    parts = normalised.split()

    for part in parts:
        if part in layer_map:
            idx = layer_map[part]
            # Return canonical name
            for canon, canon_idx in CANONICAL_LAYERS.items():
                if canon_idx == idx:
                    return canon
    return None


# ─────────────────────────────────────────────────────────────────────────────
def extract_imports_python(source: str) -> list[tuple[int, str]]:
    """Extract (lineno, module_name) from Python source using AST."""
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                result.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                result.append((node.lineno, node.module))
    return result


# Matches ES module import/export statements
_TS_IMPORT_RE = re.compile(
    r"""(?:import|export)\s+(?:[^'"]*from\s+)?['"]((?:[^'"\\]|\\.)+)['"]"""
    r"""|import\(\s*['"]((?:[^'"\\]|\\.)+)['"]\s*\)""",
    re.MULTILINE,
)


def extract_imports_ts(source: str) -> list[tuple[int, str]]:
    """Extract (approx_lineno, path) from TypeScript/JavaScript source via regex."""
    result = []
    line_offsets: list[int] = []
    offset = 0
    for line in source.splitlines():
        line_offsets.append(offset)
        offset += len(line) + 1

    for match in _TS_IMPORT_RE.finditer(source):
        path = match.group(1) or match.group(2)
        if path:
            lineno = next((i + 1 for i, o in enumerate(line_offsets) if o <= match.start()), 1)
            result.append((lineno, path))
    return result


def extract_imports(path: Path, source: str) -> list[tuple[int, str]]:
    ext = path.suffix.lower()
    if ext == ".py":
        return extract_imports_python(source)
    if ext in {".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs"}:
        return extract_imports_ts(source)
    return []


# ─────────────────────────────────────────────────────────────────────────────
def lint_file(
    path: Path,
    root: Path,
    result: LintResult,
    layer_map: dict[str, int],
    verbose: bool = False,
) -> None:
    source_layer = get_layer(path, root, layer_map)
    if source_layer is None:
        return  # Not in a recognised layer — skip

    source_code = path.read_text(encoding="utf-8", errors="replace")
    imports = extract_imports(path, source_code)

    for lineno, module in imports:
        target_layer = get_imported_layer(module, layer_map)
        if target_layer is None or target_layer == source_layer:
            continue

        src_idx = CANONICAL_LAYERS[source_layer]
        tgt_idx = CANONICAL_LAYERS[target_layer]

        # ── ARCH-01: Layer dependency direction ──────────────────────────────
        if tgt_idx > src_idx:
            result.add(
                file=str(path.relative_to(root)),
                line=lineno,
                rule="ARCH-01",
                message=(
                    f"`{source_layer}` imports from `{target_layer}` — forbidden. "
                    f"Dependencies must flow forward: Types → Config → Repo → Service → Runtime / UI. "
                    f"Importing: '{module}'. "
                    f"Fix: inject via a Provider or Service interface instead."
                ),
            )

        # ── ARCH-02: UI must not directly import repo/infra ──────────────────
        if source_layer == "ui" and target_layer in UI_FORBIDDEN_IMPORTS:
            result.add(
                file=str(path.relative_to(root)),
                line=lineno,
                rule="ARCH-02",
                message=(
                    f"UI imports directly from `{target_layer}` — forbidden. "
                    f"UI must access data only through Service (via DI/hooks) and Types. "
                    f"Importing: '{module}'."
                ),
            )

        # ── ARCH-03: Service must not import UI or Runtime ───────────────────
        if source_layer == "service" and target_layer in {"ui", "runtime"}:
            result.add(
                file=str(path.relative_to(root)),
                line=lineno,
                rule="ARCH-03",
                message=(
                    f"Service imports from `{target_layer}` — forbidden. "
                    f"Service must be agnostic of all entry-point layers (UI and Runtime). "
                    f"Importing: '{module}'."
                ),
            )

        # ── ARCH-04: Runtime must not import UI ──────────────────────────────
        if source_layer == "runtime" and target_layer == "ui":
            result.add(
                file=str(path.relative_to(root)),
                line=lineno,
                rule="ARCH-04",
                message=(
                    f"Runtime imports from `ui` — forbidden. "
                    f"Background jobs must not depend on UI components. "
                    f"Importing: '{module}'."
                ),
            )

        # ── ARCH-05: UI must not import Runtime ──────────────────────────────
        # NOTE: ARCH-01 does NOT catch this — runtime(4) > ui(5) is false.
        # Runtime and UI are sibling entry points; this rule is required explicitly.
        if source_layer == "ui" and target_layer == "runtime":
            result.add(
                file=str(path.relative_to(root)),
                line=lineno,
                rule="ARCH-05",
                message=(
                    f"UI imports from `runtime` — forbidden. "
                    f"Runtime and UI are sibling entry points; neither may import the other. "
                    f"Expose job status through a Service method instead. "
                    f"Importing: '{module}'."
                ),
            )

    if verbose and imports:
        print(f"  checked: {path.relative_to(root)} (layer={source_layer}, imports={len(imports)})")


def lint_file_size(path: Path, root: Path, result: LintResult, max_lines: int = 400) -> None:
    """SIZE-01: No source file exceeds max_lines."""
    line_count = path.read_text(encoding="utf-8", errors="replace").count("\n")
    if line_count > max_lines:
        result.add(
            file=str(path.relative_to(root)),
            line=max_lines,
            rule="SIZE-01",
            message=(
                f"File has {line_count} lines — exceeds the {max_lines}-line limit. "
                f"Split into smaller modules. Large files reduce agent coherence. "
                f"See GOLDEN_PRINCIPLES.md § File Size Limits."
            ),
        )


# ─────────────────────────────────────────────────────────────────────────────
def collect_source_files(root: Path, extensions: list[str]) -> list[Path]:
    files = []
    for ext in extensions:
        files.extend(root.rglob(f"*.{ext}"))
    excluded = {"node_modules", ".venv", "venv", "__pycache__", ".git", "dist", "build", ".next"}
    return [f for f in files if not any(part in excluded for part in f.parts)]


def main() -> None:
    parser = argparse.ArgumentParser(description="Structural import linter for layered domain architecture.")
    parser.add_argument("--root", default=".", help="Project root (default: .)")
    parser.add_argument("--ext", nargs="+", default=["py", "ts", "tsx", "js", "jsx"],
                        help="File extensions to check")
    parser.add_argument("--max-lines", type=int, default=400, help="Max lines per file (default: 400)")
    parser.add_argument("--verbose", action="store_true", help="Print each checked file")
    parser.add_argument("--skip-size", action="store_true", help="Skip the file size check")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    layer_map = load_config(root)

    config_path = root / CONFIG_FILE
    if config_path.exists():
        aliases = {k: v for k, v in layer_map.items() if k not in CANONICAL_LAYERS}
        print(f"📋 Loaded {CONFIG_FILE} — {len(aliases)} custom folder alias(es) registered.\n")
    else:
        print(f"ℹ️  No {CONFIG_FILE} found — using canonical layer names only.\n"
              f"   To map custom folder names (e.g. 'workers' → 'runtime'), create {CONFIG_FILE}.\n"
              f"   See ARCHITECTURE.md § Adapting to Your Project.\n")

    result = LintResult()
    print(f"🔍 Scanning {root} for architectural violations...\n")

    files = collect_source_files(root, args.ext)
    print(f"   Found {len(files)} source files.\n")

    for path in sorted(files):
        lint_file(path, root, result, layer_map, verbose=args.verbose)
        if not args.skip_size:
            lint_file_size(path, root, result, max_lines=args.max_lines)

    print()
    if result.passed:
        print("✅ All architectural checks passed.\n")
        sys.exit(0)
    else:
        print(f"❌ {len(result.violations)} violation(s) found:\n")
        for v in result.violations:
            print(v)
            print()
        print(
            "Fix these before opening a PR.\n"
            "See ARCHITECTURE.md for rules and GOLDEN_PRINCIPLES.md for remediation.\n"
        )
        sys.exit(1)


if __name__ == "__main__":
    main()
