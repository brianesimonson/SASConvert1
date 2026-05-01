
/* Macro for general export */
%macro export_QC(sheetname, QC_Check_Notes,metrics); 
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
	 
%mend;
%macro export_Summary(sheetname, QC_Check_Notes); 

	ods tagsets.Excelxp options(sheet_name="&sheetname.");
	Title &QC_Check_Notes.;
	proc print data= &sheetname. noobs; run; 
	
%mend;

%macro DataClean_Exp;
	%if &error_type = Claim %then %do; 
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
	run;
%mend;
