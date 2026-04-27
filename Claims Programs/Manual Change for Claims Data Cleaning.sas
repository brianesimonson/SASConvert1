/* Manual Change Macros for Raw Data */

%macro manual_raw_data_change_error_mr;
	data MR;
		set MR; 
		if substr(permid, 1, 2) NE "PR";
	run;
%mend manual_raw_data_change_error_mr;


%macro manual_raw_data_change_error_dp;
	data DP;
		set DP; 
		if substr(permid, 1, 2) NE "PR";
	run;
%mend manual_raw_data_change_error_dp;


%macro manual_raw_data_change_claim;
	data full_data;
	set full_data; 
	where substr(permid, 1, 2) NE "PR";
		/* CC 8/23/22 - zero out underpayments for specific claim at the claim level */
		if permid = "CAC2302F016" then do;
			Processing_Underpayment = 0;
			Underpayments = 0;
		end;
	run;
%mend manual_raw_data_change_claim;


/* Any manual changes to the data Here*/
%macro manual_data_change; /* change any specific claims here, for example incorrect dollar amounts */
/* if perm_id = X then amount_paid = X*/

%mend manual_data_change;


%macro pop_totals_manual_change(indata=,outdata=);
data &outdata.;
	set &indata.;
	*Any manual changes to population data; 
	if missing(fyear) then fyear = "&pyear.";
run; 
%mend pop_totals_manual_change;

%macro pop_totals_manual_change_nodup;
%PrintMessage("Remove duplicate - nodupkey by state qtr type stratum totclm_clm");
data temp; 
	set poptotals_temp; 
	if not missing(cnt_act_sampled); 
	if cnt_act_sampled_clm ne 0; /* CS Added 8/22/2023 since 2 strata that ELG only oversamples */
run;  
proc sort data = temp out = poptotals_temp nodupkey ;
by state qtr type stratum totclm;
run;

%mend pop_totals_manual_change_nodup;

%macro pop_totals_manual_change_nodup2;
%PrintMessage("Remove duplicate - nodupkey by state qtr type stratum totclm_clm");
proc sort data = pop_totals_temp out = pop_totals_temp nodupkey ;
by state type qtr strata;
run;

%mend pop_totals_manual_change_nodup2;

/* any manual changes to sweight data saved at here */
%macro SE_Rate_data_Manual_change;

%mend SE_Rate_data_Manual_change;