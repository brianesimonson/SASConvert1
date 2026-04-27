* Modified - 08/11/2008 --- changed the format for standard error to have more decimal points ;
* Modified - 03/02/2012 --- changed length of output state variable;

%macro raterun2;
		%let contractor_cluster=state;
		%let strata=strata;
		%combined_ratio_estimator;

		proc means data=all nway;
		where program_type eq "&program_type";
		class &service_type_id &contractor_cluster  ;
		var dummy;
		output out=truecount sum=sampled_claims2;
		proc means data=truecount;
		var sampled_claims2;
		output out=truecount2 sum=total_claim_count;
		run;

		data finalstateresults;
		set error.&service_type_id.&dataset.results;
		if &contractor_cluster ne " " and &service_type_id ne .;
		run;
		proc sort; by &service_type_id ;

		
/*Compute National Rates*/
		data statestrataresults;
		set error.&service_type_id.&dataset.results;
		if &contractor_cluster = " " and &service_type_id ne .;
		state_strata_rate=rate;
		state_strata_sd=sdtaylor;
		var2sumcorrect=projpaid*sdtaylor;
		keep state_strata_rate &service_type_id ;
		run;

		data statestratasd;
		set error.&service_type_id.&dataset.results;
		if &contractor_cluster = " " and &service_type_id ne .;
		var2sumcorrect=(projpaid*sdtaylor)**2;
		keep var2sumcorrect &service_type_id ;
		run;

		proc sort data=statestrataresults;by &service_type_id;run;

		data step1;
		merge finalstateresults statestrataresults;
		by &service_type_id;

		delta=(projerr-state_strata_rate*projpaid);
		var2=((projpaid*sdtaylor)**2);
		run;

		proc sort data=finalstateresults;
		by &service_type_id;
		run;

		proc means data=step1;
		by &service_type_id;
		var delta var2 projerr projpaid sampled_line_items samperr samppaid;
		output out=&service_type_id._n  var=vardiff d1  d4 d5 d8 d10 d11 n=ss_n  d2 d6 d7 d9 d12 d13 
               sum=d3 var2sum projerr projpaid sampled_line_items samperr samppaid;
		run;

		data step2;
		merge &service_type_id._n total_file statestratasd(in=a);
		by &service_type_id;
		if a;
		N=total_states;
		n1=ss_n;
 		projerr2=payments*(projerr/projpaid);
		varRi=(((N**2)/n1)*(1-n1/N)*vardiff + N/n1*var2sumcorrect)/(((N/n1)*projpaid)**2);
		varRpiece=(payments**2)*(((N**2)/n1)*(1-n1/N)*vardiff + N/n1*var2sumcorrect)/(((N/n1)*projpaid)**2);
		sdRi=sqrt(varRi);
		drop N n1 d1 d2 d3 d4 d5 d6 d7 d8 d9 d10 d11 d12 d13;
		run;

		proc means data=step2;
		var varRpiece projerr2  payments sampled_line_items samperr samppaid;
		output out=step3 sum=varRpiece projerr2  payments sampled_line_items samperr samppaid;
		run;
		data step3;
		set step3;
		rate=projerr2/payments;
		varR=varRpiece/(payments**2);
		sdtaylor=sqrt(varR);
		projerr=projerr2;
		projpaid=payments;
				ucl=rate+1.96*sdtaylor;
				lcl=rate-1.96*sdtaylor;
				clcl=put(lcl,percent10.1);
				cucl=put(ucl,percent10.1);
				if ucl lt .10 then ci95=clcl||" -    "||left(cucl);
				if ucl ge .10 then ci95=clcl||" -  "||left(cucl);
				if ucl ge 1 then ci95=clcl||" -"||left(cucl);

		run;
		data step3point1;
		merge step3 truecount2;
			diff=sampled_line_items-total_claim_count;
		sampled_line_items=total_claim_count;
		run;
		data step4;
		set step3point1 step1;
			keep &service_type_id &contractor_cluster sampled_line_items samperr samppaid projerr projpaid rate sdtaylor ci95;
		run;

		data step5;
		merge step4 truecount(in=a);
		by &service_type_id &contractor_cluster;
		diff=sampled_line_items-sampled_claims2;
		if a then sampled_line_items=sampled_claims2;
		if a or state=" ";
		run;
			 	  data temporary;
          set  step5                                 end=EFIEOD;
          length state2 $20.;
		   		  if state=" " then state2 ="National";
		  else state2=state;

          %let _EFIERR_ = 0;     /* clear ERROR detection macro variable */
          %let _EFIREC_ = 0;     /* clear export record count macro variable*/
          file "&pathname/&outputfile..csv" delimiter=',' DSD DROPOVER lrecl=32767;
			 format sampled_line_items comma12.0;
			 format samperr dollar12.0;
			 format samppaid dollar12.0;
			 format projerr	dollar15.0;
			 format projpaid dollar15.0;
			 format rate percent20.16;
			 format sdtaylor percent20.16;
			format ci95 $char23.;
          if _n_ = 1 then        /* write column names */
           do;
             put
             "State"
             ','
			 'Sample Line Items'
			 ','
             'Sample Error'
			 ','
			 'Sample Paid'
			 ','
			 'Projected Error'
			 ','
			 'Projected Paid'
			 ','
			 'Rate'
			 ','
			 "Standard Error"
			 ','
			 '95% Confidence Interval'
			 

             ;
           end;
           do;
            EFIOUT + 1;

    		 put state2 $ @;
			 put sampled_line_items @;
			 put samperr @;
			 put samppaid @;
			 put projerr @;
			 put projpaid @;
			 put rate @;
			 put sdtaylor @;
			 put ci95;
             ;
           end;
          If _ERROR_ then        /* ERROR detection */
             call symput('_EFIERR_',1);
          If EFIEOD then
             call symput('_EFIREC_',EFIOUT);
          run;

		  data error.&outputfile;
		  set temporary;
		  run;

proc contents data=step4;
run;


proc print data=step1;
run;
proc print data=step2;
run;
proc print data=step3;
run;
proc print data=step4;
run;
proc print data=step5;
run;
%mend;		
