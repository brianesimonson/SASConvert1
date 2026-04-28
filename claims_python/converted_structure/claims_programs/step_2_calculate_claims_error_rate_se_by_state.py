"""Auto-generated SAS->Python structural conversion module.

Source: Claims Programs/Step 2 - Calculate claims error rate SE by state.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

INCLUDES = [
    "&mainpath./Claims Error Rates/Programs/Manual Change for Claims Data Cleaning.sas",
    "&mainpath./Global Macros/include macros.sas",
    "&mainpath./Global Macros/Reconcile Macro/PrintMessage_Macro.sas",
    "&mainpath./Global Macros/Reconcile Macro/4_ExportQC.sas",
]

def mainpath(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %mainpath."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """*/
/*	/sas_data_cms/Project/PERM/Statistical Reporting/&permyear*/
/*"""
    return run_transpiled_macro(source_file="Claims Programs/Step 2 - Calculate claims error rate SE by state.sas", macro_name="mainpath", arguments=_arguments, sas_block=_sas_block)

def ratecalculation(type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %RateCalculation."""
    _arguments = {
        "type": type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%if &type. = _TC %then %do; 
	%let type2 = t; 
%end; 
%else %do; 
	%let type2 = ;
%end; 
%PrintMessage("Read and modify sample data &type.");
*read/set sample;
data all; 
format strata $20. stratum $3.;
set error.claim_sample_data&type.;
 
state=state_name;
/*assign program type corectly for all good (non-garbage claims)*/
if program="Medicaid" and claim_type = "FFS" then program_type="MF";
else if program="Medicaid" and claim_type = "MC " then program_type="MM";
else if program="CHIP" and claim_type = "FFS" then program_type="SF";
else if program="CHIP" and claim_type = "MC " then program_type="SM";

if state_stratum="1A" then state_strata=1;
else if state_stratum="1B" then state_strata=2;
else if state_stratum="2" then state_strata=3;
else if state_stratum="3" then state_strata=4;

if program_type="MM" then state_strata=state_strata+4;
else if program_type = "SF" then state_strata=state_strata+12;
else if program_type = "SM" then state_strata=state_strata+16;

if missing(qtr) then qtr = qtr0;
if missing(state_id) then state_id = state0;
stratum = stratum0;
if length(stratum) = 1 then stratum0 = "0"||stratum0;

*use sample universe (original) variables, not reporting universe (new) variables;
*type, qtr0, stratum0, state0 and not program_type,qtr,stratum,state_id;
/* CS Updated 5/8/23 -- for Oversample Strata */
if sampling_quarter = "S" then strata = COMPRESS(CAT(state0, "&pyear.", "O", sampling_quarter, type, stratum0));
else strata = COMPRESS(CAT(state0, "&pyear.", "0", sampling_quarter, type, stratum0)); /* CS Edited - 5/25/2021 - Update QTR to Sampling Quarter */

/* SC 9/14/20 - add drop_temp */

if drop_temp EQ 1 then do;
	program = "None";
	program_type="XX";
	processing_error_code1 = "";
	medical_review_error_code1 = "";
	error_total = 0;
	overpayments = 0;
	underpayments = 0;
	medical_review_overpayment = 0;
	medical_review_underpayment = 0;
	medical_review_error_total = 0;
	processing_overpayment = 0;
	processing_underpayment = 0;
	processing_error_total = 0;
	amount_paid = 0;
	paid = 0;
end;

/* JUNK CLAIMS (claims in Lewin data that were not in APLUS) */
if drop_from_review EQ 1 then do;
	program = "None";
	program_type="XX";
	processing_error_code1 = "";
	medical_review_error_code1 = "";
	error_total = 0;
	overpayments = 0;
	underpayments = 0;
	medical_review_overpayment = 0;
	medical_review_underpayment = 0;
	medical_review_error_total = 0;
	processing_overpayment = 0;
	processing_underpayment = 0;
	processing_error_total = 0;
	amount_paid = 0;
	paid = 0;
end;
/* Claims in Lewin but have not been reviewed yet by A+ */
else if flag = "all" then do;
	flag_not_in_aplus = 1;
	amount_paid = final_paidamt;
	paid = final_paidamt;

	/* assign error */
	processing_error_code1 = "PENDING";
	processing_reason_for_error1 = "PENDING";
	medical_review_error_code1 = "PENDING";
	medical_review_reason_for_error1 = "PENDING";

	medical_review_overpayment = amount_paid;
	medical_review_underpayment = 0;
	medical_review_error_total = amount_paid;
	
	processing_overpayment = amount_paid;
	processing_underpayment = 0;
	processing_error_total = amount_paid;

	overpayments = amount_paid;
	underpayments = 0;
	error_total = amount_paid;
end;

paid2=amount_paid;
gross_error=error_total;
net_error=overpayments - underpayments;
dummyx=1;
cid = perm_id;
span_date_adj_ind=1;
CLAIM_LINE_ITEM_NUMBER=1;
dummyline=1;
dummy=1;

*not including pending cases;
if pending NE 1 then no_pending = 1;

run;
/*%let type = ;*/
data jstest5;
set error.claim_sample_data&type.;
if abs(amount_paid - paid) >= .01;
keep drop_from_review flag amount_paid final_paidamt paid;
run;


data jstest4;
set all;
if abs(amount_paid - paid) >= .01;
keep strata perm_id drop_from_review flag amount_paid final_paidamt paid;
run;
proc freq data=all; tables drop_from_review*flag/list missing; run; 
proc freq data=jstest4; tables drop_from_review*flag/list missing; run; 

data qc; 
	set all;
	if drop_from_review EQ 1;
	keep perm_id drop_from_review flag amount_paid final_paidamt paid;
run;
proc sort data=jstest4; by perm_id; run; 
proc sort data=error.claim_sample_data&type.; by PERM_ID; run; 
data qc2_orig; 
	merge error.claim_sample_data&type. jstest4(in=a keep=perm_id); 
	by perm_id;
	if a;
	keep perm_id drop_from_review flag amount_paid final_paidamt paid;
run;

/* Claim data - Variable check*/
proc freq data=all;
tables flag*state_stratum state state_name program_type*state_strata*flag/list missing;
run;

/* get lines on the claim level, these claims will have the same weight that they were sampled with
	however, they will not be double counted in the weight */

proc means data=all nway noprint;
class strata lewin_permid;
var dummyx;
output out=all_temp (drop = _type_ _freq_) sum=;
run;

data all_temp;
set all_temp;
if dummyx >1 then dummyx = 1;
run;

/* add up claims per strata */
proc means data=all_temp nway noprint;
class strata;
var dummyx;
output out=sample_counts (drop=_type_ _freq_) sum=m1;
run;

data testsample_counts; /* should be empty */
set sample_counts;
by strata;
if first.strata Ne last.strata;
run;

proc sql;
	select count(*) into: numobs
	from testsample_counts; 
quit; 

%PrintMessage("Action Needed if >0: Claims data has &numobs. observations with Duplicate Strata");

%PrintMessage("Merge with population data and");
******************* create weights *******************;
data error.test_wt; /* should be empty, or at least poptotals should have more */
merge sample_counts (in=insamp) poptotals_temp (in=intotal);
by strata;
if insamp and intotal then flagwt = "both          ";
else if insamp then flagwt = "sample only";
else if intotal then flagwt = "pop only";
else flagwt = "prob";
if m1 ne cnt_act_sampled;
run;
proc freq data=error.test_wt; tables flagwt/list missing out=pop_merge_flag;run;
data error.in_sample_only error.in_pop_only;
set error.test_wt;
if flagwt = "sample only" then output error.in_sample_only;
else if flagwt = "pop only" then output error.in_pop_only;
/*drop count flag;*/
run;

data error.weights2;
merge sample_counts (in=insamp) poptotals (in=intotal);
by strata;
if insamp and intotal then flagwt = "both          ";
else if insamp then flagwt = "sample only";
else if intotal then flagwt = "pop only";
else flagwt = "prob";

*Sample data may be incomplete compared to universe totals;
if insamp; /* CC added 8/15/2024 */

/*use weights already in data*/
/*weight = sample_weight;*/
/*weight =  pop_lines/m1;*/

universe_lines=totclm;
pop_lines=universe_lines;
line_wt = totclm/m1;
weight = line_wt;
keep strata universe_lines pop_lines m1 weight line_wt flagwt;
run;

proc means data=error.weights2 nway noprint;
where flagwt NE "both";
class flagwt strata;
var m1 universe_lines;
output out=error.weight_nomatch (drop = _type_) sum= sample_count universe_lines;
run;

*merge in weights2 with all data set;
proc sort data=all; by strata; run;
proc sort data=error.weights2; by strata; run;

data error.claim_merged_data&type.;
merge all (in=inall) error.weights2 (in=inweight);
by strata;
if inall;
if inall and inweight then flagclm = "both";
else if inall then flagclm = "prob";
run;


data fmr_stratum_totals;
set error.fmr_stratum_totals;

data error.total_file&type.;
set fmr_stratum_totals;
if claim_type NE "ELG";
if program="Medicaid" and claim_type = "FFS" then program_type="MF";
else if program="Medicaid" and claim_type = "MC " then program_type="MM";
else if program="CHIP" and claim_type = "FFS" then program_type="SF";
else if program="CHIP" and claim_type = "MC " then program_type="SM";

if state_stratum="1A" then state_strata=1;
else if state_stratum="1B" then state_strata=2;
else if state_stratum="2" then state_strata=3;
else if state_stratum="3" then state_strata=4;

if program_type="MM" then state_strata=state_strata+4;
else if program_type = "SF" then state_strata=state_strata+12;
else if program_type = "SM" then state_strata=state_strata+16;
%if &type. = _TC %then %do; 
payments = fmr_total_pmts;
%end; 
%else %do; 
payments=fmr_federal_pmts;
%end; 
total_states = state_pop_count;
run;

/* create sweight */
data fmr_stratum_claim;
set error.total_file&type.;
if claim_type NE "ELG";
keep  state_strata fmr_total_pmts fmr_federal_pmts;
run;
proc sort data=fmr_stratum_claim;by  state_strata;run;

data claim_merged_data;
/* add where statement here */
set error.claim_merged_data&type.;
projpaid = amount_paid*line_wt;
run;

proc means data=claim_merged_data nway noprint;
class state_strata;
var projpaid;
output out=sweight sum=sumprojpaid;
run;

proc sort data=claim_merged_data; by program; run;

data error.afr_adjustment;
set error.afr_adjustment;
keep program afr_adjustment;
run;

proc sort data=error.afr_adjustment;by program;run;

data claim_merged_data2;
merge claim_merged_data error.afr_adjustment;
by program;
run;

proc sort;by state_strata;

data error.claim_merged_data_sweight&type.;
merge claim_merged_data2 sweight fmr_stratum_claim(in=a);
by state_strata;
if a and flag ="both" then do;
	%if &type.=_TC %then %do;
	multiplier = fmr_total_pmts/sumprojpaid;
	%end; 
	%else %do; 
	multiplier = fmr_federal_pmts/sumprojpaid;
	%end;
	sweight_fmr = line_wt*multiplier;
	sweight = line_wt*multiplier*afr_adjustment;
end;
if not missing(PERM_ID);
drop _type_ _freq_ fmr_total_pmts fmr_federal_pmts sumprojpaid projpaid;
run;

data jstest3;
	set claim_merged_data2;
	if paid ne amount_paid;
	keep perm_id pending paid amount_paid;
run;
%PrintMessage("Create sweights state");
/* create sweight state */
/* Since this is TC, benchmark directly to universe expenditures */
/* Create error.total_file_strat_TC - this is needed for both TC and federal*/
%if &type. = _TC %then %do;
data error.total_file_strat_TC;
set poptotals_temp;
universe_payments = totpaid_clm;
keep strata universe_payments;
run;
proc sort; by strata; run;
%end;

%else %do;
* Additional step to get federal universe_payments;

/* Read in TC universe expenditures */
data total_file_strat;
set error.total_file_strat_TC;
run;

/* get federal to total computable ratio based on projpaid */
proc means data=error.claim_merged_data_sweight_TC nway noprint;
class strata;
var amount_paid;
weight line_wt;
output out=strata_tc (drop = _type_ _freq_) sum=projpaid_strata_tc;
run;

proc means data=error.claim_merged_data_sweight nway noprint;
class strata;
var amount_paid;
weight line_wt;
output out=strata_fed (drop = _type_ _freq_) sum=projpaid_strata_fed;
run;

data total_file_strat2;
merge total_file_strat strata_tc strata_fed;
by strata;
universe_payments_fed = universe_payments * projpaid_strata_fed/projpaid_strata_tc;
drop universe_payments;
run;
 
data error.total_file_strat;
set total_file_strat2;
universe_payments = universe_payments_fed;
keep strata universe_payments;
run;
%end; 

proc means data=error.claim_merged_data_sweight&type. nway noprint;
class strata;
var amount_paid;
weight line_wt;
output out=bystrata (drop = _type_ _freq_) sum=projpaid_strata;
run;

/*check if any strata has $0 projpaid*/
proc sql; 
	create table projpaid_strata_ck as
	select *
	from bystrata
	where projpaid_strata = 0 or missing(projpaid_strata);
quit; 

data multiplier_strata;
/*format multiplier_strata 20.12;*/
merge error.total_file_strat&type. bystrata;
by strata;
multiplier_strata = universe_payments/projpaid_strata;
keep strata multiplier_strata;
run;

data claim_merged_data_sweight;
set error.claim_merged_data_sweight&type.;
run;
proc sort; by strata; run;

data claim_merged_data_sweight2;
merge claim_merged_data_sweight (in=indata) multiplier_strata;
by strata;
if indata; /* CC added 8/15/2024 */
sweight_strata = line_wt*multiplier_strata;
run;

/* benchmark to state CMS 64/21 expenditures */
%PrintMessage("benchmark to state CMS 64/21 expenditures");
data fmrdata;
retain state;
set error.fmrdata;
state = state_name;
keep program state total_ffs total_mc fed_ffs fed_mc;
run;
proc sort data=fmrdata;by program state; run;

data claim_merged_data_sweight_strata;
set claim_merged_data_sweight2;
if claim_type = "FFS" then projpaid_ffs = amount_paid*sweight_strata;
else if claim_type = "MC" then projpaid_mc = amount_paid*sweight_strata;
run;

proc sort data=claim_merged_data_sweight_strata; by program state; run;

proc means data=claim_merged_data_sweight_strata nway noprint;
class program state;
var projpaid_ffs projpaid_mc;
output out=sweightst sum=sumprojpaid_ffs sumprojpaid_mc;
run;

data sweightst;
set sweightst;
if missing(sumprojpaid_ffs) then missingffs = 1;
if missing(sumprojpaid_mc) then missingmc = 1;
run;

%PrintMessage("Export Final Claim Sweight State");
data error.claim_merged_data_sweight_state&type2.;
merge claim_merged_data_sweight_strata sweightst fmrdata(in=a);
by program state;
*for states that have 0 sumprojpaid_mc or 0 sumprojpaid_ffs, move over FMR dollars;
	/*if missingffs or missingmc then do;
		if missingffs then multiplier_state = sum(total_ffs,total_mc)/sumprojpaid_mc;
		if missingmc then multiplier_state = sum(total_ffs,total_mc)/sumprojpaid_ffs;
	end;
	else do;*/
		%if &type. = _TC %then %do;
		if claim_type = "FFS" then multiplier_state = total_ffs/sumprojpaid_ffs;
		else if claim_type = "MC" then multiplier_state = total_mc/sumprojpaid_mc;
		%end; 
		%else %do; 
		if claim_type = "FFS" then multiplier_state = fed_ffs/sumprojpaid_ffs;
		else if claim_type = "MC" then multiplier_state = fed_mc/sumprojpaid_mc;
		%end;
	/*end;*/

if a then do;
	sweight_state = sweight_strata*multiplier_state;
end;

drop total_ffs total_mc fed_ffs fed_mc projpaid_ffs projpaid_mc sumprojpaid_ffs sumprojpaid_mc _type_ _freq_ missingffs missingmc;
run;

data error.missing_sweight&type2.;
	set error.claim_merged_data_sweight_state&type2.;
	if missing(sweight_state) and program ne 'None';
	keep strata perm_id claim_type program amount_paid line_wt;
run;


data jstest;
	set error.claim_merged_data_sweight_state&type2.;
	if paid ne amount_paid;
	run;

/* test claim data */
data claim_test&type2.; /* should be empty */
retain program state strata aplus_permid lewin_permid gross_error paid paid2 error_total amount_paid overpayments underpayments
	medical_review_error_total medical_review_overpayment medical_review_underpayment
	processing_error_total processing_overpayment processing_underpayment;
set error.claim_merged_data_sweight_state&type2.;
if abs(amount_paid - paid) >= .01 then flag_paid = 1;
if abs(amount_paid - paid2) >= .01 then flag_paid2 = 1;
if abs(error_total - gross_error) >= .01 then flag_gross_error = 1;
if abs(error_total - sum(overpayments,underpayments))>=.01 then flag_sumerr = 1;
if abs(medical_review_error_total - sum(medical_review_overpayment,medical_review_underpayment))>=.01 then flag_med = 1;
if abs(processing_error_total - sum(processing_overpayment,processing_underpayment))>=.01 then flag_dp = 1;
if sum(flag_paid,flag_paid2,flag_gross_error,flag_med,flag_dp) >=1;
keep program state strata aplus_permid lewin_permid gross_error paid paid2 error_total amount_paid overpayments underpayments
	medical_review_error_total medical_review_overpayment medical_review_underpayment
	processing_error_total processing_overpayment processing_underpayment;
run;

proc freq data=error.claim_merged_data_sweight_state&type2.; 
tables program/list missing; run ;
/* any manual changes to sE state data */
%SE_Rate_data_Manual_change;

*calculate overall file;
data temp;
set error.claim_merged_data_sweight_state&type2.;
run;

data all2;set temp;run;

proc freq data=all2;
table state program_type*state_strata*flag;
run;

%macro extract_relevant_pgmtype_data(program_type,xnumerator,xdenominator);

DATA all;
SET all2;
if program_type NE "&program_type." then do;
	&xnumerator. = 0;
	&xdenominator. = 0;
end;
RUN;

DATA total_file;
SET error.total_file&type.;
IF program_type eq "&program_type";
/*if program_type EQ "&program_type.";*/
RUN;


DATA weights2;
SET error.weights2;
/*if program_type EQ "&program_type.";*/
RUN;"""
    return run_transpiled_macro(source_file="Claims Programs/Step 2 - Calculate claims error rate SE by state.sas", macro_name="RateCalculation", arguments=_arguments, sas_block=_sas_block)

def extract_relevant_pgmtype_data(program_type: Any = None, xnumerator: Any = None, xdenominator: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %extract_relevant_pgmtype_data."""
    _arguments = {
        "program_type": program_type,
        "xnumerator": xnumerator,
        "xdenominator": xdenominator,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """"""
    return run_transpiled_macro(source_file="Claims Programs/Step 2 - Calculate claims error rate SE by state.sas", macro_name="extract_relevant_pgmtype_data", arguments=_arguments, sas_block=_sas_block)

def run_rates(program_type: Any = None, out: Any = None, data: Any = None, numerator: Any = None, denominator: Any = None, domainvar: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %run_rates."""
    _arguments = {
        "program_type": program_type,
        "out": out,
        "data": data,
        "numerator": numerator,
        "denominator": denominator,
        "domainvar": domainvar,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%extract_relevant_pgmtype_data(&program_type,&numerator,&denominator);

%let service_type_id=&domainvar.;
%let numerator=&numerator.;
%let denominator=&denominator.;
%let dataset=&data.;
%let outputfile = &out.;

PROC SORT DATA=all;
BY strata;
RUN;


PROC SORT DATA=weights2;
BY strata;
RUN;


%raterun2;"""
    return run_transpiled_macro(source_file="Claims Programs/Step 2 - Calculate claims error rate SE by state.sas", macro_name="run_rates", arguments=_arguments, sas_block=_sas_block)

def check(res_type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %check."""
    _arguments = {
        "res_type": res_type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """data &res_type._overall;
set error.&res_type.statelevel_overall&type.;
if state = " ";
program_type = "&res_type.";
keep program_type projpaid;
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Step 2 - Calculate claims error rate SE by state.sas", macro_name="check", arguments=_arguments, sas_block=_sas_block)

