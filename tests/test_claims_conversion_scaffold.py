from __future__ import annotations

import importlib
import re
from pathlib import Path

from claims_python.master_claims import ClaimsRunConfig, validate_claims_sources
from claims_python.precision import configure_decimal
from decimal import getcontext, ROUND_HALF_EVEN


ROOT = Path(__file__).resolve().parents[1]


def sas_macros_in_scope() -> set[str]:
    sas_dirs = [ROOT / "Claims Programs", ROOT / "Global Macros", ROOT / "Reconcile Macro"]
    pattern = re.compile(r"%macro\s+([A-Za-z0-9_]+)", re.IGNORECASE)
    names: set[str] = set()
    for folder in sas_dirs:
        for path in folder.glob("*.sas"):
            text = path.read_text(errors="ignore")
            names.update(m.group(1).lower() for m in pattern.finditer(text))
    return names


def python_macro_functions() -> set[str]:
    module = importlib.import_module("claims_python.claims_macros")
    names = {
        name.lower()
        for name, value in vars(module).items()
        if callable(value) and not name.startswith("_")
    }
    return names


def test_precision_policy():
    configure_decimal(28)
    ctx = getcontext()
    assert ctx.prec == 28
    assert ctx.rounding == ROUND_HALF_EVEN


def test_claims_sources_exist():
    validate_claims_sources(ROOT)


def test_every_sas_macro_has_python_equivalent_name():
    sas_names = sas_macros_in_scope() - {"mainpath"}
    py_names = python_macro_functions()

    # Name adjustments where Python uses snake_case.
    aliases = {
        "imputedfmap": "imputed_fmap",
        "mergeddatacleanup": "merged_data_clean_up",
        "se_rate_data_manual_change": "se_rate_data_manual_change",
        "sampledata_qc": "sample_data_qc",
        "strata_popqc": "strata_pop_qc",
        "assign_sqc": "assign_sqc",
        "printtolog": "print_to_log",
        "printmessage": "print_message",
        "printtoscreen": "print_to_screen",
        "popdataclean": "pop_data_clean",
        "checkvartype": "check_var_type",
        "export_qc": "export_qc",
        "export_summary": "export_summary",
        "dataclean_exp": "data_clean_exp",
        "getsampledata": "get_sample_data",
        "ratecalculation": "rate_calculation",
    }

    missing = []
    for sas_name in sas_names:
        target = aliases.get(sas_name, sas_name)
        if target not in py_names:
            missing.append((sas_name, target))

    assert not missing, f"Missing python functions for SAS macros: {missing}"


def test_claims_run_config_smoke():
    cfg = ClaimsRunConfig(repo_root=ROOT)
    assert cfg.precision == 28
