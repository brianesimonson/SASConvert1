from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Any

from .converted_structure.claims_programs import manual_change_for_claims_data_cleaning as manual_prog


def read_csv_rows(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def write_csv_rows(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def run_manual_change_program(input_dir: Path, output_dir: Path, pyear: str) -> None:
    """Run converted manual-change claims program.

    Expected input files:
    - MR.csv
    - DP.csv
    - full_data.csv
    - poptotals_temp.csv
    """
    mr = read_csv_rows(input_dir / "MR.csv")
    dp = read_csv_rows(input_dir / "DP.csv")
    full_data = read_csv_rows(input_dir / "full_data.csv")
    pop = read_csv_rows(input_dir / "poptotals_temp.csv")

    mr_out = manual_prog.manual_raw_data_change_error_mr(mr)
    dp_out = manual_prog.manual_raw_data_change_error_dp(dp)
    full_out = manual_prog.manual_raw_data_change_claim(full_data)
    full_out = manual_prog.manual_data_change(full_out)

    pop_out = manual_prog.pop_totals_manual_change(pop, pyear)
    pop_out = manual_prog.pop_totals_manual_change_nodup(pop_out)

    write_csv_rows(output_dir / "MR.cleaned.csv", mr_out)
    write_csv_rows(output_dir / "DP.cleaned.csv", dp_out)
    write_csv_rows(output_dir / "full_data.cleaned.csv", full_out)
    write_csv_rows(output_dir / "poptotals_temp.cleaned.csv", pop_out)



def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run converted Claims Python programs")
    parser.add_argument("--program", choices=["manual-change"], default="manual-change")
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--pyear", default="2026")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    if args.program == "manual-change":
        run_manual_change_program(args.input_dir, args.output_dir, args.pyear)


if __name__ == "__main__":
    main()
