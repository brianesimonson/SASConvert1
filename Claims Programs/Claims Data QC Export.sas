/*********************************************************************************

Macros QC checks and Export

**********************************************************************************/
options formdlim="*" compress=yes symbolgen mprint VALIDVARNAME=V7;
%let accept_diff = 0.01; 
proc datasets library=work;
delete qc_summaryQual qc_summary_TCQual; 
run; 
options dlcreatedir;
libname newdir "&mainpath./Claims Error Rates/Results/QC_Results_&sysdate.";
%let QCPath = &mainpath./Claims Error Rates/Results/QC_Results_&sysdate.; 

/************ QC for Sample Data ****************************/
%macro SampleData_Qc(type);
data check;
set sample_data2&type.;

if missing(amount_paid) then amount_paid = 0;
if missing(error_total) then error_total = 0;
if missing(overpayments) then overpayments = 0;
if missing(underpayments) then underpayments = 0;

if missing(Processing_Accuracy_Total) then Processing_Accuracy_Total = 0;
if missing(processing_error_total) then processing_error_total = 0;
if missing(processing_overpayment) then processing_overpayment = 0;
if missing(processing_underpayment) then processing_underpayment = 0;

if missing(Medical_Review_Error_Total) then Medical_Review_Error_Total = 0;
if missing(medical_review_overpayment) then medical_review_overpayment = 0;
if missing(medical_review_underpayment) then medical_review_underpayment = 0;

if missing(paid) then paid = 0;
if missing(gross_error) then gross_error = 0;
run;
proc sql; 
	select max(mr_toe_varnum) into: mr_toe_varnum
	from sample_data2&type.; 
	select max(dp_toe_varnum) into: dp_toe_varnum
	from sample_data2&type.; 
quit; 

*problem claims; 

* error total > amount paid;
data perm.error_gt_paid&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if error_total - paid> &accept_diff.; /* overpay > amount_paid */
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;
* overpayment > amount paid;
data perm.over_gt_paid&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if overpayments-amount_paid > &accept_diff.; /* overpay > amount_paid */
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

*if overpay + underpay NE error_total;
data perm.over_under_NE_error&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if sum(abs(overpayments),abs(underpayments)) - abs(error_total) > &accept_diff.;
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

*if data processing underpay + overpay NE processing error total;
data perm.dp_over_under_error&type.;
retain perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
set check;
if abs(sum(abs(processing_underpayment),abs(processing_overpayment)) - abs(processing_error_total)) > &accept_diff.;
keep perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

*if MR overpay+ underpay NE MR error total;
data perm.mr_over_under_error&type.;
retain perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
set check;
if abs(sum(abs(medical_review_underpayment),abs(medical_review_overpayment)) - abs(medical_review_error_total)) > &accept_diff.;
keep perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

*DP error + MR error NE error total (and not pending);
data perm.dp_mr_error&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if abs(sum(abs(processing_error_total),abs(medical_review_error_total)) - abs(error_total)) > &accept_diff.;
if upcase(processing_error_code1) NE "PENDING" and upcase(Medical_Review_Error_Code1) NE "PENDING";
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

* DP error NE MR error ... sometimes if they are the same it is being double counted so error total
	also equals DP error and MR error (not sum);
data perm.dp_mr_error2&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments;
set perm.dp_mr_error&type.;
if processing_error_total NE medical_review_error_total;
run;

*error total greater than amount paid;
data perm.errortot_gr_paid&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if error_total - amount_paid > &accept_diff.;
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
run;

data perm.pending&type.;
retain perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
set check;
if upcase(processing_error_code1) = "PENDING" or upcase(medical_review_error_code1) = "PENDING";
keep perm_ID processing_error_code1 Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments paid;
run;

data perm.dp_multerr_gt_errortot&type.;
retain perm_ID processing_error_total processing_error_code1-processing_error_code%eval(&dp_toe_varnum.) processing_error_total1-processing_error_total%eval(&dp_toe_varnum.) amount_paid error_Total;
set check;
%do i = 1 %to %eval(&dp_toe_varnum.);
	%if &i. = 1 %then %do;
	if processing_error_code1 ne "PENDING" and abs(processing_error_total1)-abs(processing_error_total)>&accept_diff. then flagx = 1;
	%end;
	%else %do;
	else if processing_error_code&i. not in (" ","DTD") and abs(processing_error_total&i.) - abs(processing_error_total) >&accept_diff. then flagx = 1;
	%end;
%end; 
if flagx = 1;
keep perm_ID processing_error_total processing_error_code1-processing_error_code%eval(&dp_toe_varnum.) processing_error_total1-processing_error_total%eval(&dp_toe_varnum.) amount_paid error_Total;
run;

data perm.mr_multerr_gt_errortot&type.;
retain perm_ID medical_review_error_total medical_review_error_code1-medical_review_error_code%eval(&mr_toe_varnum.) medical_review_error_total1-medical_review_error_total%eval(&mr_toe_varnum.) amount_paid error_Total;
set check;
%do j = 1 %to %eval(&mr_toe_varnum.);
	%if &j. = 1 %then %do;
	if medical_review_error_code1 ne "PENDING" and abs(medical_review_error_total1) - abs(medical_review_error_total)>&accept_diff. then flagx = 1;
	%end;
	%else %do;
	else if medical_review_error_code&j. not in (" ","MTD") and abs(medical_review_error_total&j.)-abs(medical_review_error_total)>&accept_diff. then flagx = 1;
	%end; 
%end; 

if flagx = 1;
keep perm_ID medical_review_error_total medical_review_error_code1-medical_review_error_code%eval(&mr_toe_varnum.) medical_review_error_total1-medical_review_error_total%eval(&mr_toe_varnum.) amount_paid error_Total;
run;

data perm.dp_multerr_underpay&type.;
retain perm_ID processing_underpayment processing_error_code1-processing_error_code%eval(&dp_toe_varnum.) processing_underpayment1-processing_underpayment%eval(&dp_toe_varnum.) amount_paid error_Total;
set check;
if processing_error_code1 not in ("PENDING","C1","N/A");
%do k = 1 %to %eval(&dp_toe_varnum.);
if abs(processing_underpayment) - abs(processing_underpayment&k.) >&accept_diff. and processing_underpayment&k. ne 0 then flagx = 1;
%end;

if flagx = 1;
keep perm_ID processing_underpayment processing_error_code1-processing_error_code%eval(&dp_toe_varnum.) processing_underpayment1-processing_underpayment%eval(&dp_toe_varnum.) amount_paid error_total;
run;

data perm.mr_multerr_underpay&type.;
retain perm_ID medical_review_underpayment medical_review_error_code1-medical_review_error_code%eval(&mr_toe_varnum.) medical_review_underpayment1-medical_review_underpayment%eval(&mr_toe_varnum.) amount_paid error_total;
set check;
if medical_review_error_code1 not in ("PENDING","N/A","C1");
%do l = 1 %to %eval(&mr_toe_varnum.);
if medical_review_underpayment&l. ne 0 and abs(medical_review_underpayment) -abs(medical_review_underpayment&l.)>&accept_diff. then flagx = 1;
%end;
if flagx = 1;
keep perm_ID medical_review_underpayment medical_review_error_code1-medical_review_error_code%eval(&mr_toe_varnum.) medical_review_underpayment1-medical_review_underpayment%eval(&mr_toe_varnum.) amount_paid error_total;
run;

data perm.missing_fmap_rates;
retain perm_ID paidfmaprate error_total overpayments underpayments paid;
set perm.sample_data1&type.;
if missing(paidfmaprate) then flagx = 1;
else if paidfmaprate < 1 then flagx =1;
if flagx = 1;
keep perm_ID paidFmaprate  error_total overpayments underpayments amount_paid_claim;
run; 

/* partial errors */ 

/* get max toe by review type */
proc means data = check noprint;
var mr_toe_varnum;
output out = max_toe_var (drop = _type_ _freq_) max=;
run;
data max_toe_var;
set max_toe_var;
call symput ("mr_toe_varnum", mr_toe_varnum);
run;

proc means data = check noprint;
var dp_toe_varnum;
output out = max_toe_var (drop = _type_ _freq_) max=;
run;
data max_toe_var;
set max_toe_var;
call symput ("DP_toe_varnum", dp_toe_varnum);
run;

%put &dp_toe_varnum;

data partial_mr;
run;
data partial_dp;
run;

%macro runme(type2,max,dataset,error_total,error_code,underpayment,overpayment);

%do i = 1 %to &max.;

/* partial errors */
data temp;
set &dataset.;
if program NE "None";
error_codex = &error_code.&i.;
error_totalx = &error_total.&i.;
underpaymentx = &underpayment.&i.;
overpaymentx = &overpayment.&i.;
if error_codex not in ("","PENDING","C1","MTD","DTD","N/A","ERTD1","ERTD2");
if abs(error_totalx-amount_paid)> .01;
keep perm_id program error_codex error_totalx underpaymentx overpaymentx amount_paid;
run;

data partial_&type2.;
retain perm_id program error_codex error_totalx underpaymentx overpaymentx amount_paid;
set partial_&type2. temp;
if not missing(perm_id);
run;
%end;

%mend runme;

%runme(dp,&dp_toe_varnum.,check,processing_error_total,processing_error_code,processing_underpayment,processing_overpayment);
%runme(mr,&mr_toe_varnum.,check,medical_review_error_total,medical_review_error_code,medical_review_underpayment,medical_review_overpayment);

data perm.partial_mr;
	set partial_mr;
run;

data perm.partial_dp;
	set partial_dp;
run;
proc datasets library=work;
delete qc_summary&type.Sample; 
run; 

ods listing close; 
ods tagsets.ExcelXP file="&QCPath./1_&error_type. Sample Data Problems&type..xls"
	style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
options(embedded_titles = 'yes' embedded_footnotes='yes');
%export_QC(import_merge, "Import &error_type. Data check",Sample);
%export_QC(pay_incorrect, "Check sample data error payment calculations",Sample);
%export_QC(perm.error_gt_paid&type., "MR+DP problem claims: error > amount paid",Sample);
%export_QC(perm.over_gt_paid&type., 'MR+DP problem claims: overpayment > amount paid',Sample);
%export_QC(perm.over_under_NE_error&type., 'MR+DP problem claims: overpay + underpay NE error_total',Sample);
%export_QC(perm.dp_over_under_error&type., 'DP problem claims: DP overpay + DP underpay NE DP error_total',Sample);
%export_QC(perm.mr_over_under_error&type., 'MR problem claims: MR overpay + MR underpay NE MRerror_total',Sample);
%export_QC(perm.dp_mr_error&type.,'DP+MR problem claims: DP error + MR error NE error_total',Sample);
%export_QC(perm.dp_mr_error2&type.,'DP+MR problem claims: DP error NE MR error',Sample);
%export_QC(perm.errortot_gr_paid&type., 'RC ER problem claims: error_total > amount paid',Sample);
/*%export_QC(perm.pending&type., 'RC ER problem claims: Pending claims',Sample);*/
/*%export_QC(perm.missing_fmap_rates, 'Claim problem claims: diff_fmap_rates',Sample);*/
%export_QC(perm.dp_multerr_gt_errortot&type., 'DP problem claims: MultiError Amt NE error_total',Sample);
%export_QC(perm.mr_multerr_gt_errortot&type., 'MR problem claims: MultiError Amt NE error_total',Sample);
%export_QC(perm.dp_multerr_underpay&type., 'DP problem claims: MultiError Underpay NE Underpay',Sample);
%export_QC(perm.mr_multerr_underpay&type., 'MR ER problem claims: MultiError Underpay NE Underpay',Sample);
/*%export_QC(perm.ertd1_paid&type., 'RC ER problem claims: Error code = ERTD1 and paid ne 0');
%export_QC(perm.missing_elgcat, 'RC ER problem claims: Missing eligibility_Category');
%export_QC(perm.missing_magi, 'RC ER problem claims: Missing magi state');
%export_QC(perm.missing_caseaction, 'RC ER problem claims: Missing case action');*/
%export_QC(perm.missing_fmap_rates, 'RC ER problem claims: Missing fmap rates',Sample);
%export_QC(perm.partial_mr, 'MR problem claims: Partial Error Check',Sample);
%export_QC(perm.partial_dp, 'DP problem claims: Partial Error Check',Sample);
%export_Summary(qc_summary&type.Sample, "&error_type. Sample Data Problems&type. Summary")
ods tagsets.ExcelXP close;
ods listing;

%mend; 


/************ QC for Final DP+MR Data ****************************/
%macro QC_Sample_data(type);
data perm.correct_with_error&type.;
retain perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
set perm.claim_sample_data&type.;
if drop_from_review NE 1;
if medical_review_error_code1 in ("C1","N/A","MTD") and 
	sum(medical_review_Overpayment,medical_review_underpayment,medical_review_error_total) > 0 then keep = 1;
if processing_error_code1 in ("C1","DTD") and 
	sum(processing_overpayment,processing_underpayment,processing_error_total) > 0 then keep = 1;
if medical_review_error_code1 in ("C1","N/A","MTD") and processing_error_code1 in ("C1","DTD")
	and sum(overpayments,underpayments,error_total) > 0 then keep = 1;
if keep = 1;
keep perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

data perm.incorrect_no_error&type.;
retain perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
set perm.claim_sample_data&type.;
if drop_from_review NE 1;
if medical_review_error_code1 not in ("C1","N/A","MTD","") and 
	sum(medical_review_Overpayment,medical_review_underpayment,medical_review_error_total) = 0 then keep = 1;
if processing_error_code1 not in ("C1","DTD","") and 
	sum(processing_overpayment,processing_underpayment,processing_error_total) = 0 then keep = 1;
if medical_review_error_code1 not in ("C1","N/A","MTD","") and processing_error_code1 not in ("C1","DTD","")
	and sum(overpayments,underpayments,error_total) = 0 then keep = 1;
if keep = 1;
keep perm_ID processing_error_code1 processing_underpayment processing_overpayment medical_review_overpayment
	medical_review_underpayment Medical_Review_Error_Code1 processing_error_total 
	medical_review_error_total error_total overpayments underpayments amount_paid;
run;

%mend; 

 
%macro Strata_PopQC;
***********************************************;
*test merged data to make sure there are claims in each universe strata;
*merge sample count from data and pop totals, output outcome;
data test;
format flag $10.;
merge sample_counts (in=inall) poptotals (in=intotals);
by strata;
count=1;
if inall and intotals then flag = "Both";
else if inall then flag = "In Sample";
else if intotals then flag = "In Total";
else flag = "None";
if m1 ne cnt_act_sampled_elg;
run;

data error.wt_test;
set test;
run;

proc means data=test nway;
class flag;
var count;
output out=error.Summary (drop=_freq_ _type_) sum=;
run;

data error.in_sample_only error.in_pop_only;
set test;
if flag = "In Sample" then output error.in_sample_only;
else if flag = "In Total" then output error.in_pop_only;
drop count flag;
run;
ods listing close; 
ods tagsets.ExcelXP file="&QCPath./Elig Sample and Population merge check.xls"
	style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
options(embedded_titles = 'yes' embedded_footnotes='yes');
%export_QC(error.summary, 'Sample & Population count check')
%export_QC(error.in_sample_only, 'Sample & Population - In Sample Only')
%export_QC(error.in_pop_only, 'Sample & Population - In Population Only')
%export_QC(error.wt_test, 'Sample & Population - Weight Test')
%export_QC(error.poptotal_duplicate, 'Population Duplicate Strata Check')
ods tagsets.ExcelXP close;
ods listing;
%mend;
