"""Converted manual-change program from SAS.

Source: Claims Programs/Manual Change for Claims Data Cleaning.sas
"""

from __future__ import annotations

from typing import Any

from ... import claims_macros as cm


def manual_raw_data_change_error_mr(rows_mr: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %manual_raw_data_change_error_mr."""
    return cm.manual_raw_data_change_error_mr(rows_mr)


def manual_raw_data_change_error_dp(rows_dp: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %manual_raw_data_change_error_dp."""
    return cm.manual_raw_data_change_error_dp(rows_dp)


def manual_raw_data_change_claim(rows_full: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %manual_raw_data_change_claim."""
    return cm.manual_raw_data_change_claim(rows_full)


def manual_data_change(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %manual_data_change."""
    return cm.manual_data_change(rows)


def pop_totals_manual_change(indata: list[dict[str, Any]], pyear: str | int) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %pop_totals_manual_change."""
    return cm.pop_totals_manual_change(indata, pyear)


def pop_totals_manual_change_nodup(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %pop_totals_manual_change_nodup."""
    return cm.pop_totals_manual_change_nodup(rows)


def pop_totals_manual_change_nodup2(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %pop_totals_manual_change_nodup2."""
    return cm.pop_totals_manual_change_nodup2(rows)


def se_rate_data_manual_change(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Converted entrypoint for SAS macro %SE_Rate_data_Manual_change."""
    return cm.se_rate_data_manual_change(rows)
