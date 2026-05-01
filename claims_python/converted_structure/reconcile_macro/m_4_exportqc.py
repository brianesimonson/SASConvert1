"""Auto-generated SAS->Python structural conversion module.

Source: Reconcile Macro/4_ExportQC.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def export_qc(sheetname: Any = None, qc_check_notes: Any = None, metrics: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %export_QC."""
    _arguments = {
        "sheetname": sheetname,
        "QC_Check_Notes": qc_check_notes,
        "metrics": metrics,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ 
	*create summary table;
	proc sql; 
		create table qc_check as
		select &QC_Check_Notes. as QC_check length=200, 
			count(*) as number_of_records,
			"&sheetname." as QC_Sheet length=100/*,
			"&filename." as QC_File length=100*/
		from &sheetname.
	quit; 
	
	proc append base=qc_summary&type.&metrics. data=qc_check force; run; 

	ods tagsets.Excelxp options(sheet_name="&sheetname.");
	Title &QC_Check_Notes.;
	proc print data= &sheetname. noobs; run; 
	 """
    return run_transpiled_macro(source_file="Reconcile Macro/4_ExportQC.sas", macro_name="export_QC", arguments=_arguments, sas_block=_sas_block)

def export_summary(sheetname: Any = None, qc_check_notes: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %export_Summary."""
    _arguments = {
        "sheetname": sheetname,
        "QC_Check_Notes": qc_check_notes,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """ 

	ods tagsets.Excelxp options(sheet_name="&sheetname.");
	Title &QC_Check_Notes.;
	proc print data= &sheetname. noobs; run; 
	"""
    return run_transpiled_macro(source_file="Reconcile Macro/4_ExportQC.sas", macro_name="export_Summary", arguments=_arguments, sas_block=_sas_block)

def dataclean_exp(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %DataClean_Exp."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """	%if &error_type = Claim %then %do; 
		%let File_type = Claims; 
	%end; 
	%else %do; 
		%let File_type = Eligibility; 
	%end; 
	data summary; 
		set qc_summaryQual(in=a)
			qc_summary_TCSample(in=b)
			qc_summarySample(in=c)
			qc_summary_TCRECON(in=d)
			qc_summary_TCFinal(in=e)
			qc_summaryFinal(in=f)
			qc_summary_TCError(in=g)
			qc_summaryError(in=h)
		%if &error_type = Claim %then %do;
			qc_summaryMaster
		%end;
		;
		length TC $1. Key $200.;
		if b or e or g then TC = "1"; else TC = "";  
		Key = strip(strip(QC_Sheet)||TC);
	run; 

	%sysexec copy "&mainpath./Global Macros/Reconcile Macro/&file_type. Data QC Summary - TEMPLATE.xlsx" 
				  "&mainpath./&file_type. Error Rates/Results/&file_type. Data QC Summary &sysdate..xlsx" ;

	proc export data = summary
				outfile = "&mainpath./&file_type. Error Rates/Results/&file_type. Data QC Summary &sysdate..xlsx" 
	 			dbms = xlsx REPLACE; 
				sheet = "QC summary" ; 
	run;"""
    return run_transpiled_macro(source_file="Reconcile Macro/4_ExportQC.sas", macro_name="DataClean_Exp", arguments=_arguments, sas_block=_sas_block)

