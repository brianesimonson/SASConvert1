"""Auto-generated SAS->Python structural conversion module.

Source: Claims Programs/Step 1 - Reconcile and Import Data.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

INCLUDES = [
    "&mainpath./Claims Error Rates/Programs/Manual Change for Claims Data Cleaning.sas",
    "&mainpath./Claims Error Rates/Programs/Macros_MR_and_DP_Data_Cleaning.sas",
    "&mainpath./Claims Error Rates/Programs/Claims Data QC Export.sas",
    "&mainpath./Extra/Type of Error Mapping/Assign TOE Label.sas",
    "&mainpath./Global Macros/Reconcile Macro/0_Qualifier_Mapping.sas",
    "&mainpath./Global Macros/Reconcile Macro/2_CompareVarType.sas",
    "&mainpath./Global Macros/Reconcile Macro/3_Population_Data_SetUp.sas",
    "&mainpath./Global Macros/Reconcile Macro/4_ExportQC.sas",
    "&mainpath./Global Macros/Reconcile Macro/PrintMessage_Macro.sas",
    "&masterpath./Global Macros/Reconcile Macro/1_Reconcile_Lewin_and_APLUS_Data.sas",
]

def getsampledata(type: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %getSampleData."""
    _arguments = {
        "type": type,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ 
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
	"""
    return run_transpiled_macro(source_file="Claims Programs/Step 1 - Reconcile and Import Data.sas", macro_name="getSampleData", arguments=_arguments, sas_block=_sas_block)

