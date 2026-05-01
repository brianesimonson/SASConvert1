from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

from .precision import configure_decimal
from .run_claims import run_manual_change_program
from .converted_structure.claims_programs import (
    step_1_reconcile_and_import_data,
    step_2_calculate_claims_error_rate_se_by_state,
)


@dataclass(slots=True)
class ClaimsRunConfig:
    """Runtime configuration for the Claims-only pipeline."""

    repo_root: Path
    precision: int = 28


CLAIMS_REQUIRED_SAS = [
    Path("Claims Programs/Step 1 - Reconcile and Import Data.sas"),
    Path("Claims Programs/Step 2 - Calculate claims error rate SE by state.sas"),
    Path("Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas"),
    Path("Global Macros/include macros.sas"),
]


class MissingSourceError(FileNotFoundError):
    """Raised when required SAS source files are absent."""


def validate_claims_sources(repo_root: Path) -> None:
    missing = [p for p in CLAIMS_REQUIRED_SAS if not (repo_root / p).exists()]
    if missing:
        joined = "\n".join(str(p) for p in missing)
        raise MissingSourceError(f"Missing required Claims SAS files:\n{joined}")


def run_claims_pipeline(config: ClaimsRunConfig) -> None:
    """Claims pipeline initializer (precision + source checks)."""
    configure_decimal(config.precision)
    validate_claims_sources(config.repo_root)


def run_master_claims(
    repo_root: Path,
    input_dir: Path,
    output_dir: Path,
    pyear: str = "2026",
    precision: int = 28,
) -> Path:
    """Closest Python equivalent to SAS Claims master flow.

    Current executable pieces:
    - Manual Change program (native Python implementation)

    Current transpiled/non-native pieces:
    - Step 1 Reconcile and Import Data
    - Step 2 Calculate claims error rate/SE by state

    Returns path to the generated run summary JSON.
    """
    run_claims_pipeline(ClaimsRunConfig(repo_root=repo_root, precision=precision))

    output_dir.mkdir(parents=True, exist_ok=True)

    # Executable native flow
    run_manual_change_program(input_dir=input_dir, output_dir=output_dir, pyear=pyear)

    # Transpiled structural flow capture (for traceability/logging)
    step1_call = step_1_reconcile_and_import_data.getsampledata(type="")
    step2_call = step_2_calculate_claims_error_rate_se_by_state.ratecalculation(type="")

    summary = {
        "master_equivalent": "Claims-only",
        "native_executed": [
            "Claims Programs/Manual Change for Claims Data Cleaning.sas",
        ],
        "transpiled_captured": [
            {
                "source_file": step1_call.source_file,
                "macro_name": step1_call.macro_name,
            },
            {
                "source_file": step2_call.source_file,
                "macro_name": step2_call.macro_name,
            },
        ],
        "inputs": str(input_dir),
        "outputs": str(output_dir),
        "pyear": pyear,
        "precision": precision,
    }

    summary_path = output_dir / "master_claims_run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run Claims master-equivalent pipeline")
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pyear", default="2026")
    parser.add_argument("--precision", type=int, default=28)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    run_master_claims(
        repo_root=args.repo_root,
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        pyear=args.pyear,
        precision=args.precision,
    )


if __name__ == "__main__":
    main()
