"""Auto-generated SAS->Python structural conversion module.

Source: Reconcile Macro/1_Reconcile_Lewin_and_APLUS_Data.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def manual_lewindata_change(inputdata: Any = None, outdata: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %manual_lewindata_change."""
    _arguments = {
        "inputdata": inputdata,
        "outdata": outdata,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ 
/* make any manual changes to lewin data here */
/* does not contain any permanent data changes */
proc freq data=&inputdata.; tables type; run; 
data lewin_temp;
format New_Payment_Status New_SampUnit Change_reported_to_A___as_necess Email_Subject final_paystatus $255.
new_paid_amount2 best12. type2 $4. insample2 8. indetails2 8. quarter_lewin 8.;
set &inputdata.;
%if &error_type. = Claim %then %do;
	if samp_DP_ind = "Y" or samp_MR_ind = "Y";
%end; 
%else %do;
	if samp_elig_ind = "Y";
%end; 

/* Make New Paid Amount Numeric */
new_paid_amount = tranwrd(new_paid_amount,"$","");
new_paid_amount = tranwrd(new_paid_amount,",","");
new_paid_amount = compress(new_paid_amount);

new_paid_amount2 = input(new_paid_amount, best12.);
drop_from_review2 = input(drop_from_review, best12.);
drop_from_elg_review2 = input(drop_from_elg_review, best12.);
type2 = type;
quarter_lewin = quarter;

if insample = "Y" then insample2 = 1;
else if insample = "N" then insample2 = 0;
if indetails = "Y" then indetails2 = 1;
else if indetails = "N" then indetails2 = 0;
paid_date2 = input(paid_date, mmddyy10.);
date_of_payment2 = input(date_of_payment, mmddyy10.);
date_of_payment_line2 = input(date_of_payment_line, mmddyy10.);
final_paiddt2=compress(final_paiddt, '/');

drop quarter REPORTING_UNIVERSE new_paid_amount drop_from_review drop_from_elg_review type insample indetails date_of_payment date_of_payment_line final_paiddt paid_date; /* variables retained from CNI data */ 
run;

data lewin_temp2;
set lewin_temp;
format paid_date mmddyy10. date_of_payment mmddyy10. date_of_payment_line mmddyy10. final_paiddt 8.;
new_paid_amount = new_paid_amount2;
drop_from_review = drop_from_review2;
drop_from_elg_review = drop_from_elg_review2;
type = type2;

insample							= insample2;
indetails							= indetails2;
final_paiddt						= final_paiddt2;
paid_date							= paid_date2;
date_of_payment					 	= date_of_payment2;
date_of_payment_line				= date_of_payment_line2;

drop new_paid_amount2 drop_from_review2 drop_from_elg_review2 type2 indetails2 insample2 final_paiddt2 paid_date2 date_of_payment2 date_of_payment_line2;
run;



/***************************** MANUAL DATA CHANGES HERE *****************************************/
/***************************** MANUAL DATA CHANGES HERE *****************************************/
/***************************** MANUAL DATA CHANGES HERE *****************************************/
data manual;
set lewin_temp2;
if perm_ID in ("MNC2201F540","MNC2202F538","MNC2202F539","MNC2203F537") then do; /* update sampling quarter */
	sampling_quarter = "4";
end;
run;

/***************************** END MANUAL DATA CHANGES *****************************************/
/***************************** END MANUAL DATA CHANGES *****************************************/
/***************************** END MANUAL DATA CHANGES *****************************************/

data &outdata.;
	format sampling_universe $2. final_paidamt dollar21.2 stratum0 $4. final_paiddate mmddyy10.;
	set manual;
	lewin_permid = perm_id;
	permidmatch = final_perm_id; /* CC: use latest perm id to merge Lewin and RC data */

	if not missing(state);

	final_paiddate = final_paiddt;
	*final_PaidAmt = final_PaidAmt;
	*final_PayStatus = final_PayStatus;
	*final_xOverInd = final_xOverInd;
	*final_FixedPayInd = final_FixedPay;

	sampling_universe = trim(type);
	sampling_level0 = sampling_level_sam; 
	state0 = state;
	qtr0 = qtr;
	stratum0 = strata;
	
	drop perm_id state qtr stratum strata;
	%if &error_type. = Claim and &status. = RECON %then %do; 
		if drop_from_review NE 1; /* dropped here for reconciliation purposes, DO NOT DROP in actual data clean up, 
		these claims need to be in the weight */
	%end; 
	%else %if &error_type. = Elig and &status. = RECON %then %do; 
		if drop_from_elg_review NE 1;/* dropped here for reconciliation purposes, DO NOT DROP in actual data clean up, 
		these claims need to be in the weight */
	%end; 
	if type = "MP" then type = "MF";
run;

/*data lewin_temp4;*/
/*	set lewin_temp2;*/
/*	if strata = "So01" then strata1 = "S_01";*/
/*	else if strata = "So02" then strata1 = "S_02";*/
/*	else if strata = "So03" then strata1 = "S_03";*/
/*	else if strata = "So04" then strata1 = "S_04";*/
/*	else if strata = "So05" then strata1 = "S_05";*/
/*	else strata1 = strata;*/
/*	drop strata;*/
/*run;*/
/**/
/*data lewin_temp2;*/
/*	set lewin_temp4;*/
/*	strata = strata1;*/
/*	drop strata1;*/
/*run;*/"""
    return run_transpiled_macro(source_file="Reconcile Macro/1_Reconcile_Lewin_and_APLUS_Data.sas", macro_name="manual_lewindata_change", arguments=_arguments, sas_block=_sas_block)

