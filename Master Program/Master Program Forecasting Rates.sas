
*------------------------------------
Programmers  : Qitong Guo
Date created : 01.03.2014
Date edited  : 01.17.2025
Last progrmr : Janice Lin
Purpose      : RY2026 Master Program to run all Forecast rates
*------------------------------------;

/* import parameter list from CSV file */

/* UPDATE THE FOLLOWING VARIABLES IN THE PARAMETER CSV !!!!! */

/* 
	Aplus_Final_Data
	Aplus_Final_Data_Sheet
	Pop_Data
	previous_run_folder
	datacut_month
*/

DM LOG 'CLEAR';
DM OUT 'CLEAR';

OPTIONS MPRINT MLOGIC validvarname=v7;

/* import parameter list from CSV file */
%let masteryear=RY2026;
%let log_file = /sas_data_cms/Project/PERM/Statistical Reporting/&masteryear./Master Program/Logs;
%include "/sas_data_cms/Project/PERM/Statistical Reporting/&masteryear./Master Program/Parameter List.sas" /source2;

/* create a new macro variable */
%macro macro_var(var,value);
%global &var;
%let &var=&value;
/*%syslput &var=&value;*/
%mend;

/* STEP 1: Change all parameters in the CSV to make sure they are up to date */
/* STEP 2: BACKUP the data and results folders in Claims, Claims forecasting, Rolling, Rolling forecasting, 
			and interim error rates forecasting folders */
/* STEP 3: go through Claims cleaning step by step first, then check outputs before
			proceeeding */


/************************* Claims Error Rates CLEANING *************************/
/* import A+ claims data, merge with Lewin data */
/* edits to qualifiers */
/* data cleaning and calculation (17 state project to national) */
/* Note/sas_data_cms Update Manual changes program for any specific updates */
%include "&masterpath./Claims Error Rates/Programs/Step 1 - Reconcile and Import Data.sas" /source2; 
%include "&masterpath./Claims Error Rates/Programs/Step 2 - Calculate claims error rate SE by state.sas" /source2; 
%include "&masterpath./Claims Error Rates/Programs/Step 3 - Data Completeness Check.sas" /source2;

/************************* Eligibility Error Rates *****************************/
/* Note/sas_data_cms Update Manual changes program for any specific updates */
%include "&masterpath./Eligibility Error Rates/Programs/Step 1 - Reconcile and Import Data.sas" /source2; 
%include "&masterpath./Eligibility Error Rates/Programs/Step 2 - Calculate Eligibility Error Rate SE by state.sas" /source2; 
%include "&masterpath./Eligibility Error Rates/Programs/Step 3 - Create State Level Dataset wo Unwinding.sas" /source2; 

/************************* Rolling Rates DATA *************************/
proc printto log="&log_file./Rolling Rates Log &sysdate..txt" new; run; 
%include "&masterpath./Rolling Rates/Programs/01 Three Year Rolling Dataset with Sweight2--New Rolling.sas"/source2;
%macro_var(program, Medicaid);
%macro_var(typeroll, );
%include "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas" /source2;
%macro_var(program, Medicaid);
%macro_var(typeroll,d);
%include "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas" /source2;
%macro_var(program, CHIP);
%macro_var(typeroll, );
%include "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas" /source2;
%macro_var(program, CHIP);
%macro_var(typeroll,d);
%include "&masterpath./Rolling Rates/Programs/02 Calculating Rolling Rates--NEW method.sas" /source2;
%include "&masterpath./Rolling Rates/Programs/07 Calculate 17 State Cycle Error Rate.sas" /source2;
proc printto;
run;


/************************* Rolling Rates DATA -- CC added 6/16/2025 *************************/
proc printto log="&log_file./Rolling Rates No Unwinding Log &sysdate..txt" new; run; 
%include "&masterpath./Rolling Rates/Programs/08 Three Year Rolling Dataset with Sweight2--New Rolling - No Unwinding.sas"/source2;

/* additional runs including non-dynamic data are not needed for no Unwinding, since we're using
	the dynamic datasets from the previous 2 cycles */
%macro_var(program, Medicaid); 
%macro_var(typeroll,d);
%include "&masterpath./Rolling Rates/Programs/09 Calculating Rolling Rates--NEW method - No Unwinding.sas" /source2;

%macro_var(program, CHIP);
%macro_var(typeroll,d);
%include "&masterpath./Rolling Rates/Programs/09 Calculating Rolling Rates--NEW method - No Unwinding.sas" /source2;
%include "&masterpath./Rolling Rates/Programs/10 Calculate 17 State Cycle Error Rate - No Unwinding.sas" /source2;
proc printto;
run;




/************************* Overall Error Rates *************************/
proc printto log="&log_file./Overall - Overall Error Rates Log &sysdate..txt" new; run; 
%macro_var(program,Medicaid);
%include "&masterpath./Overall Error Rates/Programs/Step 01 PERM Overall Error Rate and SE Calculator.sas" /source2;
%macro_var(program,CHIP);
%include "&masterpath./Overall Error Rates/Programs/Step 01 PERM Overall Error Rate and SE Calculator.sas" /source2;
/*step 02, sample sizes*/
%include "&masterpath./Overall Error Rates/Programs/Step 02 Sample Size Run.sas" /source2;

proc printto;
run;


/************************* Interim Rates FORECASTING *************************/
proc printto log="&log_file./Interim Error Rates Forecasting Log &sysdate..txt" new; run; 
%include "&masterpath./Interim Error Rates Forecasting/Programs/01 Estimate Rolling Rates.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/02 Estimate Cycle Rates.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/03 Export Rolling and Cycle Forecast Rates.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/04 DP and MR Error Summary.sas"/source2; 
%include "&masterpath./Interim Error Rates Forecasting/Programs/04.1 Subqualifier Summary.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/05 Cycle and Rolling Qualifier List.sas"/source2; 
/*%include "&masterpath./Interim Error Rates Forecasting/Programs/06 Small Key Tables.sas"/source2; JL - No longer Needed*/
%include "&masterpath./Interim Error Rates Forecasting/Programs/07 Cycle Forecast Trends.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/07.3 ELG Forecast Trends.sas"/source2; /* CS Re-Ordered for Update to Cycle Forecast */
%include "&masterpath./Interim Error Rates Forecasting/Programs/07.1 Cycle Overall Forecast Trends.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/07.2 Rolling Overall Forecast Trends.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/08 Claims Reviewed Progress.sas"/source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/09 Top 100 MR1 and MR2 Errors.sas" /source2;
%include "&masterpath./Interim Error Rates Forecasting/Programs/10 Weight Test for Accuracy Reviews v2.sas" /source2;
proc printto;
run;


/************************* ELG Key Tables *************************/
proc printto log="&log_file./Elig Key Tables &sysdate..txt" new; run; 
%include "&masterpath./Overall Error Rates/Programs/ELG Key Tables/Key Tables ELG Master Program.sas" /source2;
proc printto;
run;


/************************* CLM Key Tables *************************/
proc printto log="&log_file./CLM Key Tables &sysdate..txt" new; run; 
%include "&masterpath./Overall Error Rates/Programs/CLM Key Tables/Key Tables CLM Master Program.sas" /source2;
proc printto;
run;


/************************* Key Tables *************************/
proc printto log="&log_file./Key Tables &sysdate..txt" new; run; 
%include "&masterpath./Overall Error Rates/Programs/Key Tables/00 Key Tables Master Program - New.sas" /source2;
proc printto;
run;

/************************* Key Tables Comparison *************************/
proc printto log="&log_file./Key Tables Comparison &sysdate..txt" new; run;
%include "&masterpath./Overall Error Rates/Programs/Key Tables Comparison/PERM Qualifier Cycle Compare.sas" /source2;
proc printto;
run;

/************************* Key Tables - No Unwinding *************************/
proc printto log = "&masterpath./Master Program/Logs/Master Program Logs &sysdate. - Key Tables - No Unwinding.txt" new; run;
	%include "&masterpath./Overall Error Rates/Programs/Key Tables - No Unwinding/00 Key Tables Master Program - New.sas" /source2;
proc printto; run;


proc printto log = "&masterpath./Master Program/Logs/Master Program Logs &sysdate. - ELG Key Tables - No Unwinding.txt" new; run;
	%include "&masterpath./Overall Error Rates/Programs/ELG Key Tables - No Unwinding/Key Tables ELG Master Program.sas" /source2;
proc printto; run;

/************************* Administrative: File Backups *************************/
*%include "&masterpath./Master Program/Automated Forecasting Rates Backup V2.sas"/source2;






