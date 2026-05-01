from __future__ import annotations

import importlib
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_generated_module_count_matches_sas_files():
    sas_files = [
        *list((ROOT / "Claims Programs").glob("*.sas")),
        *list((ROOT / "Global Macros").glob("*.sas")),
        *list((ROOT / "Reconcile Macro").glob("*.sas")),
        *list((ROOT / "Master Program").glob("*.sas")),
    ]
    py_modules = [p for p in (ROOT / "claims_python" / "converted_structure").rglob("*.py") if p.name != "__init__.py"]
    assert len(py_modules) == len(sas_files)


def test_generated_modules_are_importable():
    import claims_python.converted_structure as cs

    assert cs is not None
    # Smoke import representative modules
    importlib.import_module("claims_python.converted_structure.claims_programs.step_1_reconcile_and_import_data")
    importlib.import_module("claims_python.converted_structure.global_macros.double_ratio_estimator")


def test_macro_entrypoints_generated():
    path = ROOT / "claims_python" / "converted_structure" / "claims_programs" / "manual_change_for_claims_data_cleaning.py"
    text = path.read_text()
    assert "def manual_raw_data_change_error_mr" in text
    assert "def se_rate_data_manual_change" in text

    # ensure includes are captured when present
    master_path = ROOT / "claims_python" / "converted_structure" / "master_program" / "master_program_forecasting_rates.py"
    mtext = master_path.read_text()
    assert re.search(r"INCLUDES\s*=\s*\[", mtext)
