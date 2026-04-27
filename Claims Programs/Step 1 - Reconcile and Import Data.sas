*Reconcile claims sample with sample count;


options formdlim="*" compress=yes symbolgen mprint mlogic notes nosource;
/* The parameter list is created in Master Program fron Parameter List csv
--------------------------------------------------------------------------
%let permyear = RY2019;
%let prev = FY2017;
%let RC_MR_Data = RY19 MR Findings 05-08-2019;
%let RC_MR_Data_Range = Sheet1$A6:Q20000;
%let RC_DP_Data = RY19 DP Findings 05-08-2019; 
%let RC_DP_Data_Range = Sheet1$A6:Q20000;
%let RC_Final_Data = RY19 Claims Master File 05-08-2019;
%let RC_Final_Data_Range = Sheet1$A6:Q20000 ;
%let Lewin_Final_Data = final_comparison4ccv2;
%let rc_elig_data = Eligibility Reconciliation Master File_Run_ID_37;
%let rc_elig_data_range = Sheet1$A6:AP20000;
%let pop_data = ry21universesamplecnt20201221; 
--------------------------------------------------------------------------
*/

/*---------------Define folder path--------------------------------------------------------------*/
%let mainpath = /sas_data_cms/Project/PERM/Statistical Reporting/&permyear.;
%let data_path    = &mainpath./Rawdata/Rawdata;
%let error_type = Claim;

libname perm "&mainpath./Claims Error Rates/Data";
libname check "&mainpath./Rawdata/Rawdata";
libname qualcode "&mainpath./Extra/Qualifier Coding";
libname subqual "&mainpath./Extra/Subqualifier Coding";
libname previous "/sas_data_cms/Project/PERM/Statistical Reporting/&prev./Claims Error Rates/Data";

%include "&mainpath./Claims Error Rates/Programs/Manual Change for Claims Data Cleaning.sas" /source2;
%include "&mainpath./Claims Error Rates/Programs/Macros_MR_and_DP_Data_Cleaning.sas" /source2;
%include "&mainpath./Claims Error Rates/Programs/Claims Data QC Export.sas" /source2;
%let log_folder = &QCpath.;
%let log_file_cv = Step 1 - &error_type. Reconcile and import data &sysdate..txt;

*Global Macro - ;
%include "&mainpath./Extra/Type of Error Mapping/Assign TOE Label.sas" /source2; *Type of error; 
%include "&mainpath./Global Macros/Reconcile Macro/0_Qualifier_Mapping.sas"/source2; *Qualifier Mapping; 
%include "&mainpath./Global Macros/Reconcile Macro/2_CompareVarType.sas"/source2; *Compare with previous year file and change vartype if necessary; 
%include "&mainpath./Global Macros/Reconcile Macro/3_Population_Data_SetUp.sas"/source2; *Import population data; 
%include "&mainpath./Global Macros/Reconcile Macro/4_ExportQC.sas"/source2;
%include "&mainpath./Global Macros/Reconcile Macro/PrintMessage_Macro.sas"/source2;
/*--------------------------------------------------------------------------------------------------*/
proc printto; run; 
proc printto log = "&log_folder./&log_file_cv" new;
quit;
/*****************************************************
****** Create qualifier mapping for MR and DP ********
*****************************************************/
%PrintMessage("Import qualifier mapping");
data dp_map;
format qualifier $200.;
set qualcode.dp_qualifier_code_map;
code = processing_error_code;
qualifier = processing_reason_for_error_code;
unique_qualcode = processing_unique_qualcode;
mapped_qualcode = processing_mapped_qualcode;
keep code qualifier unique_qualcode mapped_qualcode;
run;

data mr_map;
format qualifier $200.;
set qualcode.mr_qualifier_code_map;
code = medical_review_error_code;
qualifier = medical_review_reason_for_error;
unique_qualcode = medical_review_unique_qualcode;
mapped_qualcode = medical_review_mapped_qualcode;
keep code qualifier unique_qualcode mapped_qualcode;
run;

data map;
set mr_map dp_map;
proc sort ; by code qualifier;
run;

/*****************************************************
********** Import data and data cleaning ************
*****************************************************/
/* %let type = ;
%let type = _TC; */
%macro getSampleData(type); 
	%PrintMessage("Import Data and perform data cleaning &type.");
	* Step 1: a)Import RC MR data, b)modify error payment variables based on type,
			  c) create qualifier mapping, d) Assig type of error based on error code,
			  e)transpose data from long to wide ;
	%import_mr(&type.);
	* Step 2: a)Import RC MR data, b)modify error payment variables based on type,
			  c)create qualifier & subqualifier mapping, d) Assig type of error based on error code,
			  e)transpose data from long to wide ;
	%import_dp(&type.);
	*Step 3: Export qualifier mapping QC;
	%qualifier_subqual_check_export;


	/*Step 4: import APLUS data (Full_Data), with output dataset, Export QC checks 1)import_merge check with DP & MR file,
				2) payincorrect check */
	%import_data(perm.sample_data1&type., &type.);
	
	/*Step 5: reformat certain variables*/
	%format_variables(perm.sample_data1&type.,sample_data1,sample_data2); /* dataset names */

	/* dataset called sample_data2 (including variable fixes) is going to be used here */
	/*make manual changes to A+ data early in import process*/
	data sample_data2&type.;
		set sample_data2;
		%manual_data_change;
	run;

	/* BEGIN RECONCILIATION */
	/*--------------RECONCILIATION: using _TC (Only need to run once)--------------*/
	%PrintMessage("BEGIN RECONCILIATION");
	%if &type. = _TC %then %do;
		data perm.aplus; 
			set sample_data2&type.; 
		run; 
		%let status = RECON; 
		%include "&masterpath./Global Macros/Reconcile Macro/1_Reconcile_Lewin_and_APLUS_Data.sas" /source2; 
	%end;
	/*------------Sample Data QC ---------------------------*/
	%PrintMessage("END RECONCILIATION");
	%PrintMessage("Sample Data QC");
	%SampleData_Qc(&type.);
	
	/*------------Reconciliation Merge  ---------------------------*/
	*Lewin data clean-up and format;
	%PrintMessage("Reconciliation Merge &type.");
	%let status = CLEAN; 
	%manual_lewindata_change(check.&Lewin_Final_Data., lewindata);
	
	*mergedDataCleanUp: perfrom data cleaning for merged data (APLUS - sample & Lewin data)
		indata - Lewindata, sample_data2&type.
		outdata - merged2; 
	%mergedDataCleanUp;

	/*------------Format variables for rolling stack  ---------------------------*/
	%PrintMessage("Format variables for rolling stack &type.");
	* if there is any other variables that we did not format and does not match previous
	  year data - it will format it at here;
	%checkVarType(pre_data=claim_sample_data&type.,
				  cur_data=Merged2,
				  outdata =claim_sample_data_dpmr1&type.);
/*	%format_for_rolling_stack(claim_sample_data_dpmr1&type.,claim_sample_data_dpmr2&type.);*/
	* Saved the final formatted data;
	data perm.claim_sample_data&type.;
	set claim_sample_data_dpmr1&type.;
	run;
	/*------------Final Sample data QC check ---------------------------------------*/
	%QC_Sample_data(&type.);
	
	proc datasets library=work;
	delete qc_summary&type.Final; 
	run; 
	ods listing close; 
	ods tagsets.ExcelXP file="&QCPath./4_Final Claim QC Summary&type..xls"
		style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
	options(embedded_titles = 'yes' embedded_footnotes='yes');
	%export_QC(perm.correct_with_error&type., 'Final Sample Data Check - check any no error claim has error $',Final);
	%export_QC(perm.incorrect_no_error&type., 'Final Sample Data Check - check any error claim has error $0',Final);
	%export_QC(nonmatch_variables, "&masteryear.-Nonmatching variables Comp previous year",Final);
	%export_QC(nonmatch_vartype, "&masteryear.-Nonmatching vartype Comp previous year",Final);
	%export_Summary(qc_summary&type.Final, "Final Sample Data Check Summary");
	ods tagsets.ExcelXP close;
	ods listing; 
	
%mend;
%getSampleData(_TC);
%getSampleData();

/*----------------------------------------------
--------------Population Data ------------------
-----------------------------------------------*/
%PrintMessage("Population Data");
data pop_totals_temp;
set check.&Pop_Data.;
drop program_type;
run;
/* Any manual changes to the population data */
%pop_totals_manual_change(indata=pop_totals_temp, outdata=pop_totals_temp);
/* Run cleaning program */
%popDataClean(indata=pop_totals_temp, outdata=perm.claim_pop_totals);

%PrintMessage("Claims data QC Files Exporting....");
%PrintMessage("0_Qualifier Check");
%PrintMessage("1_Claim Sample Data Problems - QC Checks");
%PrintMessage("2_RECONCILIATION QC Files");
%PrintMessage("3_Claim Merged QC File - Merged w. Lewin Data");
%PrintMessage("4_Final Claim QC Summary - Final Claim Data QC");
%PrintMessage("5_Population Data QC");

proc printto; run; 






















