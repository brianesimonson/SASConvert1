/*********************************************************
This Macro is used for qualifier and subqualifier mapping
for all 3 files (ER, MR, & DP). Export QC checks for 
qualifier mapping.
*/
%macro qualifier_coding(indata); 
/*************************** add qualifier coding  ****************************/
proc sort data=&indata.;
by code qualifier;
run;

data merged_map;
merge &indata. (in=inall) map (in=inmap);
by code qualifier;
if inall;
if inall and inmap then flag_qualmap = "both";
else if inall then flag_qualmap = "data";
run;

/* export non matches */
data perm.&abbr._add_to_qualmap;
set merged_map;
if flag_qualmap = "data";
if code not in ("C1","P1","P2");
keep perm_id code qualifier;
run;

%assign_qualifier_label_cleaning(merged_map,&abbr._errors_raw_fin);

/**** check for changed qualifiers ******/
data perm.changed_qualifier_&abbr.;
set &abbr._errors_raw_fin;
if code not in ("C1","P1","P2") then do;
	if qualifier NE tranwrd(qualifier_orig,".","")
		then keep = 1;
	end;
if keep = 1;
keep perm_id code qualifier qualifier_orig mapped_qualcode
	unique_qualcode;
run;

%mend qualifier_coding;
%macro assign_qualifier_label_cleaning(indata,outdata);
data temp;
set &indata.;
/* mark errors to receive a new error code */
if code not in ("C1", "P1", "P2") then code = "XX";
drop qualifier ;
run;

proc sort data=temp; by unique_qualcode; run;

data &abbr._qualcode_change;
set qualcode.&abbr._qualcode_change;
unique_qualcode = &name._unique_qualcode;
mapped_qualcode = &name._mapped_qualcode;
keep unique_qualcode mapped_qualcode;
run;

data &abbr.;
merge temp (in=ina) &abbr._qualcode_change;
by unique_qualcode;
if ina;
run;

proc sort; by mapped_qualcode;run;

data &abbr._unique_map;
set qualcode.&abbr._unique_map;
mapped_qualcode = &name._mapped_qualcode;
codex = &name._error_codex;
%if &abbr. = DP %then %do;
	qualifier = processing_reason_for_error_code;
%end;
%else %if &abbr. = MR %then %do;
	qualifier = medical_review_reason_for_error;
%end;
%else %if &abbr. = ER %then %do;
	qualifier = eligibility_reason_for_error;
%end;
keep mapped_qualcode codex qualifier;
run;

data &abbr.;
merge &abbr. (in=ina) &abbr._unique_map;
by mapped_qualcode;
if ina;
run;

data &outdata.;
set &abbr.; 
if not missing(codex) then code = codex;
drop codex;
run;

%mend assign_qualifier_label_cleaning;
%macro assign_qualifier_label2(indata,outdata);
data temp;
set &indata.;
/* mark errors to receive a new error code */
if code not in ("C1", "P1", "P2") then code = "XX";
drop qualifier ;
run;

proc sort data=temp; by unique_qualcode; run;

data &abbr._qualcode_change;
set qualcode.&abbr._qualcode_change;
unique_qualcode = &name._unique_qualcode;
mapped_qualcode = &name._mapped_qualcode;
keep unique_qualcode mapped_qualcode;
run;

data &abbr.;
merge temp (in=ina) &abbr._qualcode_change;
by unique_qualcode;
if ina;
run;

proc sort; by mapped_qualcode;run;

data &abbr._unique_map;
set qualcode.&abbr._unique_map;
mapped_qualcode = &name._mapped_qualcode;
codex = &name._error_codex;
%if &abbr. = DP %then %do;
	qualifier = processing_reason_for_error_code;
%end;
%else %if &abbr. = MR %then %do;
	qualifier = medical_review_reason_for_error;
%end;
%else %if &abbr. = ER %then %do;
	qualifier = eligibility_reason_for_error;
%end;

keep mapped_qualcode codex qualifier;
run;

data &abbr.;
merge &abbr. (in=ina) &abbr._unique_map;
by mapped_qualcode;
if ina;
run;

data &outdata.;
set &abbr.; 
if not missing(codex) then code = codex;
drop codex;
run;

%mend assign_qualifier_label2;

%macro subqualifier_coding;
%if &abbr. = MR %then %do; 
	%let prefix = MR_; 
%end;
%else %do; 
	%let prefix = ; 
%end;
/* get mapping */
data sq_map (drop = Mapped_Subqualifier_Code);
format unique_subqualifier_code $10.;
      set subqual.subqualifier_code_map;
sq_length = length(subqualifier);
	/* limit to only DP or MR - Added CC 4/11/2025 */
	if index(unique_subqualifier_code,"&abbr.")>=1;
run;

proc sort data = sq_map; by descending sq_length; quit;

/*determine number of subqual codes to loop through*/
data _null_;
      set sq_map nobs = size;
call symputx('size',size,'Global');
run;

%Assign_SQC;

%assign_subqualifier_label2(merged2_subqual,&abbr._errors_raw2);

/* subqualifier check */
data perm.&abbr._changed_subqualifier;
set &abbr._errors_raw2;
if not missing(&prefix.subqualifiers);
if &prefix.subqualifiers NE &prefix.subqualifiers_orig;
keep &prefix.subqualifiers &prefix.unique_subqualifier_code
	&prefix.mapped_subqualifier_code &prefix.subqualifiers_orig;
run;

%mend subqualifier_coding;
%macro assign_subqualifier_label2(indata,outdata);

data mapme;
set &indata.;
drop &prefix.subqualifiers;
run;

/* get mapping to map codes */
data mapped_qual;
format unique_subqualifier_code $10.;
      set subqual.subqualifier_code_map;
  	/* limit to only DP or MR - Added CC 4/11/2025 */
	if index(unique_subqualifier_code,"&abbr.")>=1;
keep unique_subqualifier_code mapped_subqualifier_code;
run;

/*determine number of subqual codes to loop through*/
data _null_;
      set mapped_qual nobs = size;
call symputx('size',size,'Global');
run;

/* assign the mapped subqualifier code */
%do i = 1 %to &size.;
      data mapped_qual1;
                  set mapped_qual;
            if _n_ = &i.;
            call symputx('unique_subqualifier_code', unique_subqualifier_code);
            call symputx('mapped_subqualifier_code', mapped_subqualifier_code);
            run;
      %if &i.=1 %then %do; /* set up the new variable */
            data mapped_data;
            format &prefix.mapped_subqualifier_code $750.;
                  set mapme;
            &prefix.mapped_subqualifier_code = transtrn(&prefix.unique_subqualifier_code,"&unique_subqualifier_code.","&mapped_subqualifier_code.");      
            run;
      %end;
      %else %do;
            data mapped_data; /* change the new variable */
            format &prefix.mapped_subqualifier_code $750.;
                  set mapped_data;
            &prefix.mapped_subqualifier_code = transtrn(&prefix.mapped_subqualifier_code,"&unique_subqualifier_code.","&mapped_subqualifier_code.");
            run;  
      %end;
%end;

/* get mapping to put text back */
data reassign_subqual;
      set subqual.subqualifier_code_map;
new_subqualifier_code = unique_subqualifier_code;
keep new_subqualifier_code subqualifier;
run;

/*determine number of subqual codes to loop through*/
data _null_;
      set reassign_subqual nobs = size;
call symputx('size',size,'Global');
run;

/* assign the mapped subqualifier code */
%do i = 1 %to &size.;
      data reassign_subqual1;
                  set reassign_subqual;
            if _n_ = &i.;
            call symputx('subqualifier', subqualifier);
            call symputx('new_subqualifier_code', new_subqualifier_code);
            run;
      %if &i.=1 %then %do; /* set up the new variable */
            data mapped_data2;
            format &prefix.subqualifiers $750.;
                  set mapped_data;
            &prefix.subqualifiers = transtrn(&prefix.mapped_subqualifier_code,"&new_subqualifier_code.","&subqualifier.");      
            run;
      %end;
      %else %do;
            data mapped_data2; /* change the new variable */
            format &prefix.subqualifiers $750.;
                  set mapped_data2;
            &prefix.subqualifiers = transtrn(&prefix.subqualifiers,"&new_subqualifier_code.","&subqualifier.");
            run;  
      %end;
%end;

data &outdata.;
set mapped_data2;
run;

%mend assign_subqualifier_label2;
%macro Assign_SQC;
%do i = 1 %to &size.;
      data sq_map1;
                  set sq_map;
            if _n_ = &i.;
            call symputx('Subqualifier', subqualifier);
            call symputx('USC', unique_subqualifier_code);
            run;
      %if &i.=1 %then %do; /* set up the new variable */
            data merged2_subqual;
            format &prefix.unique_subqualifier_code $750.;
                  set &abbr._errors_raw;
            &prefix.unique_subqualifier_code = transtrn(&prefix.subqualifiers,"&subqualifier.","&usc.");      
            run;
      %end;
      %else %do;
            data merged2_subqual; /* change the new variable */
            format &prefix.unique_subqualifier_code $750.;
                  set merged2_subqual;
            &prefix.unique_subqualifier_code = transtrn(&prefix.unique_subqualifier_code,"&subqualifier.","&usc.");
            run;  
      %end;
%end;
%mend Assign_SQC;

%macro qualifier_subqual_check_export;
proc datasets library=work;
delete qc_summaryQual qc_summary_TCQual; 
run; 
ods listing close; 
ods tagsets.ExcelXP file="&QCPath./0_Qualifier Check.xls"
	style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
options(embedded_titles = 'yes' embedded_footnotes='yes');
%if &error_type. = Claim %then %do; 
	%export_QC(perm.mr_add_to_qualmap, "Check any additional MR Qualifier added",Qual)
	%export_QC(perm.changed_qualifier_mr, "Check any changed MR Qualifier",Qual)
	%export_QC(perm.dp_add_to_qualmap, "Check any additional DP Qualifier added",Qual)
	%export_QC(perm.changed_qualifier_dp, "Check any changed DP Qualifier",Qual)
	%export_QC(perm.mr_changed_subqualifier, "Check any changed MR Sub-Qualifier",Qual)
	%export_QC(perm.dp_changed_subqualifier, "Check any changed DP Sub-Qualifier",Qual)
	%export_Summary(qc_summary&type.Qual, "Summary of Qualifier and Sub-Qualifier Report"); 
	%export_Summary(qualcode.MR_QUALIFIER_CODE_MAP, "MR_QUALCODE_CODE_MAP");
	%export_Summary(qualcode.DP_QUALIFIER_CODE_MAP, "DP_QUALCODE_CODE_MAP");
	%export_Summary(subqual.subqualifier_code_map, "Sub-Qualifier Code Map");
%end;
%else %do;
	%export_QC(perm.er_add_to_qualmap, "Check any additional ER Qualifier added",Qual)
	%export_QC(perm.changed_qualifier_er, "Check any changed ER Qualifier",Qual)
	%export_Summary(qc_summary&type.Qual, "Summary of Qualifier Report"); 
	%export_Summary(qualcode.ER_QUALIFIER_CODE_MAP, "MR_QUALCODE_CODE_MAP");
%end; 
ods tagsets.ExcelXP close;
ods listing;
%mend qualifier_subqual_check_export;
