"""Auto-generated SAS->Python structural conversion module.

Source: Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def loopit_mr(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %loopit_mr."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """/* Determine max number of Error Codes */
proc means data = toe_varnum;
var &abbr._toe_varnum;
output out = max_toe_var (drop = _type_ _freq_) max=;
run;

data max_toe_var;
set max_toe_var;
call symput ("max_toe_varnum", &abbr._toe_varnum);
run;

%do i = 1 %to &max_toe_varnum.;

data &abbr._errors ;
	format &toe.&i. $10. &qual.&i. $200. &abbr._toe&i. $100. &abbr._toe_def&i. $100. &abbr._subqualifiers&i. $750. &abbr._subqualifiers_orig&i. $750.
	&name._overpayment&i. best12. &name._underpayment&i. best12. &name._error_total&i. best12.  mapped_subqualifier_code&i. $250. unique_subqualifier_code&i. $250.
	&name._reason_orig&i. $200. &name._mapped_qualcode&i. $10. &name._unique_qualcode&i. $10. missingdocs&i. $750.;
	%if &i = 1 %then %do;
	set &abbr._errors_transpose ;
	%end;
	%else %do;
	set &abbr._errors;
	%end;
	&toe.&i. = scan(var&i.,1,"_@#$_");
	&qual.&i. = scan(var&i.,2,"_@#$_");
	&abbr._toe&i. = scan(var&i.,3,"_@#$_");
	&abbr._toe_def&i. = scan(var&i.,4,"_@#$_");
	&name._overpayment&i.=scan(var&i.,5,"_@#$_");
	&name._underpayment&i.=scan(var&i.,6,"_@#$_");
	&name._error_total&i. = scan(var&i.,7,"_@#$_");
	&name._reason_orig&i. = scan(var&i.,8,"_@#$_");
	&name._mapped_qualcode&i. = scan(var&i.,9,"_@#$_");
	&name._unique_qualcode&i. = scan(var&i.,10,"_@#$_");
	missingdocs&i. = scan(var&i.,11,"_@#$_");
	&abbr._subqualifiers&i. = scan(var&i.,12,"_@#$_");
	&abbr._subqualifiers_orig&i. = scan(var&i., 13,"_@#$_");
	&abbr._unique_subqualifier_code&i. = scan(var&i.,14,"_@#$_");
	&abbr._mapped_subqualifier_code&i. = scan(var&i.,15,"_@#$_");
	
	if &qual.&i. = "No Qualifier" then &qual.&i. ="" ; 
	if &name._reason_orig&i. = "No Qualifier" then &name._reason_orig&i. ="" ; 
	if &name._mapped_qualcode&i. = "NA" then &name._mapped_qualcode&i. = "";
	if &name._unique_qualcode&i. = "NA" then &name._unique_qualcode&i. = "";
	if missingdocs&i. = "NA" then missingdocs&i. = "";
	if &abbr._subqualifiers&i. = "NA" then &abbr._subqualifiers&i. ="";
	if &abbr._subqualifiers_orig&i. = "NA" then &abbr._subqualifiers_orig&i. = "";
	if &abbr._unique_subqualifier_code&i. = "NA" then unique_subqualifier_code&i. = "";
	if &abbr._mapped_subqualifier_code&i. = "NA" then mapped_subqualifier_code&i. = "";
	if &abbr._toe_def&i. = "Pending" then &abbr._toe_def&i. = "";
	if &abbr._toe&i. = "Pending" then &abbr._toe&i.="";
	if missing(&name._overpayment&i.) then &name._overpayment&i. = 0 ; 
	if missing(&name._underpayment&i.) then &name._underpayment&i. = 0 ; 
	if missing(&name._error_total&i.) then &name._error_total&i. = 0;
	drop var&i.;
run ;

%end;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="loopit_mr", arguments=_arguments, sas_block=_sas_block)

def loopit_dp(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %loopit_dp."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """/* Determine max number of Error Codes */
proc means data = toe_varnum;
var &abbr._toe_varnum;
output out = max_toe_var (drop = _type_ _freq_) max=;
run;

data max_toe_var;
set max_toe_var;
call symput ("max_toe_varnum", &abbr._toe_varnum);
run;

%do i = 1 %to &max_toe_varnum.;

data &abbr._errors ;
	format subqualifiers&i. $750. subqualifiers_orig&i. $750. mapped_subqualifier_code&i. $250. unique_subqualifier_code&i. $250.;
	format &toe.&i. $10. &qual.&i. $200. &abbr._toe&i. $100. &abbr._toe_def&i. $100. 
	&name._overpayment&i. best12. &name._underpayment&i. best12. &name._error_total&i. best12. 
	&name._reason_orig&i. $200. &name._mapped_qualcode&i. $10. &name._unique_qualcode&i. $10.;
	%if &i = 1 %then %do;
	set &abbr._errors_transpose ;
	%end;
	%else %do;
	set &abbr._errors;
	%end;
	&toe.&i. = scan(var&i.,1,"_@#$_");
	&qual.&i. = scan(var&i.,2,"_@#$_");
	&abbr._toe&i. = scan(var&i.,3,"_@#$_");
	&abbr._toe_def&i. = scan(var&i.,4,"_@#$_");
	&name._overpayment&i.=scan(var&i.,5,"_@#$_");
	&name._underpayment&i.=scan(var&i.,6,"_@#$_");
	&name._error_total&i. = scan(var&i.,7,"_@#$_");
	&name._reason_orig&i. = scan(var&i.,8,"_@#$_");
	&name._mapped_qualcode&i. = scan(var&i.,9,"_@#$_");
	&name._unique_qualcode&i. = scan(var&i.,10,"_@#$_");
	subqualifiers&i. = scan(var&i.,11,"_@#$_");
	subqualifiers_orig&i. = scan(var&i.,12,"_@#$_");
	unique_subqualifier_code&i. = scan(var&i.,13,"_@#$_");
	mapped_subqualifier_code&i. = scan(var&i.,14,"_@#$_");
	
	if &toe.&i. in ("P1","P2") then do;
	&toe.&i. = "PENDING";
	&qual.&i. = " " ; 
	&abbr._toe&i. = " " ; 
	&abbr._toe_def&i. = " " ; 
	end;
	if &qual.&i. = "No Qualifier" then &qual.&i. ="" ; 
	if &name._reason_orig&i. = "No Qualifier" then &name._reason_orig&i. ="" ; 
	if &name._mapped_qualcode&i. = "NA" then &name._mapped_qualcode&i. = "";
	if &name._unique_qualcode&i. = "NA" then &name._unique_qualcode&i. = "";
	if subqualifiers&i. = "No Subqualifier" then subqualifiers&i. = "" ;
	if subqualifiers_orig&i. = "No Subqualifier" then subqualifiers_orig&i. = "" ;
	if unique_subqualifier_code&i. = "NA" then unique_subqualifier_code&i. = "";
	if mapped_subqualifier_code&i. = "NA" then mapped_subqualifier_code&i. = "";
	if &abbr._toe_def&i. = "Pending" then &abbr._toe_def&i. = "";
	if &abbr._toe&i. = "Pending" then &abbr._toe&i.="";
	if missing(&name._overpayment&i.) then &name._overpayment&i. = 0 ; 
	if missing(&name._underpayment&i.) then &name._underpayment&i. = 0 ; 
	if missing(&name._error_total&i.) then &name._error_total&i. = 0;
	drop var&i.;
run ;

%end;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="loopit_dp", arguments=_arguments, sas_block=_sas_block)

def imputedfmap(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %ImputedFMAP."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ 
proc import datafile = "&data_path./&ERC_FMAP_rate..csv"
	out = fmapdata
	dbms = csv replace;
	getnames = yes;
/*	range="&ERC_FMAP_rate_range.";*/
run;

data perm.erc_fmap_rate;
	format Program $20. StateFK $20.;
	set fmapdata;
	/* create program and state variables if not already in the imported FMAP file */
	/*	if index(var1, "Medicaid") >= 1 then do;*/
	/*		state = strip(tranwrd(var1, "Medicaid", ""));*/
	/*		program = "Medicaid";*/
	/*	end;*/
	/*	else do;*/
	/*		state = strip(tranwrd(var1, "CHIP", ""));*/
	/*		program = "CHIP";*/
	/*	end;*/
run;

data pending_fmap2;
	set perm.erc_fmap_rate;
	pending_fmap_rate = mean(Q1, Q2, Q3, Q4);
	if stateFK NE "";
	keep program stateFK pending_fmap_rate;
	proc sort; by program StateFK; 
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="ImputedFMAP", arguments=_arguments, sas_block=_sas_block)

def import_mr(type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %import_mr."""
    _arguments = {
        "type": type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%let abbr = MR;
%let name = medical_review;
%let qual = medical_review_reason_for_error;
%let toe = medical_review_error_code; 

*Step a) Import MR; 
proc import datafile="&data_path./&RC_mr_Data..xlsx"
   		out= MR
		dbms = xlsx replace;
		getnames = yes;
		range="&rc_mr_data_range.";
run;

%manual_raw_data_change_error_mr;

*Step b) MR data cleaning - ;
data mr_errors_raw;
format perm_id $11. missingdocs $750. code $5. qualifier $250. mr_subqualifiers $750.;
set mr;
if not missing(permid);
perm_id = permid;

missingdocs= tranwrd(missingdocs,";",",");
missingdocs= tranwrd(missingdocs,"@#$","; ");
*remove quotation marks from qualifier; 
qualifier = compress(qualifier,'"');

code_orig = code;
qualifier = tranwrd(qualifier,".",""); /* CS Added 1/9/2023 */
qualifier_orig = qualifier;
*underpayment = Undepayment;
error_total = overpayment + underpayment;
mr_subqualifiers = Subqualifiers;
mr_subqualifiers = tranwrd(mr_subqualifiers,"(s) ","");
mr_subqualifiers = tranwrd(mr_subqualifiers,"; ",",");
mr_subqualifiers = tranwrd(mr_subqualifiers,".@#$",";");
mr_subqualifiers = tranwrd(mr_subqualifiers,"@#$",";");
mr_subqualifiers = tranwrd(mr_subqualifiers,".","");
mr_subqualifiers_orig = mr_subqualifiers;
keep perm_id code qualifier code_orig qualifier_orig missingdocs overpayment underpayment error_total mr_subqualifiers mr_subqualifiers_orig;
proc sort; by perm_id;
run;
/*check if variables are modified as coded*/

Title "MR Check variables are modified as coded - missingdocs, qualifier, mr_subqualifiers ";
proc freq data=mr_errors_raw; 
tables missingdocs qualifier mr_subqualifiers/list missing; 
run; 


/* Grab Paid FMAP Rate from Master File */
proc import datafile="&data_path./&RC_Final_Data..xlsx"
   		out= full_data
		dbms=xlsx replace;
		getnames = yes;
		range="&rc_final_data_range.";
run;

data full_data_temp;
format perm_id $11. program $11.;
set full_data;
perm_id = permid;
if substr(permid, 3, 1) = "C" then program = "CHIP";
	else program = "Medicaid";
keep perm_id paidfmaprate program StateFK;
proc sort; by program StateFK; 
run;

%ImputedFMAP;

data full_data;
merge full_data_temp (in=input) pending_fmap2;
by program StateFK;
if input;
FORMAT paidfmaprate2 best12.2; 
paidfmaprate2 = paidfmaprate; 
drop paidfmaprate; 
rename paidfmaprate2 = paidfmaprate; 
run;

* Check if there is missing paidfmaprate; 
Title "APLUS Data - FMAP Rate Distribution"; 
proc means data=full_data NWAY N NMISS MIN P5 P25 P50 P75 P95 MAX; 
var paidfmaprate; 
run; 

proc sql;
	select count(*) into: numobs
	from full_data
	where missing(paidfmaprate) or paidfmaprate=0; 
quit; 
%PrintMessage("Action Needed if >0: APLUS data has &numobs. observations with missing or 0 paidfmaprate and will be replaced with imputed FMAP Rate of average across Q1-Q4 for each state and program.");

/*replace missing and 0 with averages*/
data fmap_rate;
set full_data;
if missing(paidfmaprate) or  paidfmaprate = 0 then paidfmaprate = pending_fmap_rate;
/*drop pending_fmap_rate;*/
proc sort; by perm_id;
run;

data mr_errors_raw;
merge mr_errors_raw (in=a) fmap_rate;
by perm_id;
if a;
drop pending_fmap_rate;
run;

%if &type. ne _TC %then %do;
data mr_errors_raw;
set mr_errors_raw;
overpayment = overpayment*(paidfmaprate/100);
underpayment = underpayment*(paidfmaprate/100);
error_total = error_total*(paidfmaprate/100);
run;
%end;
%subqualifier_coding; 
%qualifier_coding(mr_errors_raw2);

/* Check Mapped Qualifier Codes -- Do any "XX" show up? */
proc freq data = &abbr._errors_raw_fin;
table code/out = &abbr._code_check;
run;

proc sql;
	select count(*) into: numobs
	from &abbr._errors_raw_fin
	where code = 'XX'; 
quit; 

%PrintMessage("Action Needed if >0: MR data has &numobs. observations with code = XX");


data &abbr._errors_fin;
set &abbr._errors_raw_fin;
if code = "XX" then do;
	code = code_orig; /* Comment Out for Final Data */
	qualifier = qualifier_orig; /* Comment Out for Final Data */
end;

if qualifier = " " then qualifier = "No Qualifier" ; 
if qualifier_orig = " " then qualifier_orig = "No Qualifier" ; 
if mapped_qualcode = " " then mapped_qualcode = "NA";
if unique_qualcode = " " then unique_qualcode = "NA";
if missingdocs = " " then missingdocs = "NA";
if mr_subqualifiers = " " then mr_subqualifiers = "NA";
if mr_subqualifiers_orig=" " then mr_subqualifiers = "NA";
run ; 

proc sort data = &abbr._errors_fin; by perm_id;
run;
/* Determine Number of Error Codes for Each claim -- Will be used to stack Datasets */
data &abbr._errors_fin ; 
set &abbr._errors_fin ; 
if code ne " " then toe_flag = 1;
run ; 

proc means data = &abbr._errors_fin noprint nway ; 
class perm_id ; 
var toe_flag ; 
output out = toe_varnum (drop = _type_ _freq_) sum = &abbr._toe_varnum ; 
run ; 

data &abbr._errors_fin ; 
set &abbr._errors_fin ;  

%assign_toe_claims_multerr;

if code not in ("P1","P2") then toe_def = strip(toe)||" ("||strip(code)||")";
if toe_def = " " then toe_def = "Pending";
if toe = " " then toe ="Pending";
if code in ("MTD", "DTD") then sort = 3;
else if substr(code,3,2) in ("10","11","12") then sort = 2;
else sort = 1;
proc sort ; by perm_id sort;
run ; 

/* Concatenate All Variables that need to be transposed */
/* Break apart after transpose */
data &abbr._errors_fin;
set &abbr._errors_fin;
var = strip(code)||"_@#$_"||strip(qualifier)||"_@#$_"||strip(toe)||"_@#$_"||strip(toe_def)||"_@#$_"||strip(overpayment)||"_@#$_"||strip(underpayment)||"_@#$_"||strip(error_total)||"_@#$_"||strip(qualifier_orig)||"_@#$_"||strip(mapped_qualcode)||"_@#$_"||strip(unique_qualcode)||"_@#$_"||strip(missingdocs)||"_@#$_"||strip(mr_subqualifiers)||"_@#$_"||strip(mr_subqualifiers_orig)||"_@#$_"||strip(mr_unique_subqualifier_code)||"_@#$_"||strip(mr_mapped_subqualifier_code);
run;

proc transpose data = &abbr._errors_fin out = &abbr._errors_transpose prefix = var;
	by perm_id ; 
	var var ; 
run ; 

%loopit_mr;

data &abbr._errors&type.;
merge &abbr._errors toe_varnum;
by perm_id;
drop _name_;
run;

*get counts of observations; 
proc sql; 
	select count(*) into: obs
	from MR; 
	select count(*) into: uniqueobs
	from toe_varnum; 
	select count(*) into: finalobs
	from &abbr._errors&type.; 
quit; 

%PrintMessage("The imported MR data has &obs. observations and &uniqueobs. unique PERM IDs");
%PrintMessage("the maximum toe is &max_toe_varnum..");
%PrintMessage("The final MR data has &finalobs. observations. ");"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="import_mr", arguments=_arguments, sas_block=_sas_block)

def import_dp(type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %import_dp."""
    _arguments = {
        "type": type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """%let abbr = DP;
%let name = processing;
%let toe = processing_error_code;
%let qual = processing_reason_for_error;

proc import datafile="&data_path./&RC_dp_Data..xlsx"
   		out= DP
		dbms = xlsx replace;
		getnames = yes;
		range="&RC_dp_Data_Range.";
run;

%manual_raw_data_change_error_dp;

data dp_errors_raw;
format perm_id $11. subqualifiers $750. code $5. qualifier $250.;
set dp;
if not missing(permid);
perm_id = permid;

*remove quotation marks from qualifier; 
/*if qualifier = "State relied on Medicare screening and provider not in an approved PECOS record status prior to the state enrollment determination date but in an approved status prior to claim payment date" */
/*then qualifier = "State relied on Medicare screening and provider not in an approved PECOS record status prior to the state enrollment determination date but in an approved status prior to claim payment date";*/
qualifier = compress(qualifier,'"');

code_orig = code;
qualifier_orig = qualifier;
subqualifiers = Subqualifiers;
subqualifiers = tranwrd(subqualifiers,"(s) ","");
subqualifiers = tranwrd(subqualifiers,"; ",",");
subqualifiers = tranwrd(subqualifiers,"@#$",";");
subqualifiers_orig = subqualifiers;

*underpayment = Undepayment;
error_total = underpayment + overpayment;

keep perm_id code qualifier code_orig qualifier_orig subqualifiers subqualifiers_orig overpayment underpayment error_total;
proc sort; by perm_id;
run;

Title "DP Check variables are modified as coded - qualifier, subqualifiers ";
proc freq data=dp_errors_raw; 
tables qualifier subqualifiers/list missing; 
run; 

/*This is created at import_mr module*/
/* Grab Paid FMAP Rate from Master File */
/*
proc import datafile="&data_path.\&RC_Final_Data..xlsx"
   		out= full_data
		dbms=excel2000 replace;
		mixed = yes;
		getnames = yes;
		range="&RC_Final_Data_Range.";
run;

data full_data;
format perm_id $11.;
set full_data;
perm_id = permid;
keep perm_id paidfmaprate;
proc sort; by perm_id;
run;

data full_data;
merge full_data (in=input) perm.imputed_fmap_by_perm_id;
by perm_id;
if input;
run;

data full_data;
set full_data;
if paidfmaprate = "0.00" then paidfmaprate = imputed_fmap_rate;
drop imputed_fmap_rate;
run;
*/
data dp_errors_raw;
merge dp_errors_raw (in=a) fmap_rate;
by perm_id;
if a;
drop pending_fmap_rate;
run;

%if &type. ne _TC %then %do;
data dp_errors_raw;
set dp_errors_raw;
overpayment = overpayment*(paidfmaprate/100);
underpayment = underpayment*(paidfmaprate/100);
error_total = error_total*(paidfmaprate/100);
run;
%end;

%subqualifier_coding; 
%qualifier_coding(dp_errors_raw2);

/* Check Mapped Qualifier Codes -- Do any "XX" show up? */
proc freq data = &abbr._errors_raw_fin;
table code/out = &abbr._code_check;
run;

proc sql;
	select count(*) into: numobs
	from &abbr._errors_raw_fin
	where code = 'XX'; 
quit; 

%PrintMessage("Action Needed if >0: DP data has &numobs. observations with code = XX");


data &abbr._errors_fin;
set &abbr._errors_raw_fin;
if code = "XX" then do;
	code = code_orig; /* Comment Out for Final Data */
	qualifier = qualifier_orig; /* Comment Out for Final Data */
	subqualifiers = subqualifiers_orig; /* Comment Out for Final Data */
end;

if qualifier = " " then qualifier = "No Qualifier" ; 
if qualifier_orig = " " then qualifier_orig = "No Qualifier" ; 
if mapped_qualcode = " " then mapped_qualcode = "NA";
if unique_qualcode = " " then unique_qualcode = "NA";
if subqualifiers = " " then subqualifiers = "No Subqualifier";
if subqualifiers_orig = " " then subqualifiers_orig = "No Subqualifier";
if unique_subqualifier_code = " " then unique_subqualifier_code = "NA";
if mapped_subqualifier_code = " " then mapped_subqualifier_code = "NA";
run ; 

proc sort data = &abbr._errors_fin; by perm_id;
run;
/* Determine Number of Error Codes for Each claim -- Will be used to stack Datasets */
data &abbr._errors_fin ; 
set &abbr._errors_fin ; 
if code ne " " then toe_flag = 1;
run ; 

proc means data = &abbr._errors_fin noprint nway ; 
class perm_id ; 
var toe_flag ; 
output out = toe_varnum (drop = _type_ _freq_) sum = &abbr._toe_varnum ; 
run ; 

data &abbr._errors_fin ; 
set &abbr._errors_fin ;  

%assign_toe_claims_multerr;

if code not in ("P1","P2") then toe_def = strip(toe)||" ("||strip(code)||")";
if toe_def = " " then toe_def = "Pending";
if toe = " " then toe ="Pending";
if code in ("MTD", "DTD") then sort = 3;
else if substr(code,3,2) in ("10","11","12") then sort = 2;
else sort = 1;
proc sort ; by perm_id sort;
run ; 

/* Concatenate All Variables that need to be transposed */
/* Break apart after transpose */
data &abbr._errors_fin;
set &abbr._errors_fin;
var = strip(code)||"_@#$_"||strip(qualifier)||"_@#$_"||strip(toe)||"_@#$_"||strip(toe_def)||"_@#$_"||strip(overpayment)||"_@#$_"||strip(underpayment)||"_@#$_"||strip(error_total)||"_@#$_"||strip(qualifier_orig)||"_@#$_"||strip(mapped_qualcode)||"_@#$_"||strip(unique_qualcode)||"_@#$_"||strip(subqualifiers)||"_@#$_"||strip(subqualifiers_orig)||"_@#$_"||strip(unique_subqualifier_code)||"_@#$_"||strip(mapped_subqualifier_code);
run;

proc transpose data = &abbr._errors_fin out = &abbr._errors_transpose prefix = var;
	by perm_id ; 
	var var ; 
run ; 

%loopit_dp;

data &abbr._errors&type.;
merge &abbr._errors toe_varnum;
by perm_id;
drop _name_;
run;

*get counts of observations; 
proc sql; 
	select count(*) into: obs
	from DP; 
	select count(*) into: uniqueobs
	from toe_varnum; 
	select count(*) into: finalobs
	from &abbr._errors&type.; 
quit; 

%PrintMessage("The imported DP data has &obs. observations and &uniqueobs. unique PERM IDs");
%PrintMessage("the maximum toe is &max_toe_varnum..");
%PrintMessage("The final DP data has &finalobs. observations. ");"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="import_dp", arguments=_arguments, sas_block=_sas_block)

def import_data(outdataset: Any = None, type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %import_data."""
    _arguments = {
        "outdataset": outdataset,
        "type": type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """proc import datafile="&data_path./&RC_Final_Data..xlsx"
   		out= full_data
		dbms=xlsx replace;
		getnames = yes;
		range="&RC_Final_Data_Range.";
run;

%manual_raw_data_change_claim;

proc contents data = full_data;
run;

data full_data;
format perm_id $11.; 
set full_data;
perm_id = permid;
if not missing(perm_id);
drop permid;
run;

proc sort data = full_data; by perm_id; run;

data full_import;
	merge full_data (in=indata) mr_errors&type. (in=inmr) dp_errors&type. (in=indp);
	by perm_id;
	if indata and inmr then flagimport = "both";
	else if indata and indp then flagimport = "both";
	else if indata then flagimport = "data";
	else if inmr then flagimport = "inmr";
	else if indp then flagimport = "indp";
run;

data full_import;
set full_import;
*if hasDP =1 or hasMR = 1; /* Subset to Only Claims that Receive MR or DP Review */
run;

/* check to make sure data imported correctly */
data import_merge;
set full_import;
if flagimport NE "both";
keep perm_id flagimport;
run;

/*proc export data=import_merge*/
/*outfile = "&mainpath.\claims error rates\results\Check Import Merge&type..xls"*/
/*dbms = excel2000*/
/*replace;*/
/*run;*/

/**/
data checkpayment;
set full_import;
/* check that payment variables are correct in the dataset 
	variables needed:
		Amount_Paid_Claim
		Medical_Review_Overpayment
		Medical_Review_Underpayment
		Processing_Overpayment
		Processing_Underpayment
*/
/* change var just for the following checks */
/*processing_overpayment = processingoverpayment;*/
/*processing_underpayment = processingunderpayment;*/
/*Medical_Review_Overpayment = MedicalReviewOverpayment;*/
/*Medical_Review_Underpayment = MedicalReviewUnderpayment;*/
/*amount_paid = amountpaid;*/

Processing_Error_Total = ProcessingErrorTotal;
Medical_Review_Error_Total = MedicalErrorTotal;
Amount_That_Should_Have_Been_Pai = AmountShouldveBeenPaid;
Error_Total = errortotal;
amount_paid_claim = amount_paid;

if missing(amount_paid_claim) then amount_paid_claim = 0;
if missing(medical_review_overpayment) then medical_review_overpayment = 0;
if missing(medical_review_underpayment) then medical_review_underpayment = 0;
if missing(processing_overpayment) then processing_overpayment = 0;
if missing(processing_underpayment) then processing_underpayment = 0;

eq_paid = abs(Amount_Paid_Claim);

/* CS Changed Processing Error Total Logic -- 8/22/23
	logic does not reflect actual calculations, this will make issues show up
	based on CMS logic for Elig 6/30/22, at the claim level, either DP over or DP under will show up */
eq_processing_error_total = abs(abs(Processing_Overpayment) - abs(Processing_Underpayment));
eq_medical_review_error_total = abs(abs(Medical_Review_Overpayment) - abs(Medical_Review_Underpayment));

eq_overpayments = min(eq_paid,sum(abs(Medical_Review_Overpayment),abs(Processing_Overpayment)));
eq_underpayments = sum(abs(Medical_Review_Underpayment),abs(Processing_Underpayment));

if eq_overpayments = eq_paid then do;
		if eq_paid NE 0 then eq_amount_shouldve_paid = 0;
		else eq_amount_shouldve_paid = max(0,(eq_paid-abs(eq_overpayments)+abs(eq_underpayments)));
end;
else eq_amount_shouldve_paid = max(0,(eq_paid-abs(eq_overpayments)+abs(eq_underpayments)));

if eq_paid = 0 then eq_error_total = abs(eq_underpayments);
else eq_error_total = abs(eq_paid-eq_amount_shouldve_paid);
run;

data pay_incorrect;
set checkpayment;

if abs(	eq_paid -	Amount_Paid_Claim		)>.009	or
abs(	eq_processing_error_total 	-	Processing_Error_Total		)>.009	or
abs(	eq_medical_review_error_total 	-	Medical_Review_Error_Total		)>.009	or
abs(	eq_overpayments 	-	Overpayments		)>.009	or
abs(	eq_underpayments 	-	Underpayments		)>.009 or
abs(	eq_amount_shouldve_paid	-	Amount_That_Should_Have_Been_Pai		)>.009	or
abs(	eq_error_total	-	Error_Total		)>.009;

keep perm_id eq_paid 
eq_processing_error_total 
eq_medical_review_error_total 
eq_overpayments 
eq_underpayments 
eq_amount_shouldve_paid
eq_error_total
Amount_Paid_Claim
Processing_Error_Total
Medical_Review_Error_Total
Overpayments
Underpayments
Amount_That_Should_Have_Been_Pai
Error_Total;
run;

/*proc export data=pay_incorrect*/
/*outfile = "&mainpath.\claims error rates\results\Check Error Variables&type..xls"*/
/*dbms = excel2000*/
/*replace;*/
/*run;*/

data &outdataset.;
format State $25. /*subqualifiers $750.*/;
set checkpayment;

state = stnamel(statefk);

/* change payment variables */
/* CS Commented out Variable Change -- 8/22/23 */
/*Amount_Paid_Claim					=	eq_paid 	;*/
/*Processing_Error_Total				=	eq_processing_error_total 	;*/
/*Medical_Review_Error_Total			=	eq_medical_review_error_total 	;*/
/*Overpayments						=	eq_overpayments 	;*/
/*Underpayments						=	eq_underpayments 	;*/
/*Amount_That_Should_Have_Been_Pai	=	eq_amount_shouldve_paid	;*/
/*Error_Total							=	eq_error_total	;*/

drop eq_paid eq_processing_error_total eq_medical_review_error_total eq_overpayments
	eq_underpayments eq_amount_shouldve_paid eq_error_total
/*processingoverpayment*/
/*processingunderpayment*/
/*MedicalReviewOverpayment*/
/*MedicalReviewUnderpayment*/
amount_paid
/*amountpaid*/
ProcessingErrorTotal
MedicalErrorTotal
AmountShouldveBeenPaid
errortotal
statefk;
run ; """
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="import_data", arguments=_arguments, sas_block=_sas_block)

def format_variables(input: Any = None, dataset1: Any = None, dataset2: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %format_variables."""
    _arguments = {
        "input": input,
        "dataset1": dataset1,
        "dataset2": dataset2,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ /* variables that need to be changed */
/* %let input = perm.sample_data1;
%let dataset1 = sample_data1;
%let dataset2 = sample_data2; 
%let type = ;*/
/* xlsx */

/* If Paid FMAP Rate is 0, then Impute the Paid FMAP Rate */
proc sort data = &input.; by program; run;

data &dataset1.;
merge &input. (in=input) pending_fmap2;
by program;
if input;
FORMAT paidfmaprate2 best12.2; 
paidfmaprate2 = paidfmaprate; 
drop paidfmaprate; 
rename paidfmaprate2 = paidfmaprate;
proc sort; by perm_id;
run;

data &dataset1.;
set &dataset1.;
if paidfmaprate = 0 or missing(paidfmaprate) then paidfmaprate = pending_fmap_rate;

if "&type." ne "_TC" then do;
	amount_paid_claim = amount_paid_claim*(paidfmaprate/100);
	error_total = error_total*(paidfmaprate/100);
	overpayments = overpayments*(paidfmaprate/100);
	underpayments = underpayments*(paidfmaprate/100);
	medical_review_error_total = medical_review_error_total*(paidfmaprate/100);
	medical_review_overpayment = medical_review_overpayment*(paidfmaprate/100);
	medical_review_underpayment = medical_review_underpayment*(paidfmaprate/100);
	processing_error_total = processing_error_total*(paidfmaprate/100);
	processing_overpayment = processing_overpayment*(paidfmaprate/100);
	processing_underpayment = processing_underpayment*(paidfmaprate/100);
end;


correct_fmap_rate = input(correctfmaprate, 8.);
hasdp2 = input(hasdp, 8.);
hasmr2 = input(hasmr, 8.);
paid_fmap_rate=paidfmaprate;
iscompletelyloaded2 = input(iscompletelyloaded, 8.);
  

drop pending_fmap_rate iscompletelyloaded hasdp hasmr;
run;

data &dataset1.;
format date_paid mmddyy10. processing_error_code1 $10. medical_review_error_code1 $10. medical_Review_Reason_for_Error $200. medical_review_error_code_raw $10. processing_reason_for_error_raw $200. processing_error_code_raw $10.;
set &dataset1.;

if not missing(perm_id);
if not missing(state);

/* rename variables */
claim_adj_ind 						= claim_adj_indicator;
adjusted_icn						= adjustedicn;
amount_paid 						= amount_paid_claim;
iscompletelyloaded 					= iscompletelyloaded2;
hasdp								= hasdp2;
hasmr								= hasmr2;


adjustmentqualifier = adjustment_qualifier;

/*claim_identifier = claimidentifier;*/
/*date_paid = datepaid;*/
medical_review_accuracy_total = medicalreviewaccuracytotal;
/*medical_review_error_code = medicalreviewerrorcode;*/
/*medical_review_reason_for_error = medicalreviewreasonforerrorcode;*/
/*medical_review_reason_for_error = medical_review_reason_for_error_;*/
/*medicare_xover = medicarexover;*/
/*original_amount = originalamount;*/
processing_accuracy_total = processingaccuracytotal;
/*processing_error_code = processingerrorcode; */
/*processing_reason_for_error_code = processingreasonforerrorcode;*/
/*sampled_line = sampledline;*/
sampling_level = samplinglevel;
/*total_lines = totallines;*/
medicare_xover = SampledMedicareXoverIndicator;

/* Make Error Code Pending for missing error code information */
if hasMR = 0 then medical_review_error_code1 = "N/A";
else if missing(medical_review_error_code1) then medical_review_error_code1 = "PENDING";
if missing(processing_error_code1) then processing_error_code1 = "PENDING";

/* assign medical review error code = "N/A" error totals since these werent in the
	MR error list */
	if medical_review_error_code1 = "N/A" then do;
		mr_toe1 = "N/A";
		medical_review_error_total1 = 0;
		medical_review_error_total2 = 0;
		*medical_review_error_total3 = 0;
		medical_review_overpayment1 = 0;
		medical_review_overpayment2 = 0;
		*medical_review_overpayment3 = 0;
		medical_review_underpayment1 = 0;
		medical_review_underpayment2 = 0;
		*medical_review_underpayment3 = 0;
	end;

	if medical_review_error_code1 = "PENDING" then do;
		medical_review_error_total1 = 0;
		medical_review_overpayment1 = 0;
		medical_review_underpayment1 = 0;
	end;

	if processing_error_code1 = "PENDING" then do;
		processing_error_total1 = 0;
		processing_overpayment1 = 0;
		processing_underpayment1 = 0;
	end;

toe_varnum = max(dp_toe_varnum, mr_toe_varnum);

/* set some variables */
*adjusted_paid_date2 				= input(adjustedpaiddate, mmddyy10.);
adjusted_paid_date2 				= adjustedpaiddate;
claim_category2						= input(categoryidentifier,best12.);
medical_review_error_code_raw 		= medical_review_error_code;
processing_error_code_raw 			= processing_error_code;
processing_reason_for_error_Raw 	= processing_reason_for_error_Code;

drop  
	adjustment_qualifier
	SampledMedicareXoverIndicator
	claim_adj_indicator
	adjustedicn
	adjustedpaiddate
	paidfmaprate
	correctfmaprate
	amount_paid_claim
 	categoryidentifier
	iscompletelyloaded2
/* 	claimidentifier*/
/* 	datepaid*/
 	medicalreviewaccuracytotal
/* 	medicalreviewerrorcode*/
/* 	medicalreviewreasonforerrorcode*/
/*	medical_review_reason_for_error_*/
/* 	medicarexover*/
/* 	originalamount*/
 	processingaccuracytotal
/* 	processingerrorcode*/
/* 	processingreasonforerrorcode*/
/* 	sampledline*/
/*	totallines*/
	medical_review_error_code
	processing_error_code
	processing_reason_for_error_code
 	samplinglevel
	hasmr2
	hasdp2;
run;

data &dataset2.;
format claim_category2 best12. adjusted_paid_date $10. medical_review_error_code $10. processing_error_code $10.;
set &dataset1.;

/* reset variables */
/*adjusted_paid_date = adjusted_paid_date2;*/
claim_category = claim_category2;
adjusted_paid_date = adjusted_paid_date2;
medical_review_error_code = medical_review_error_code_raw;
processing_error_code = processing_error_code_raw;
processing_reason_for_error_code = processing_reason_for_error_raw;

/* change paid to amount paid */
paid = amount_paid ; 

/* keep original error total, amount paid, and medical_review_error_total and processing_error_total*/
error_total_original = error_total;
amount_paid_original = amount_paid;
medical_review_error_total_orig = medical_review_error_total;
processing_error_total_original = processing_error_total;

/* perm id */
aplus_permid = perm_id;
permidmatch = perm_ID; /* want to merge by latest permIDs */
aplus_stratum = stratum;

drop claim_category2 adjusted_paid_date2 medical_review_error_code_raw processing_reason_for_error_raw processing_error_code_raw;
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="format_variables", arguments=_arguments, sas_block=_sas_block)

def mergeddatacleanup(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %mergedDataCleanUp."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """data test; 
set sample_data2&type.;
by permidmatch;
if first.permidmatch NE last.permidmatch;
run;

proc sql; 
	select count(*) into: numobs
	from test; 
quit; 

data sample_data2_test;
set sample_data2&type.;
run;

proc sort data=sample_data2_test;by permidmatch;run;
proc sort data=lewindata;by permidmatch;run;

data lewindata;
set lewindata;
if state0 NE "PR";
run;

%PrintMessage("Action Needed if >0: Claims Sample data has &numobs. observations with duplicate PERM ID");

data merged;
format qtr0 $2.;
merge lewindata (in=inall) sample_data2_test (in=insamp);
by permidmatch;
if inall and insamp then flag = "both";
else if insamp then flag = "samp";
else if inall then flag = "all";


if flag = "samp" then do;
	stratum0 = aplus_stratum;
	state0 = substr(perm_id,1,2);
	qtr0 = compress("0"||quarter);
	if substr(perm_id,8,1) = "F" then claim_type="FFS";
		else if substr(perm_id,8,1) = "M" then claim_type="MC ";
		else claim_type="UNK";
	if claim_type = "FFS" and program = "Medicaid" then type = "MF";
	else if claim_type = "MC" and program = "Medicaid" then type = "MM";
	else if claim_type = "FFS" and program = "CHIP" then type = "SF";
	else if claim_type = "MC" and program = "CHIP" then type = "SM";
	lewin_permid = perm_id;
end;
run;

proc freq data=merged;
where drop_from_review NE 1; 
table flag;
run;
proc freq data=merged; 
tables flag*stratum0 flag*state0 flag*qtr0 flag*claim_type flag*type/list missing; run;
 
/*cleaning*/
data merged2;
set merged;
	state_id=state0;
	if missing(state0) and not missing(state) then state_id = state; 
	
	if flag="all" then do;
		perm_id=lewin_permid;
		
		if substr(lewin_permid,3,1)="C" then program="CHIP";
		else if substr(lewin_permid,3,1)="M" then program="Medicaid";
	end;
	drop state;
run;

data merged2;
	format processing_reason_for_error_code medical_review_reason_for_error $200.;
	set merged2;
	rename amount_that_should_have_been_pai = should_pay;
	format state $20. claim_id $50. qtr $2.;
	

	if missing(state_id) then state_id = state0;

	state = stnamel(state_id);
	state_name = state;
	claim_id = claim_identifier;

	* FFS claims, change the PERM ID to have an F instead of P and grab the claim types;
	if substr(perm_id,8,1) = "P" then do;
		sub1 = substr(perm_id,1,7);
		sub2 = substr(perm_id,9,3);
		perm_id = trim(sub1)||"F"||trim(sub2);
	end;

	* Define claim type;
	if substr(perm_id,8,1) = "F" then claim_type="FFS";
	else if substr(perm_id,8,1) = "M" then claim_type="MC ";
	else claim_type="UNK";

	* Make quarter a string variable;
	qtr = "0" || put(quarter,1.);

	* UPCASE;
	medical_review_error_code = upcase(medical_review_error_code);
	processing_error_code = upcase(processing_error_code);

	* Define state stratum;
   	if state_id in ("CA","FL","GA","IL","NY","NC","OH","PA","TX") then state_stratum="1A";
	else if state_id in ("IN","LA","MA","MI","MN","MO","NJ","TN") then state_stratum="1B";
	else if state_id in ("AL","AZ","AR","CT","IA","KY","ME","MD","MS","NM","OK","OR","SC","VA","WA","WV","WI") then state_stratum="2 ";
	else if state_id in ("AK","CO","DE","DC","HI","ID","KS","MT","NE","NV","NH","ND","RI","SD","UT","VT","WY") then state_stratum="3 ";
	else state_stratum="XX";

	* Set missing values to zero in error variables ;
	if missing(error_total)   then error_total   = 0;
	if missing(overpayments)  then overpayments  = 0;
	if missing(underpayments) then underpayments = 0;
	if missing(medical_review_overpayment) then medical_review_overpayment = 0;
	if missing(medical_review_underpayment) then medical_review_underpayment = 0;
	if missing(medical_review_error_total) then medical_review_error_total = 0;
	if missing(processing_overpayment) then processing_overpayment = 0;
	if missing(processing_underpayment) then processing_underpayment = 0;
	if missing(processing_error_total) then processing_error_total = 0;
	if missing(paid) then paid = 0;
	if missing(amount_paid) then amount_paid = 0;

	*take absolute value;
	if amount_paid < 0 or error_total < 0 or processing_error_total < 0 or Medical_Review_Error_Total < 0
		or overpayments < 0 or underpayments <0 or medical_review_underpayment <0 or medical_review_overpayment<0
		or processing_overpayment<0 or processing_underpayment<0 then flag_negative_pay = 1;
	paid = abs(paid);
	amount_paid = abs(amount_paid);
	error_total = abs(error_total);
	processing_error_total = abs(processing_error_total);
	medical_review_error_total = abs(medical_review_error_total);
	overpayments = abs(overpayments);
	underpayments = abs(underpayments);
	medical_review_underpayment = abs(medical_review_underpayment);
	medical_review_overpayment = abs(medical_review_overpayment);
	processing_overpayment = abs(processing_overpayment);
	processing_underpayment = abs(processing_underpayment);

	
	error_total_hdi = error_total;
	/*if underpayments > error_total then error_total = underpayments;*/

	* Adjust overpayments so they never exceed amt paid.  ;
	* Adjusted overpayments should be used in all analyses;
	overpayments_adj = min(overpayments, amount_paid);
	
	/* new pending logic - make all pending as an error (overpayment) */

	if upcase(processing_error_code1)      in ("PENDING") or
			upcase(medical_review_error_code1)  in ("PENDING") then pending = 1; 
	else pending=0;

	/* retain original dollar variables */
	overpayments_orig = overpayments;
	underpayments_orig = underpayments;
	error_total_orig = error_total;
	amount_paid_orig = amount_paid;

	medical_review_overpayment_orig = medical_review_overpayment;
	medical_review_underpayment_orig = medical_review_underpayment;	
	medical_review_error_total_orig = medical_review_error_total;

	processing_overpayment_orig = processing_overpayment;
	processing_underpayment_orig = processing_underpayment;
	processing_error_total_orig = processing_error_total;

	if pending = 1 then do;
		/* pending because of MR and DP */
		if upcase(processing_error_code1) = "PENDING" and upcase(medical_review_error_code1) in ("PENDING","") then do;
			medical_review_overpayment = amount_paid;
			medical_review_underpayment = 0;
			medical_review_error_total = sum(medical_review_overpayment,medical_review_underpayment);
			processing_overpayment = amount_paid;
			processing_underpayment = 0;
			processing_error_total = sum(processing_overpayment,processing_underpayment);
			end; 
			/* DP pending, then assign DP to fully an error */
		else if upcase(processing_error_code1)="PENDING" then do;
			processing_overpayment = amount_paid;
			processing_underpayment = 0;
			processing_error_total = sum(processing_overpayment,processing_underpayment);
			end;
			/* MR pending, then assign MR to fully an error */
		else if upcase(medical_review_error_code1)="PENDING" or missing(medical_review_error_code1) then do;
			medical_review_overpayment = amount_paid;
			medical_review_underpayment = 0;
			medical_review_error_total = sum(medical_review_overpayment,medical_review_underpayment);
			end;

		overpayments = min(amount_paid,sum(medical_review_overpayment,processing_overpayment));
		underpayments = min(amount_paid,sum(medical_review_underpayment,processing_underpayment));
		error_total = min(amount_paid,sum(overpayments,underpayments));	
	end;

	processing_reason_orig = processing_reason_for_error_code;
	processing_error_code_orig = processing_error_code;
	medical_review_reason_orig = medical_review_reason_for_error;
	medical_review_error_code_orig = medical_review_error_code;
	claim_category_orig = claim_category;

	processing_reason_for_error_code = tranwrd(processing_reason_for_error_code,".","");
	medical_review_reason_for_error = tranwrd(medical_review_reason_for_error,".","");

	drop sub1 sub2;
run;

proc freq data=merged2; 
tables flag*stratum0 flag*state0 flag*qtr0 flag*claim_type flag*type/list missing; run;

*test pending cases;
data pending;
set merged2;
if pending = 1;
run;
proc means data=pending nway noprint;
class program state qtr;
var pending;
output out=count_pending (drop=_type_ _freq_) sum=number_pending;
run;

ods listing close; 
	ods tagsets.ExcelXP file="&QCPath./3_Claim Merged QC File.xls"
		style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
	options(embedded_titles = 'yes' embedded_footnotes='yes');
	ods tagsets.Excelxp options(sheet_name="Merged check");
	Title "Lewin and Sample data Merged check";
	proc freq data=merged2; 
	tables flag*stratum0 flag*state0 flag*qtr0 flag*claim_type flag*type/list missing; run;
	%export_Summary(count_pending, "Number of pending claims by program, state, and quarter");
ods tagsets.ExcelXP close;
ods listing;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="mergedDataCleanUp", arguments=_arguments, sas_block=_sas_block)

def format_for_rolling_stack(input: Any = None, output: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %format_for_rolling_stack."""
    _arguments = {
        "input": input,
        "output": output,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """data &output.;
format MR_toe1 $100. dp_toe1 $100. mapped_subqualifier_code1 $750. unique_subqualifier_code1 $750.
	qtr0 $3. medicare_xover $16. Claim_Adj_Ind2 $4. type $4. processing_error_code_orig Processing_Error_Code $100. medical_review_error_code_orig Medical_Review_Error_Code $100.
	medical_review_reason_for_error $200. medical_review_reason_orig $200.  
    oversampleind $5. state0 $20. Claim_Identifier $50. ICN $50.
	Adjusted_ICN $50. processing_reason_orig $200. processing_reason_for_error_code $200.
	program $10. PERM_ID $13. Sampling_Level $15. clm_type_sam $75. adjustmentQualifier $50.
	CurrentPaymentStatus $23. SecondaryQualifiers $200. aplus_stratum $9. state_id $9. aplus_permid $15.
	OriginalPermID $15. MissingDocs $255.;

set &input.;
/*error_total_original2 			 = input(error_total_original,dollar21.);
medical_review_error_total_orig2 = input(medical_review_error_total_orig,dollar21.);
processing_error_total_original2 = input(processing_error_total_original,dollar21.);
total_lines2 					 = input(total_lines,8.);*/

adjusted_paid_date2 			 = adjusted_paid_date;

claim_adj_ind2 					 = claim_adj_ind ; 

changed_paid_amount2 			 = input(changed_paid_amount, best12.);
changed_paid_date2 				 = input(changed_paid_date, best12.) ; 
changed_payment_status2			 = input(changed_payment_status, best12.) ; 
changed_to_fixed2 				 = input(changed_to_fixed, best12.) ;
changed_to_xover2 				 = input(changed_to_xover, best12.) ; 
changed_sampunit2 				 = input(changed_sampunit, best12.) ; 
rev_changed2 					 = input(rev_changed, best12.) ; 
new_paid_amount2 				 = input(new_paid_amount,best12.);

drop /*error_total_original 
	processing_error_total_original 
	medical_review_error_total_orig total_lines */
	claim_adj_ind
	new_paid_date changed_paid_amount
	changed_paid_date 
	changed_payment_status 
	changed_to_fixed 
	changed_to_xover 
	changed_sampunit 
	rev_changed
	new_paid_amount; 
run;

data &output.;
format claim_adj_ind $4. ; 
set &output.;
claim_adj_ind = claim_adj_ind2 ; 
/*error_total_original = error_total_original2;
medical_review_error_total_orig = medical_review_error_total_orig2;
processing_error_total_original = processing_error_total_original2;
total_lines = total_lines2;*/

adjusted_paid_date = adjusted_paid_date2;

changed_paid_amount = changed_paid_amount2 ;
changed_paid_date = changed_paid_date2;
changed_payment_status = changed_payment_status;
changed_to_fixed= changed_to_fixed2 ;
changed_to_xover = changed_to_xover2 ;
changed_sampunit= changed_sampunit2; 
rev_changed = rev_changed2;
new_paid_amount = new_paid_amount2;

drop /*error_total_original2 
	processing_error_total_original2 
	medical_review_error_total_orig2 total_lines2*/
	adjusted_paid_date2
	claim_adj_ind2
	changed_paid_amount2
	changed_paid_date2 
	changed_payment_status2 
	changed_to_fixed2
	changed_to_xover2 
	changed_sampunit2
	rev_changed2
	new_paid_amount2;
run;"""
    return run_transpiled_macro(source_file="Claims Programs/Macros_MR_and_DP_Data_Cleaning.sas", macro_name="format_for_rolling_stack", arguments=_arguments, sas_block=_sas_block)

