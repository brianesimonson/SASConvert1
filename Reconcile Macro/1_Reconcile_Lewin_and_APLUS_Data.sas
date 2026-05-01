*Reconcile claims sample with sample count;

/*Macro to clean up Lewin Data - Used in following procedure*/
%macro manual_lewindata_change(inputdata,outdata); 
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
/*run;*/

%mend manual_lewindata_change;

/* BEGIN RECONCILIATION */
data aplus;
format amount_paid paid original_amount dollar21.2 merge_permid $11.;
set perm.aplus;

/* change names of some variables for merge */
	aplus_permid = perm_id;	
	merge_permid = trim(perm_ID); /* CC: use latest perm id for merges to Lewin Data */

	* Define claim type;
	if substr(perm_id,8,1) = "F" or substr(perm_id,8,1) = "P" then claim_type="FFS";
	else if substr(perm_id,8,1) = "M" then claim_type="MC ";

/*checked with CERA - no need to create reporting_universe here*/
* define aplus universe;
	if program = "CHIP" and claim_type = "FFS" then reporting_universe = "SF";
	else if program = "CHIP" and claim_type = "MC" then reporting_universe = "SM";
	else if program = "Medicaid" and claim_type = "FFS" then reporting_universe = "MF";
	else if program = "Medicaid" and claim_type = "MC" then reporting_universe = "MM";

drop perm_id;
run;

proc sort data=aplus;
by merge_permid;
run;

data duplicate_aplus; /* make sure this is empty so permids are unique */
retain merge_permid	program	state	claim_type	quarter	aplus_stratum;
set aplus;
by merge_permid;
if first.merge_permid NE last.merge_permid;
keep merge_permid	program	state	claim_type	quarter	aplus_stratum;
run;
proc sql;
	select count(*) into: numobs
	from duplicate_aplus
	; 
quit; 
%PrintMessage("Action Needed if >0: RC data has &numobs. observations with Duplicate PERM ID");

/* check to see if there are variables named the same in Lewin vs CNI data */
proc contents data=check.&lewin_final_data. out=lewin_var (keep = name type length label format);
run;
data lewin_var; set lewin_var; name = upcase(name);run;
proc sort; by name; run;
proc contents data=aplus out=cni_var (keep = name type length label format);
run;
data cni_var; set cni_var; name = upcase(name);run;
proc sort; by name; run;

data duplicate_var;
merge lewin_var (in=inlew) cni_var (in=incni);
by name;
if inlew and incni;
if name NE "STRATUM" and name NE "STATE" AND NAME NE "REPORTING_UNIVERSE";
run;
%let duplicateVars=;
proc sql; 
	select name into: duplicateVars separated by ','
	from duplicate_var; 
	select count(*) into: numvars
	from duplicate_var; 
quit; 
%PrintMessage("Action Needed if >0: RC data and Lewin data has &numvars. variables with same name. Variables are &duplicateVars.");

/* lewin data */
%manual_lewindata_change(check.&Lewin_Final_Data.,lewin_temp3); 

proc sort; by lewin_permid; run;


data lewin;
format merge_permid $11.;
set lewin_temp3;
merge_permid = final_perm_id; /* CC: use latest perm id to merge Lewin and RC data */
run;

proc sort data=lewin;
by merge_permid;
run;
data duplicate_lewin; /* make sure this is empty so permids are unique */
retain merge_permid state0 qtr0 sampling_universe stratum0;
set lewin;
by merge_permid;
if first.merge_permid NE last.merge_permid;
keep merge_permid state0 qtr0 sampling_universe stratum0;
run;
proc sql;
	select count(*) into: numobs
	from duplicate_lewin
	; 
quit; 
%PrintMessage("Action Needed if >0: Lewin data has &numobs. observations with Duplicate PERM ID");

data merged;
merge lewin(in=inlewin) aplus(in=inaplus);
by merge_permid; /* this is merging by lewin perm id */
if inaplus and inlewin then flag = "both        ";
else if inaplus then flag = "aplus";
else if inlewin then flag = "lewin";
else flag = "prob";
count = 1;
run;
proc freq data=merged;
tables flag;
run;

/* dummy check to make sure variables match , dataset should be empty */
data basic_check;
set merged;
if flag = "both";
if state NE state0 or quarter NE qtr0;
keep merge_permid state state0 Quarter qtr0; 
run;

/* export some problem datasets */
data lewin_only;
retain merge_permid state0 qtr0;
set merged;
if flag = "lewin";
keep merge_permid state0 qtr0 stratum0 sampling_universe reporting_universe; 
run;
data aplus_only;
retain merge_permid program state claim_type quarter ;
set merged;
if flag = "aplus";
keep merge_permid program claim_type state quarter aplus_stratum reporting_universe;
run;

data permid_change;
retain merge_permid lewin_permid aplus_permid program state claim_type quarter ;
set merged;
if flag = "both";
if merge_permid NE lewin_permid or merge_permid NE aplus_permid;
keep merge_permid lewin_permid aplus_permid program claim_type state quarter aplus_stratum sampling_universe reporting_universe;
run;

data paid_nomatch;
retain merge_permid program state claim_type sampling_universe reporting_universe quarter final_PayStatus sampling_level0;
set merged;
if flag = "both";
if abs(final_paidamt - amount_paid) > 0;
if abs(final_PaidAmt - amount_paid) >= .01 then flag_diff_ge_01 = 1;
else flag_diff_ge_01 = 0;

keep merge_permid program claim_type state quarter sampling_universe reporting_universe 
	final_paidamt amount_paid flag_diff_ge_01 final_PayStatus sampling_level0 Claim_Adj_Ind;
run;

data paidorig_nomatch;
retain merge_permid program state claim_type sampling_universe reporting_universe quarter final_PayStatus sampling_level0;
set merged;
if flag = "both";
if abs(final_paidamt - original_amount) > 0;
if abs(final_PaidAmt - original_amount) >= .01 then flag_diff_ge_01 = 1;
else flag_diff_ge_01 = 0;
keep merge_permid program claim_type state quarter sampling_universe reporting_universe 
	final_paidamt original_amount flag_diff_ge_01 final_PayStatus sampling_level0;
run;

data paiddt_nomatch;
retain merge_permid program state claim_type sampling_universe reporting_universe quarter final_PayStatus sampling_level0;
set merged;
if flag = "both";
/*if date_of_payment NE date_paid;*/
if date_of_payment NE date_paid;
keep merge_permid program claim_type state quarter sampling_universe reporting_universe 
	date_of_payment date_paid final_PayStatus sampling_level0 Claim_Adj_Ind;
run;

data universe_nomatch;
retain merge_permid program state claim_type quarter;
set merged;
if flag = "both";
if sampling_universe NE reporting_universe;
if sampling_universe in ("MP","MF") and reporting_universe in ("MP","MF") then drop = 1;
if drop NE 1;
keep merge_permid program claim_type state quarter sampling_universe reporting_universe;
run;

data medicare_xover_missing;
retain merge_permid program state claim_type quarter;
set merged;
if flag = "both";
if claim_type NE "MC"; /* Managed care cannot have xover */
if missing(medicare_xover) or missing(final_xOverInd);
keep merge_permid program claim_type state quarter medicare_xover final_xoverind sampling_universe reporting_universe;
run;

data medicare_xover_nomatch;
retain merge_permid program state claim_type quarter;
set merged;
if flag = "both";
if claim_type NE "MC"; /* Managed care cannot have xover */
if medicare_xover NE final_xOverInd;
keep merge_permid program claim_type state quarter medicare_xover final_xoverind sampling_universe reporting_universe;
run;

data permid_univ_nomatch;
retain merge_permid lewin_permid aplus_permid program sampling_universe reporting_universe;
set merged;
if flag = "both";
if substr(aplus_permid,3,1) = "M" and program = "CHIP" or substr(aplus_permid,3,1) = "C" and program = "Medicaid";
keep merge_permid lewin_permid aplus_permid claim_type program sampling_universe reporting_universe;
run;

***************************************;
/* give counts of problems by state sampling univ, reporting univ, and quarter */
/* perm id count */
data count_uniquepermid;
set merged;
if flag = "both" then do;
	lewin = 1;
	aplus = 1;
end;
else if flag = "lewin" then lewin = 1;
else if flag = "aplus" then aplus = 1;

/* for claims that are in lewin data but are not in aplus */
if flag = "lewin" and missing(state) then do;
	state = state0;
	quarter = qtr0;
	end;
run;

proc means data=count_uniquepermid nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var lewin aplus;
output out=count_uniquepermid (drop = _type_ _freq_) sum=;
run;

data count_uniquepermid;
set count_uniquepermid;
if missing(lewin) then lewin = 0;
if missing(aplus) then aplus = 0;
run;

/* paid amount not matching count */
data count_diff_paidamt;
set paid_nomatch;
if flag_diff_ge_01 NE 1 then flag_diff_l_01 = 1;
run;

proc means data=count_diff_paidamt nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var flag_diff_ge_01 flag_diff_l_01;
output out=count_diff_paidamt (drop = _type_ _freq_) sum=;
run;


/* difference in paid date count */
data count_diff_paiddt;
set paiddt_nomatch;
count = 1;
run;

proc means data=count_diff_paiddt nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var count;
output out=count_diff_paiddt (drop = _type_ _freq_) sum=;
run;

/* difference in reporting universe */
data count_diff_universe;
set universe_nomatch;
count = 1;
run;
proc means data=count_diff_universe nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var count;
output out=count_diff_universe (drop = _type_ _freq_) sum=;
run;


/* missing medicare xover */
data count_xover_missing;
set medicare_xover_missing;
count = 1;
run;
proc means data=count_xover_missing nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var count;
output out=count_xover_missing (drop = _type_ _freq_) sum=;
run;

/* difference in medicare xover */
data count_diff_xover;
set medicare_xover_nomatch;
count = 1;
run;
proc means data=count_diff_xover nway noprint;
class state sampling_universe reporting_universe quarter / missing;
var count;
output out=count_diff_xover (drop = _type_ _freq_) sum=;
run;
proc datasets library=work;
delete qc_summary_TCRECON; 
run; 
ods listing close; 
ods tagsets.ExcelXP file="&QCPath./2_&error_type. Reconciliation Problem Details.xls"
	style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
options(embedded_titles = 'yes' embedded_footnotes='yes');
%export_QC(basic_check,"check state and quarter should match between Lewin and RC data",RECON)
%export_QC(duplicate_var,"check any duplicate variables in Lewin and RC data",RECON)
%export_QC(duplicate_aplus,"Check any duplicate PERMID in RC data",RECON)
%export_QC(duplicate_lewin,"Check any duplicate PERMID in Lewin data",RECON)
%export_QC(lewin_only,"Merge RC+Lewin check - Lewin data only",RECON)
%export_QC(aplus_only,"Merge RC+Lewin check - RC data only",RECON)
%export_QC(permid_change,"Merge RC+Lewin check - PERMID Change",RECON)
%export_QC(paid_nomatch,"Final Paid Amt and Amt Paid nonmatch",RECON)
%export_QC(paidorig_nomatch,"Final Paid Amt and Original Amt Paid nonmatch",RECON)
%export_QC(paiddt_nomatch,"Paid date nonmatch",RECON)
%export_QC(universe_nomatch,"Sampling and reporting universe nonmatch",RECON)
%export_QC(medicare_xover_missing,"Missing Medicare xover indicators",RECON)
%export_QC(medicare_xover_nomatch,"Medicare xover indicators nonmatch",RECON)
%export_QC(permid_univ_nomatch,"PermID and program indicators nonmatch",RECON)
ods tagsets.ExcelXP close;
ods listing;

ods listing close; 
ods tagsets.ExcelXP file="&QCPath./2_&error_type. Reconciliation Problem Summary.xls"
	style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
options(embedded_titles = 'yes' embedded_footnotes='yes');
%export_Summary(qc_summary_TCRECON,"Reconciliation Problem Summary - See details in the Reconciliation Problem Details");
%export_Summary(count_uniquepermid, "Count Unique PERMID by universe type and qtr");
%export_Summary(count_diff_paidamt, "Nonmatch paidamt by universe type and qtr");
%export_Summary(count_diff_paiddt, "Nonmatch paid date by universe type and qtr");
%export_Summary(count_diff_universe, "Nonmatch universe by universe type and qtr");
%export_Summary(count_xover_missing, "Missing Medicare xover by universe type and qtr");
%export_Summary(count_diff_xover, "Nonmatch Medicare xover by universe type and qtr");
ods tagsets.ExcelXP close;
ods listing;































