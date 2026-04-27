from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .precision import configure_decimal


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
    """Entry point for Claims conversion execution.

    This intentionally excludes Eligibility because corresponding SAS programs
    are not available in the repository snapshot.
    """

    configure_decimal(config.precision)
    validate_claims_sources(config.repo_root)

    # TODO: Wire in concrete function implementations from claims_macros.py
    # as conversion of each SAS macro is completed.
