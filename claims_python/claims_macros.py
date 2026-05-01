"""Function equivalents for Claims-side SAS macros.

Why SAS macro names are mentioned here:
- For traceability only (to prove 1:1 mapping during migration).
- Python code does not execute SAS; these are native Python functions.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable

Row = dict[str, Any]
Table = list[Row]


def _copy_rows(rows: Iterable[Row]) -> Table:
    return [dict(r) for r in rows]


# -----------------------------
# Logging/message macros
# -----------------------------

def print_to_log(log_file: str | Path) -> Path:
    """SAS macro equivalent: %PrintToLog."""
    return Path(log_file)


def print_to_screen() -> None:
    """SAS macro equivalent: %PrintToScreen."""
    return None


def print_message(message: str, sink: Callable[[str], None] = print) -> None:
    """SAS macro equivalent: %PrintMessage(message)."""
    banner = "-" * 30
    sink(f"{banner}\n{message}\n{banner}")


# -----------------------------
# Manual claims data changes
# -----------------------------

def _starts_with_pr(v: Any) -> bool:
    return str(v or "").startswith("PR")


def manual_raw_data_change_error_mr(rows_mr: Iterable[Row]) -> Table:
    """SAS macro equivalent: %manual_raw_data_change_error_mr."""
    return [r for r in _copy_rows(rows_mr) if not _starts_with_pr(r.get("permid"))]


def manual_raw_data_change_error_dp(rows_dp: Iterable[Row]) -> Table:
    """SAS macro equivalent: %manual_raw_data_change_error_dp."""
    return [r for r in _copy_rows(rows_dp) if not _starts_with_pr(r.get("permid"))]


def manual_raw_data_change_claim(rows_full: Iterable[Row]) -> Table:
    """SAS macro equivalent: %manual_raw_data_change_claim."""
    out = [r for r in _copy_rows(rows_full) if not _starts_with_pr(r.get("permid"))]
    for row in out:
        if row.get("permid") == "CAC2302F016":
            if "Processing_Underpayment" in row:
                row["Processing_Underpayment"] = 0
            if "Underpayments" in row:
                row["Underpayments"] = 0
    return out


@dataclass(slots=True)
class ManualUpdate:
    column: str
    value: Any
    predicate: Callable[[Row], bool]


def manual_data_change(rows: Iterable[Row], updates: Iterable[ManualUpdate] | None = None) -> Table:
    """SAS macro equivalent: %manual_data_change."""
    out = _copy_rows(rows)
    for upd in updates or []:
        for row in out:
            if upd.predicate(row):
                row[upd.column] = upd.value
    return out


def pop_totals_manual_change(rows: Iterable[Row], pyear: str | int) -> Table:
    """SAS macro equivalent: %pop_totals_manual_change."""
    out = _copy_rows(rows)
    for row in out:
        if row.get("fyear") in (None, ""):
            row["fyear"] = str(pyear)
    return out


def _dedupe(rows: Table, keys: list[str]) -> Table:
    seen: set[tuple[Any, ...]] = set()
    out: Table = []
    for row in rows:
        k = tuple(row.get(c) for c in keys)
        if k in seen:
            continue
        seen.add(k)
        out.append(row)
    return out


def pop_totals_manual_change_nodup(rows: Iterable[Row]) -> Table:
    """SAS macro equivalent: %pop_totals_manual_change_nodup."""
    out = []
    for row in _copy_rows(rows):
        if row.get("cnt_act_sampled") in (None, ""):
            continue
        if row.get("cnt_act_sampled_clm") == 0:
            continue
        out.append(row)
    keys = ["state", "qtr", "type", "stratum", "totclm"]
    return _dedupe(out, keys)


def pop_totals_manual_change_nodup2(rows: Iterable[Row]) -> Table:
    """SAS macro equivalent: %pop_totals_manual_change_nodup2."""
    out = _copy_rows(rows)
    keys = ["state", "type", "qtr", "strata"]
    return _dedupe(out, keys)


def se_rate_data_manual_change(rows: Iterable[Row]) -> Table:
    """SAS macro equivalent: %SE_Rate_data_Manual_change (currently no-op in SAS)."""
    return _copy_rows(rows)


# -----------------------------
# Variable type harmonization
# -----------------------------

def _first_non_null(values: Iterable[Any]) -> Any:
    for v in values:
        if v is not None:
            return v
    return None


def check_var_type(previous_rows: Iterable[Row], current_rows: Iterable[Row]) -> Table:
    """SAS macro equivalent: %checkVarType.

    Aligns current-year values to previous-year inferred Python types for common columns.
    """
    prev = _copy_rows(previous_rows)
    cur = _copy_rows(current_rows)
    if not prev or not cur:
        return cur

    prev_cols = {k.upper(): k for k in prev[0].keys()}
    cur_cols = {k.upper(): k for k in cur[0].keys()}

    for ucol in set(prev_cols).intersection(cur_cols):
        pcol = prev_cols[ucol]
        ccol = cur_cols[ucol]
        exemplar = _first_non_null(row.get(pcol) for row in prev)
        if exemplar is None:
            continue
        target_type = type(exemplar)
        for row in cur:
            val = row.get(ccol)
            if val is None:
                continue
            try:
                row[ccol] = target_type(val)
            except Exception:
                pass
    return cur


# -----------------------------
# Export helpers
# -----------------------------

def export_qc(rows: Iterable[Row], csv_path: str | Path) -> Path:
    """SAS macro equivalent: %export_QC (CSV output in Python scaffold)."""
    out_path = Path(csv_path)
    records = _copy_rows(rows)
    if not records:
        out_path.write_text("")
        return out_path

    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(records[0].keys()))
        writer.writeheader()
        writer.writerows(records)
    return out_path


def export_summary(rows: Iterable[Row], csv_path: str | Path) -> Path:
    """SAS macro equivalent: %export_Summary."""
    return export_qc(rows, csv_path)


def data_clean_exp(named_tables: dict[str, Table], out_dir: str | Path) -> list[Path]:
    """SAS macro equivalent: %DataClean_Exp.

    Writes each table into one CSV file named after the logical sheet.
    """
    output_dir = Path(out_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for name, rows in named_tables.items():
        filename = f"{name.replace(' ', '_')}.csv"
        paths.append(export_qc(rows, output_dir / filename))
    return paths


# -----------------------------
# Remaining mapped macros (to be ported)
# -----------------------------

def loopit_mr(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def loopit_dp(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def imputed_fmap(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def import_mr(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def import_dp(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def import_data(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def format_variables(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def merged_data_clean_up(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def format_for_rolling_stack(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def rate_calculation(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def extract_relevant_pgmtype_data(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def run_rates(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def check(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def get_sample_data(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def sample_data_qc(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def runme(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def qc_sample_data(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def strata_pop_qc(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def qualifier_coding(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def assign_qualifier_label_cleaning(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def assign_qualifier_label2(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def subqualifier_coding(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def assign_subqualifier_label2(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def assign_sqc(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def qualifier_subqual_check_export(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def pop_data_clean(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def manual_lewindata_change(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def double_ratio_estimator(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def combined_ratio_estimator(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def combined_ratio_estimator2(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
def raterun2(*args: Any, **kwargs: Any) -> None: raise NotImplementedError
