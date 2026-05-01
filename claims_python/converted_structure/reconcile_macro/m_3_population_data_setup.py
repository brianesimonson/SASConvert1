"""Auto-generated SAS->Python structural conversion module.

Source: Reconcile Macro/3_Population_Data_SetUp.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def popdataclean(indata: Any = None, outdata: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %popDataClean."""
    _arguments = {
        "indata": indata,
        "outdata": outdata,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """proc sort data=&indata.;
by state type qtr strata;
run;

data test_pop_totals_temp; /* should be empty, if not fix in manual changes */
set &indata.;
by state type qtr strata;
if first.strata ne last.strata;
run;

proc sql; 
	select count(*) into: numobs
	from test_pop_totals_temp; 
quit; 
%PrintMessage("Population data has &numobs. with duplicate Strata - check if >0");

data pop_totals;
set &indata.;
format qtr stratum $4.;
if state NE " ";
stratum = strata;
state_id=upcase(state);
if type = "MP" then type = "MF";
program_type = type;
	if program_type="MF" then do;
		claim_type="FFS";
		program = "Medicaid";
		end;
	else if program_type="MM" then do;
		claim_type="MC ";
		program = "Medicaid";
		end;
	else if program_type = "SF" then do;
		claim_type = "FFS";
		program = "CHIP";
		end;
	else if program_type = "SM" then do;
		claim_type = "MC ";
		program = "CHIP";
		end;
	else claim_type="XXX";
%if &error_type. = Claim %then %do;
pop_lines = totclm;
%end; 
%else %do; 
pop_lines = totclm_elg;
%end; 
drop strata;
run;

proc freq data = pop_totals;
tables stratum / list nopercent nocum ;
run;

proc sort data=pop_totals;
by state qtr type stratum;
run;

data test_pop; /* should be empty*/
set pop_totals;
by state qtr type stratum;
if first.stratum NE last.stratum;
run;

proc sql; 
	select count(*) into: numobs
	from test_pop; 
quit; 
data &outdata.;
	set pop_totals;
run;
%PrintMessage("Population data has &numobs. with duplicate stratum - check if >0");
ods tagsets.ExcelXP file="&QCPath./5_Population Data QC.xls"
		style = Normal options(autofit_width = 'yes' autofit_height = 'yes')
	options(embedded_titles = 'yes' embedded_footnotes='yes');
ods tagsets.Excelxp options(sheet_name="Population QC");
ods tagsets.Excelxp options(sheet_name="Population QC");
title "Duplicate Strata check";
proc print data=test_pop_totals_temp noobs; run; 
ods tagsets.Excelxp options(sheet_name="Population QC");
title "Duplicate Strata check";
proc print data=test_pop noobs; run;

Title "Population Data QC";
proc freq data=pop_totals;
tables program*claim_type program_type;
run;
proc freq data=pop_totals;
	title "*** Pop Totals ***";
	table state_id * (program claim_type qtr stratum)/nopercent nocol norow missing;
run;
proc freq data=pop_totals;
	title "*** Pop Totals ***";
	table state_id*program*claim_type/list;
run;
proc freq data=merged2;
	title "*** Sample Data ***";
	table state_id*program*claim_type stratum/list;
run;


ods tagsets.ExcelXP close;
ods listing; """
    return run_transpiled_macro(source_file="Reconcile Macro/3_Population_Data_SetUp.sas", macro_name="popDataClean", arguments=_arguments, sas_block=_sas_block)

