"""Auto-generated SAS->Python structural conversion module.

Source: Claims Programs/Manual Change for Claims Data Cleaning.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def manual_raw_data_change_error_mr(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %manual_raw_data_change_error_mr."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """	data MR;
		set MR; 
		if substr(permid, 1, 2) NE "PR";
	run;"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="manual_raw_data_change_error_mr", arguments=_arguments, sas_block=_sas_block)

def manual_raw_data_change_error_dp(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %manual_raw_data_change_error_dp."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """	data DP;
		set DP; 
		if substr(permid, 1, 2) NE "PR";
	run;"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="manual_raw_data_change_error_dp", arguments=_arguments, sas_block=_sas_block)

def manual_raw_data_change_claim(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %manual_raw_data_change_claim."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """	data full_data;
	set full_data; 
	where substr(permid, 1, 2) NE "PR";
		/* CC 8/23/22 - zero out underpayments for specific claim at the claim level */
		if permid = "CAC2302F016" then do;
			Processing_Underpayment = 0;
			Underpayments = 0;
		end;
	run;"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="manual_raw_data_change_claim", arguments=_arguments, sas_block=_sas_block)

def manual_data_change(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %manual_data_change."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ /* change any specific claims here, for example incorrect dollar amounts */
/* if perm_id = X then amount_paid = X*/"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="manual_data_change", arguments=_arguments, sas_block=_sas_block)

def pop_totals_manual_change(indata: Any = None, outdata: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %pop_totals_manual_change."""
    _arguments = {
        "indata=": indata,
        "outdata=": outdata,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """data &outdata.;
	set &indata.;
	*Any manual changes to population data; 
	if missing(fyear) then fyear = "&pyear.";
run; """
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="pop_totals_manual_change", arguments=_arguments, sas_block=_sas_block)

def pop_totals_manual_change_nodup(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %pop_totals_manual_change_nodup."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%PrintMessage("Remove duplicate - nodupkey by state qtr type stratum totclm_clm");
data temp; 
	set poptotals_temp; 
	if not missing(cnt_act_sampled); 
	if cnt_act_sampled_clm ne 0; /* CS Added 8/22/2023 since 2 strata that ELG only oversamples */
run;  
proc sort data = temp out = poptotals_temp nodupkey ;
by state qtr type stratum totclm;
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="pop_totals_manual_change_nodup", arguments=_arguments, sas_block=_sas_block)

def pop_totals_manual_change_nodup2(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %pop_totals_manual_change_nodup2."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%PrintMessage("Remove duplicate - nodupkey by state qtr type stratum totclm_clm");
proc sort data = pop_totals_temp out = pop_totals_temp nodupkey ;
by state type qtr strata;
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="pop_totals_manual_change_nodup2", arguments=_arguments, sas_block=_sas_block)

def se_rate_data_manual_change(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %SE_Rate_data_Manual_change."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """"""
    return run_transpiled_macro(source_file="Claims Programs/Manual Change for Claims Data Cleaning.sas", macro_name="SE_Rate_data_Manual_change", arguments=_arguments, sas_block=_sas_block)

