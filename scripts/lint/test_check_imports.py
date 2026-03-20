"""
Test suite for check_imports.py
Tests the key rules, including the ARCH-05 bug (UI importing Runtime).
"""
import sys
from pathlib import Path

# Add scripts/lint to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts" / "lint"))
from check_imports import lint_file, LintResult, get_layer, get_imported_layer


def make_file(tmp_path: Path, rel: str, content: str) -> Path:
    p = tmp_path / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)
    return p


# ── get_layer detection ───────────────────────────────────────────────────────

def test_get_layer_domains_structure(tmp_path):
    f = make_file(tmp_path, "domains/billing/service/payment.py", "")
    assert get_layer(f, tmp_path) == "service"

def test_get_layer_src_structure(tmp_path):
    f = make_file(tmp_path, "src/ui/components/button.tsx", "")
    assert get_layer(f, tmp_path) == "ui"

def test_get_layer_runtime(tmp_path):
    f = make_file(tmp_path, "domains/orders/runtime/digest_job.py", "")
    assert get_layer(f, tmp_path) == "runtime"

def test_get_layer_unrecognised(tmp_path):
    f = make_file(tmp_path, "utils/helpers.py", "")
    assert get_layer(f, tmp_path) is None  # 'utils' is not a layer

# ── get_imported_layer detection ──────────────────────────────────────────────

def test_imported_layer_python_dotted():
    assert get_imported_layer("domains.billing.repo.invoice_repo") == "repo"

def test_imported_layer_ts_relative():
    assert get_imported_layer("../../billing/ui/components") == "ui"

def test_imported_layer_ts_alias():
    assert get_imported_layer("@/domains/orders/runtime/jobs") == "runtime"

def test_imported_layer_external():
    assert get_imported_layer("fastapi") is None
    assert get_imported_layer("react") is None
    assert get_imported_layer("zod") is None

# ── ARCH-01: layer direction ──────────────────────────────────────────────────

def test_arch01_service_imports_ui(tmp_path):
    f = make_file(tmp_path, "domains/billing/service/svc.py",
                  "from domains.billing.ui.components import Button\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    rules = [v.rule for v in result.violations]
    assert "ARCH-01" in rules

def test_arch01_repo_imports_service(tmp_path):
    f = make_file(tmp_path, "domains/billing/repo/invoice.py",
                  "from domains.billing.service.payment import PaymentService\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    assert any(v.rule == "ARCH-01" for v in result.violations)

def test_arch01_service_imports_repo_is_allowed(tmp_path):
    f = make_file(tmp_path, "domains/billing/service/svc.py",
                  "from domains.billing.repo.invoice import InvoiceRepo\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    assert not any(v.rule == "ARCH-01" for v in result.violations)

# ── ARCH-05 (THE BUG): UI must not import Runtime ────────────────────────────

def test_arch05_ui_imports_runtime_is_caught(tmp_path):
    """This was the bug: ARCH-01 does NOT catch ui→runtime because ui(5) > runtime(4)
    is false. ARCH-05 must catch it explicitly."""
    f = make_file(tmp_path, "domains/orders/ui/page.tsx",
                  "import { SendDigestJob } from '../../runtime/digest_job'\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    rules = [v.rule for v in result.violations]
    assert "ARCH-05" in rules, f"Expected ARCH-05. Got rules: {rules}"
    # Also confirm ARCH-01 did NOT catch it (to document the gap it fills)
    assert "ARCH-01" not in rules, "ARCH-01 should NOT have caught ui→runtime"

def test_arch05_runtime_imports_ui_is_caught_by_arch01_and_arch04(tmp_path):
    """Confirm the reverse direction (runtime→ui) is caught by ARCH-01 and ARCH-04."""
    f = make_file(tmp_path, "domains/orders/runtime/job.py",
                  "from domains.orders.ui.components import Button\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    rules = [v.rule for v in result.violations]
    assert "ARCH-04" in rules
    assert "ARCH-01" in rules

# ── ARCH-03: Service must not import Runtime ──────────────────────────────────

def test_arch03_service_imports_runtime(tmp_path):
    f = make_file(tmp_path, "domains/orders/service/svc.py",
                  "from domains.orders.runtime.digest_job import DigestJob\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    assert any(v.rule == "ARCH-03" for v in result.violations)

# ── TypeScript import extraction ──────────────────────────────────────────────

def test_ts_import_relative_path(tmp_path):
    f = make_file(tmp_path, "domains/billing/ui/page.tsx",
                  "import { runJob } from '../../runtime/jobs'\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    assert any(v.rule == "ARCH-05" for v in result.violations)

def test_ts_import_external_library_ignored(tmp_path):
    f = make_file(tmp_path, "domains/billing/ui/page.tsx",
                  "import React from 'react'\nimport { z } from 'zod'\n")
    result = LintResult()
    lint_file(f, tmp_path, result)
    assert result.passed


if __name__ == "__main__":
    import pytest, sys
    sys.exit(pytest.main([__file__, "-v"]))
