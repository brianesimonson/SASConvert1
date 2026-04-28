"""Auto-generated SAS->Python structural conversion module.

Source: Master Program/Master Program Forecasting Rates.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

INCLUDES = [
    "/sas_data_cms/Project/PERM/Statistical Reporting/&masteryear./Master Program/Parameter List.sas",
    "&masterpath./Claims Error Rates/Programs/Step 1 - Reconcile and Import Data.sas",
    "&masterpath./Claims Error Rates/Programs/Step 2 - Calculate claims error rate SE by state.sas",
    "&masterpath./Claims Error Rates/Programs/Step 3 - Data Completeness Check.sas",
    "&masterpath./Eligibility Error Rates/Programs/Step 1 - Reconcile and Import Data.sas",
    "&masterpath./Eligibility Error Rates/Programs/Step 2 - Calculate Eligibility Error Rate SE by state.sas",
    "&masterpath./Eligibility Error Rates/Programs/Step 3 - Create State Level Dataset wo Unwinding.sas",
    "&masterpath./Rolling Rates/Programs/01 Three Year Rolling Dataset with Sweight2--New Rolling.sas",
    "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas",
    "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas",
    "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas",
    "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas",
    "&masterpath./Rolling Rates/Programs/07 Calculate 17 State Cycle Error Rate.sas",
    "&masterpath./Rolling Rates/Programs/08 Three Year Rolling Dataset with Sweight2--New Rolling - No Unwinding.sas",
    "&masterpath./Rolling Rates/Programs/09 Calculating Rolling Rates--NEW method - No Unwinding.sas",
    "&masterpath./Rolling Rates/Programs/09 Calculating Rolling Rates--NEW method - No Unwinding.sas",
    "&masterpath./Rolling Rates/Programs/10 Calculate 17 State Cycle Error Rate - No Unwinding.sas",
    "&masterpath./Overall Error Rates/Programs/Step 01 PERM Overall Error Rate and SE Calculator.sas",
    "&masterpath./Overall Error Rates/Programs/Step 01 PERM Overall Error Rate and SE Calculator.sas",
    "&masterpath./Overall Error Rates/Programs/Step 02 Sample Size Run.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/01 Estimate Rolling Rates.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/02 Estimate Cycle Rates.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/03 Export Rolling and Cycle Forecast Rates.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/04 DP and MR Error Summary.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/04.1 Subqualifier Summary.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/05 Cycle and Rolling Qualifier List.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/06 Small Key Tables.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/07 Cycle Forecast Trends.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/07.3 ELG Forecast Trends.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/07.1 Cycle Overall Forecast Trends.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/07.2 Rolling Overall Forecast Trends.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/08 Claims Reviewed Progress.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/09 Top 100 MR1 and MR2 Errors.sas",
    "&masterpath./Interim Error Rates Forecasting/Programs/10 Weight Test for Accuracy Reviews v2.sas",
    "&masterpath./Overall Error Rates/Programs/ELG Key Tables/Key Tables ELG Master Program.sas",
    "&masterpath./Overall Error Rates/Programs/CLM Key Tables/Key Tables CLM Master Program.sas",
    "&masterpath./Overall Error Rates/Programs/Key Tables/00 Key Tables Master Program - New.sas",
    "&masterpath./Overall Error Rates/Programs/Key Tables Comparison/PERM Qualifier Cycle Compare.sas",
    "&masterpath./Overall Error Rates/Programs/Key Tables - No Unwinding/00 Key Tables Master Program - New.sas",
    "&masterpath./Overall Error Rates/Programs/ELG Key Tables - No Unwinding/Key Tables ELG Master Program.sas",
    "&masterpath./Master Program/Automated Forecasting Rates Backup V2.sas",
]

def macro_var(var: Any = None, value: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %macro_var."""
    _arguments = {
        "var": var,
        "value": value,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%global &var;
%let &var=&value;
/*%syslput &var=&value;*/"""
    return run_transpiled_macro(source_file="Master Program/Master Program Forecasting Rates.sas", macro_name="macro_var", arguments=_arguments, sas_block=_sas_block)

