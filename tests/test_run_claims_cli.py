from __future__ import annotations

import csv
from pathlib import Path

from claims_python.run_claims import run_manual_change_program


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        return [dict(r) for r in csv.DictReader(f)]


def test_run_manual_change_program(tmp_path: Path):
    in_dir = tmp_path / "in"
    out_dir = tmp_path / "out"

    write_rows(in_dir / "MR.csv", [{"permid": "PRX"}, {"permid": "CA1"}])
    write_rows(in_dir / "DP.csv", [{"permid": "PRY"}, {"permid": "CA2"}])
    write_rows(
        in_dir / "full_data.csv",
        [
            {"permid": "CAC2302F016", "Processing_Underpayment": "5", "Underpayments": "2"},
            {"permid": "CA3", "Processing_Underpayment": "9", "Underpayments": "4"},
        ],
    )
    write_rows(
        in_dir / "poptotals_temp.csv",
        [
            {"state": "CA", "qtr": "1", "type": "M", "stratum": "A", "totclm": "100", "cnt_act_sampled": "1", "cnt_act_sampled_clm": "1", "fyear": ""},
            {"state": "CA", "qtr": "1", "type": "M", "stratum": "A", "totclm": "100", "cnt_act_sampled": "1", "cnt_act_sampled_clm": "1", "fyear": ""},
        ],
    )

    run_manual_change_program(in_dir, out_dir, "2026")

    mr = read_rows(out_dir / "MR.cleaned.csv")
    dp = read_rows(out_dir / "DP.cleaned.csv")
    full = read_rows(out_dir / "full_data.cleaned.csv")
    pop = read_rows(out_dir / "poptotals_temp.cleaned.csv")

    assert [r["permid"] for r in mr] == ["CA1"]
    assert [r["permid"] for r in dp] == ["CA2"]
    assert full[0]["Processing_Underpayment"] == "0"
    assert full[0]["Underpayments"] == "0"
    assert len(pop) == 1
    assert pop[0]["fyear"] == "2026"
