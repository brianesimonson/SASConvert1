from __future__ import annotations

import csv
import json
from pathlib import Path

from claims_python.master_claims import run_master_claims


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_run_master_claims_writes_summary(tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"

    write_rows(in_dir / "MR.csv", [{"permid": "CA1"}])
    write_rows(in_dir / "DP.csv", [{"permid": "CA2"}])
    write_rows(in_dir / "full_data.csv", [{"permid": "CA3", "Processing_Underpayment": "1", "Underpayments": "1"}])
    write_rows(
        in_dir / "poptotals_temp.csv",
        [{"state": "CA", "qtr": "1", "type": "M", "stratum": "A", "totclm": "100", "cnt_act_sampled": "1", "cnt_act_sampled_clm": "1", "fyear": ""}],
    )

    summary = run_master_claims(repo_root=Path('.'), input_dir=in_dir, output_dir=out_dir, pyear='2026', precision=28)

    assert summary.exists()
    payload = json.loads(summary.read_text(encoding='utf-8'))
    assert payload["master_equivalent"] == "Claims-only"
    assert payload["native_executed"] == ["Claims Programs/Manual Change for Claims Data Cleaning.sas"]
    assert len(payload["transpiled_captured"]) == 2
