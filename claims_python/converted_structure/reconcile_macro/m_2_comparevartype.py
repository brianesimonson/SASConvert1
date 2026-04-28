"""Auto-generated SAS->Python structural conversion module.

Source: Reconcile Macro/2_CompareVarType.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def checkvartype(pre_data: Any = None, cur_data: Any = None, outdata: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %checkVarType."""
    _arguments = {
        "pre_data": pre_data,
        "cur_data": cur_data,
        "outdata": outdata,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """* check variable character with previous year data;
proc contents data=previous.&pre_data. /*&pre_data.*/
	out=pyr_vars(keep=NAME TYPE length format rename=(TYPE=pyr_type LENGTH=pyr_length format=pyr_format)); run; 
proc contents data=&cur_data. /*&cur_data.*/
	out=cyr_vars(keep=NAME TYPE length format); run;
data pyr_vars; 
	set pyr_vars; 
	NAME2 = UPCASE(NAME); 
run; 
data cyr_vars; 
	set cyr_vars; 
	NAME2 = UPCASE(NAME); 
run; 
proc sort data=pyr_vars; by NAME2; run; 
proc sort data=cyr_vars; by NAME2; run; 

data vars_merge;
	merge pyr_vars(in=a) cyr_vars(in=b); 
	by NAME2; 
	length merge_type type_flag $50.; 
	if a and b then merge_type ="Both yrs";
	else if a and not b then merge_type = "Pre yr";
	else if not a and b then merge_type = "Cur yr";

	if merge_type ="Both yrs" then do; 
		if pyr_type = type then type_flag = "Matched";
		else type_flag = "Nonmatched";
	end;
run; 
proc freq data=	vars_merge; 
tables merge_type*type_flag/list missing; 
run; 

* Export ;
data nonmatch_variables; 
	set vars_merge;
	if merge_type ne "Both yrs";
run; 

data nonmatch_vartype;
	set vars_merge; 
	if type_flag = "Nonmatched";
run; 


*convert variables based on previous year var type; 
proc sql;
	select count(*) into: nonmatch_vartype_count
	from nonmatch_vartype; 
quit; 
%put &nonmatch_vartype_count.;
%let var_count = %eval(&nonmatch_vartype_count.); 
/*%let nonmatch_vartype_count =2;*/
%if &var_count. > 0 %then %do; 
	*convert non matching variables same as previous year; 
	proc sql; 
		select name, pyr_type, pyr_length into
			:name1 - :name&var_count.,
			:type1 - :type&var_count.,
			:len1 - :len&var_count.
		from nonmatch_vartype;
	quit; 

	data temp;
		set &cur_data.; /*&cur_data.*/
		%do i = 1 %to &var_count.;
			%if &&type&i.. = 1 %then %do;
				%let length = &&len&i...;
				%put &length.;
			%end;
			%else %do;
				%let length = $&&len&i...;
				%put &length.;
			%end;
			length 	&&name&i..2 &length;
			&&name&i..2 = &&name&i..; 
			drop &&name&i..;
			rename &&name&i..2 = &&name&i..; 
		%end; 
	run; 
%end;
%else %do;
	data temp;
		set &cur_data.;
	run; 
%end;

	data type_matched; 
		set vars_merge; 
		if type_flag = "Matched" and pyr_length ne length; 
		length changed_format $100.;
		max_len = max(pyr_length,length); 
		if pyr_type = 2 then changed_format = strip(NAME2)||' $'||strip(max_len)||".";
	run; 
	proc sql; 
		select changed_format into: changed_format separated by ' ' 
		from type_matched; 
	quit; 
	%PUT &changed_format.;
	DATA &outdata.; 
		FORMAT &changed_format.;
		SET temp; 
	RUN; 
	"""
    return run_transpiled_macro(source_file="Reconcile Macro/2_CompareVarType.sas", macro_name="checkVarType", arguments=_arguments, sas_block=_sas_block)

