from __future__ import annotations

from claims_python.claims_macros import (
    check_var_type,
    manual_raw_data_change_claim,
    manual_raw_data_change_error_dp,
    manual_raw_data_change_error_mr,
    pop_totals_manual_change,
    pop_totals_manual_change_nodup,
    pop_totals_manual_change_nodup2,
)


def test_manual_raw_data_change_filters_pr_records():
    rows = [{"permid": "PR123"}, {"permid": "CA999"}, {"permid": None}]
    out_mr = manual_raw_data_change_error_mr(rows)
    out_dp = manual_raw_data_change_error_dp(rows)
    assert [r["permid"] for r in out_mr] == ["CA999", None]
    assert [r["permid"] for r in out_dp] == ["CA999", None]


def test_manual_raw_data_change_claim_zeroes_specific_claim():
    rows = [
        {"permid": "CAC2302F016", "Processing_Underpayment": 10, "Underpayments": 1},
        {"permid": "CA111", "Processing_Underpayment": 20, "Underpayments": 2},
    ]
    out = manual_raw_data_change_claim(rows)
    row = [r for r in out if r["permid"] == "CAC2302F016"][0]
    assert row["Processing_Underpayment"] == 0
    assert row["Underpayments"] == 0


def test_pop_totals_manual_change_fills_fyear():
    rows = [{"fyear": None}, {"fyear": "2025"}]
    out = pop_totals_manual_change(rows, 2026)
    assert [r["fyear"] for r in out] == ["2026", "2025"]


def test_pop_totals_nodup_variants():
    rows = [
        {
            "state": "CA",
            "qtr": 1,
            "type": "A",
            "stratum": "S1",
            "strata": "S1",
            "totclm": 100,
            "cnt_act_sampled": 1,
            "cnt_act_sampled_clm": 1,
        },
        {
            "state": "CA",
            "qtr": 1,
            "type": "A",
            "stratum": "S1",
            "strata": "S1",
            "totclm": 100,
            "cnt_act_sampled": 1,
            "cnt_act_sampled_clm": 1,
        },
        {
            "state": "NY",
            "qtr": 1,
            "type": "A",
            "stratum": "S2",
            "strata": "S2",
            "totclm": 200,
            "cnt_act_sampled": None,
            "cnt_act_sampled_clm": 1,
        },
    ]
    out1 = pop_totals_manual_change_nodup(rows)
    assert len(out1) == 1
    out2 = pop_totals_manual_change_nodup2(rows)
    assert len(out2) == 2


def test_check_var_type_aligns_common_columns():
    prev = [{"A": 1, "B": "x"}, {"A": 2, "B": "y"}]
    cur = [{"a": "3", "b": 5, "C": 1.1}, {"a": "4", "b": 6, "C": 2.2}]
    out = check_var_type(prev, cur)
    assert isinstance(out[0]["a"], int)
