"""Auto-generated SAS->Python structural conversion module.

Source: Global Macros/combined ratio estimator.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def combined_ratio_estimator(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %combined_ratio_estimator."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """				proc means data=all noprint;
				var &denominator;
				class &strata cid;
				output out=claim_all sum=;
				data claim_all;set claim_all;if &strata ne " " and cid ne " ";run;
				data claim_all;merge claim_all weights2;by &strata;
				proc means data=claim_all  noprint missing;
				var &denominator;
				class &strata;
				weight weight;
				output out=proj_all_paid n=nall sum=projpaid_all;run;
				proc means data=claim_all noprint missing;
				var &denominator;
				class &strata;
				output out=all_paid2  var=var_paid_all mean=avg_pay_samp_all;run;
				data proj_all_paid;merge proj_all_paid all_paid2;by &strata;if &strata ne " ";




				proc means data=all noprint;
				class &strata &contractor_cluster;
				var dummy;
				output out=crosswalk1 sum=sum;
				run;
				data crosswalk1;set crosswalk1;if &strata ne " " and &contractor_cluster ne " ";keep &strata &contractor_cluster; RUN;

				proc sort; by &strata ; RUN;




				data &dataset.1234;set &dataset;

				dummy=1;
				dummylines=1;
				keep &numerator &denominator dummy dummylines &strata &service_type_id cid &contractor_cluster;
				proc sort tagsort;by &strata;
				proc sort data=weights2;by &strata;

				data temppaid;merge &dataset.1234(in=a) weights2 proj_all_paid;by &strata;
				if a;
				num_delta=&numerator;
				den_delta=&denominator;
				num_unadj=&numerator;
				den_unadj=&denominator;
				run;

				proc means data=temppaid noprint missing;class &strata &service_type_id &contractor_cluster;
				var num_delta den_delta num_unadj den_unadj;
				weight weight;
				output out=justrates sum=;
				run;

				data r1 r2 r3 r4 r5 r6;
				set justrates;
				dummythis=1;
				rate= num_delta/den_delta;
				if &strata=" " and &service_type_id=" " and &contractor_cluster=" " then output r1;
				else if &strata ne " " and &service_type_id=" " and &contractor_cluster ne " " then output r2;
				else if &strata = " " and &service_type_id ne " " and &contractor_cluster=" " then output r3;
				else if &strata ne " " and &service_type_id ne " " and &contractor_cluster ne " " then output r4;
				else if &strata = " " and &service_type_id = " " and &contractor_cluster ne " " then output r5;
				else if &strata = " " and &service_type_id ne " " and &contractor_cluster ne " " then output r6;

				data r1;set r1; rename rate=r1 num_delta=e1star den_delta=p1star num_unadj=e1 den_unadj=p1;
				data r2;set r2; rename rate=r2 num_delta=e2star den_delta=p2star num_unadj=e2 den_unadj=p2;
				data r3;set r3; rename rate=r3 num_delta=e3star den_delta=p3star num_unadj=e3 den_unadj=p3;
				data r4;set r4; rename rate=r4 num_delta=e4star den_delta=p4star num_unadj=e4 den_unadj=p4;
				data r5;set r5; rename rate=r5 num_delta=e5star den_delta=p5star num_unadj=e5 den_unadj=p5;
				data r6;set r6; rename rate=r6 num_delta=e6star den_delta=p6star num_unadj=e6 den_unadj=p6;

				data r2;
				merge r2 proj_all_paid;
				by &strata;
				run;

				data r1;set r1;keep e1 p1 r1 e1star p1star dummythis;

				proc sort data=r1;
					by dummythis;
				run;

				data r2;set r2;keep e2 p2 r2 e2star p2star dummythis &strata &contractor_cluster projpaid_all nall
				var_paid_all avg_pay_samp_all;

				proc sort data=r2;
					by dummythis;
				run;

				data ratefile1;
				merge r2 r1;
				by dummythis;


				proc sort data=ratefile1;
					by &contractor_cluster;
				run;

				data r5;set r5;keep e5 p5 r5 e5star p5star dummythis &contractor_cluster;

				proc sort data=r5;
					by &contractor_cluster;
				run;


				data ratefile1;
				merge ratefile1 r5;
				by &contractor_cluster;
				run;

				proc sort data=r4;by &strata;
				data r4;merge r4 proj_all_paid; by &strata;
				data r4;set r4;keep e4 p4 r4 e4star p4star dummythis &strata &service_type_id &contractor_cluster projpaid_all nall
				var_paid_all avg_pay_samp_all;

				proc sort data=r4; by  &service_type_id;

				
				data r3;set r3;keep e3 p3 r3 e3star p3star dummythis &service_type_id ;

				data ratefile2;
				merge r3 r4;
				by &service_type_id;
				keep r3 r4 e3 e4 p3 p4 e3star e4star p3star p4star &strata &service_type_id projpaid_all nall var_paid_all avg_pay_samp_all &contractor_cluster;
				run;
				proc sort data=ratefile2;by &service_type_id &contractor_cluster;

				data r6;set r6;keep e6 p6 r6 e6star p6star dummythis &service_type_id &contractor_cluster;
				proc sort data=r6;by &service_type_id &contractor_cluster;
				data ratefile2;
				merge ratefile2 r6;
				by &service_type_id &contractor_cluster;
				run;

				proc means data=temppaid noprint missing;class &strata cid ;
				var &numerator &denominator dummylines;
				output out=claims sum=&numerator &denominator lines;
				data claims;set claims; if &strata ne " " and cid ne " ";
				proc sort;by &strata;
				proc sort data=ratefile1;by &strata;
				proc sort data=weights2;by &strata;

				data claims;merge claims(in=a) weights2 ratefile1 proj_all_paid;by &strata ;if a;
				theta1=&numerator - r1*&denominator;
				theta2=&numerator - r5*&denominator;

				diff1 = &numerator - r1*&denominator;
				diff2 = &numerator - r5*&denominator;
				dummyclaims=1;

				proc means data=claims noprint missing;by &strata;
				var  &numerator &denominator diff1 diff2 lines dummyclaims theta1 theta2;
				output out=clusterrates  sum=&numerator &denominator d1 d2 lines claims sum_theta1 sum_theta2 
					n=d5 d6 n1 n2 d7 d10 d22 d23 var= d3 samp_pay_var diff1 diff2 d8 d11 d20 d21;

				data clusterrates;merge clusterrates weights2 ratefile1; by &strata;

				*avg_pay_samp_all=(projpaid_all/weight)/nall;
				avg_pay_samp_domain=(&denominator/claims);
				rate=&numerator/&denominator;

				s21     =((claims-1)/(nall-1))*diff1
						 + (claims/(nall-1))*(1-claims/nall)*((sum_theta1/claims)**2);

				s22     =((claims-1)/(nall-1))*diff2
				 + (claims/(nall-1))*(1-claims/nall)*((sum_theta2/claims)**2);

				piece=(1/(p1**2))*(weight**2)*nall*s21;
				*piece=(1/((weight*&denominator)**2))*(weight**2)*nall*s21;

				piececluster=(1/(p5**2))*(weight**2)*nall*s22;
				run;

					data savethis;set clusterrates;

				proc means noprint missing;
				var piece n2 e2star p2star lines claims &numerator &denominator;
				output out=total sum=;

				proc means data=clusterrates noprint missing;
				class &contractor_cluster;
				var piececluster n2 e2star p2star lines claims &numerator &denominator;
				output out=clustertotal sum=;
				data clustertotal;set clustertotal; if &contractor_cluster ne  " ";

				data final;
				set clustertotal total;

				final_lines=lines;
				final_claims=claims;
				final_paid_sample=&denominator;
				final_error_sample=&numerator;
				final_paid_proj=p2star;
				final_error_proj=e2star;
				final_rate=e2star/p2star;
				if &contractor_cluster = " " then se_final=sqrt(piece);
				else se_final=sqrt(piececluster);
				run;

				proc means data=temppaid noprint missing;class &strata &service_type_id cid ;
				var &numerator &denominator dummylines;
				output out=claims sum=&numerator &denominator lines;
				data claims;set claims; if &strata ne " " and  &service_type_id ne " " and cid ne " ";
				proc sort;by &strata &service_type_id;
				proc sort data=ratefile2;by &strata &service_type_id;

				data claims;merge claims ratefile2 ;by &strata  &service_type_id;
				data claims;merge claims proj_all_paid;by &strata;
				theta1=&numerator - r3*&denominator;
				theta2=&numerator - r6*&denominator;

				diff1 = &numerator - r3*&denominator;
				diff2 = &numerator - r6*&denominator;
				dummyclaims=1;


				proc means data=claims noprint missing;by &strata  &service_type_id;
				var  &numerator &denominator diff1 diff2 lines dummyclaims theta1 theta2;
				output out=clusterrates  sum=&numerator &denominator d1 d2 lines claims sum_theta1 sum_theta2 
					n=d5 d6 n3 n4 d7 d10 d22 d23 var= d3 samp_pay_var diff1 diff2 d8 d11 d20 d21;


				data clusterrates;merge clusterrates ratefile2; by &strata  &service_type_id;
				data clusterrates; merge clusterrates(in=a) weights2; by &strata;if a;


				avg_pay_samp_domain=(&denominator/claims);

				rate=&numerator/&denominator;


				s21     =((claims-1)/(nall-1))*diff1 + (claims/(nall-1))*(1-claims/nall)*((sum_theta1/claims)**2)
						;
				s22     =((claims-1)/(nall-1))*diff2 + (claims/(nall-1))*(1-claims/nall)*((sum_theta2/claims)**2)
						;

				piece=(1/(p3**2))*(weight**2)*nall*s21;
				piececluster=(1/(p6**2))*(weight**2)*nall*s22;
				run;

				proc sort tagsort;by &service_type_id;
				proc means noprint missing;
				by  &service_type_id;
				var piece n4 e4star p4star lines claims &numerator &denominator;
				output out=total sum=;

				proc sort data=clusterrates tagsort;by &contractor_cluster &service_type_id;
				proc means noprint missing;
				by  &contractor_cluster &service_type_id;
				var piececluster n4 e4star p4star lines claims &numerator &denominator;
				output out=clustertotal sum=;

				data finalby;
				set clustertotal total;


				final_lines=lines;
				final_claims=claims;
				final_paid_sample=&denominator;
				final_error_sample=&numerator;
				final_paid_proj=p4star;
				final_error_proj=e4star;
				final_rate=e4star/p4star;
				if &contractor_cluster = " " then se_final=sqrt(piece);
				else se_final=sqrt(piececluster);
				run;

				data results;
				set final finalby;
				projerr=final_error_proj;
				projpaid=final_paid_proj;
				samperr=final_error_sample;
				samppaid=final_paid_sample;
				rate=final_rate;
				sampled_claims=final_claims;
				sampled_line_items=final_lines;
				sdtaylor=se_final;
				ucl=rate+1.96*sdtaylor;
				lcl=rate-1.96*sdtaylor;
				clcl=put(lcl,percent10.1);
				cucl=put(ucl,percent10.1);
				if ucl lt .10 then ci95=clcl||" -    "||left(cucl);
				if ucl ge .10 then ci95=clcl||" -  "||left(cucl);
				if ucl ge 1 then ci95=clcl||" -"||left(cucl);

				*if &contractor_cluster=" " then &contractor_cluster="zall";
				keep &contractor_cluster &service_type_id ci95 projerr projpaid samperr samppaid rate sampled_line_items sampled_claims sdtaylor lcl ucl;

				data error.&service_type_id.&dataset.results;
				set results;
				run;"""
    return run_transpiled_macro(source_file="Global Macros/combined ratio estimator.sas", macro_name="combined_ratio_estimator", arguments=_arguments, sas_block=_sas_block)

