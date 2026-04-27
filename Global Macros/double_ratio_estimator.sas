
%macro double_ratio_estimator;
data weights2;
set weights2;
keep strata weight universe_claims total;
run;
				proc means data=all noprint nway;
				var &denominator &auxiliary; /* Updated */
				class &strata &partition cid;
				output out=claim_all sum=;
				proc sort data = weights2; by &strata;
				data claim_all;merge claim_all(in=a) weights2;by &strata;if a;
				proc means data=claim_all  noprint missing nway;
				var &auxiliary; /* NEW */
				class &partition;
				weight weight;
				output out=proj_all_paid  sum=projpaid_all;run;
				proc means data=claim_all noprint missing nway;
				var &denominator &auxiliary;
				class  &partition &strata ;
				output out=all_paid2  var=var_paid_all var_paid_all_aux mean=avg_pay_samp_all avg_pay_samp_all_aux n=n_ki n_aux;run;
				proc means data=all_paid2  noprint nway;
				var n_ki;
				class &strata;
				output out=strata_stat sum=nall;
				data proj_all_paid;merge proj_all_paid all_paid2;by &partition;
				proc sort;by &strata;
				data proj_all_paid;
				merge proj_all_paid strata_stat;
				by &strata;
				run;
				proc sort;by &partition &strata;
				data &dataset.1234;set &dataset;

				dummy=1;
				dummylines=1;
				keep &numerator &denominator dummy dummylines &strata &partition &service_type_id cid &contractor_cluster &auxiliary;
				proc sort tagsort;by &strata;
				proc sort data=weights2;by &strata;
				data temppaid;merge &dataset.1234(in=a) weights2;by &strata;if a;
				proc sort;by &partition;run;
				proc sort data=total_file;by &partition;
				data temppaid;merge temppaid(in=a) total_file ;by &partition;
				if a;

				run;
				proc sort;by &partition &strata;
				data temppaid;merge temppaid(in=a) proj_all_paid;by &partition &strata;
				if a;
				num_delta=&numerator*(payments/projpaid_all);
				den_delta=&denominator*(payments/projpaid_all);
				num_unadj=&numerator;
				den_unadj=&denominator;
				run;

				proc means data=temppaid noprint missing;class &strata &partition &service_type_id &contractor_cluster;
				var num_delta den_delta num_unadj den_unadj;
				weight weight;
				output out=justrates sum=;
				run;


				data r1 r2 r3 r4 r5 r6;
				set justrates;
				dummythis=1;
				rate= num_delta/den_delta;
				if &strata=" " and &partition = " " and &service_type_id=" " and &contractor_cluster=" " then output r1;
				else if &strata = " " and &partition ne " " and &service_type_id=" " and &contractor_cluster ne " " then output r2;
				else if &strata = " " and &partition = " " and &service_type_id ne " " and &contractor_cluster=" " then output r3;
				else if &strata = " " and &partition ne " " and &service_type_id ne " " and &contractor_cluster ne " " then output r4;
				else if &strata = " " and &partition = " " and &service_type_id = " " and &contractor_cluster ne " " then output r5;
				else if &strata = " " and &partition = " " and &service_type_id ne " " and &contractor_cluster ne " " then output r6;

				data r1;set r1; rename rate=r1 num_delta=e1star den_delta=p1star num_unadj=e1 den_unadj=p1;
				data r2;set r2; rename rate=r2 num_delta=e2star den_delta=p2star num_unadj=e2 den_unadj=p2;
				data r3;set r3; rename rate=r3 num_delta=e3star den_delta=p3star num_unadj=e3 den_unadj=p3;
				data r4;set r4; rename rate=r4 num_delta=e4star den_delta=p4star num_unadj=e4 den_unadj=p4;
				data r5;set r5; rename rate=r5 num_delta=e5star den_delta=p5star num_unadj=e5 den_unadj=p5;
				data r6;set r6; rename rate=r6 num_delta=e6star den_delta=p6star num_unadj=e6 den_unadj=p6;
				

				data r1;set r1;keep e1 p1 r1 e1star p1star dummythis;

				proc sort data=r1;
					by dummythis;
				run;

				data r2;set r2;keep e2 p2 r2 e2star p2star dummythis &partition &contractor_cluster;
*projpaid_all nall	var_paid_all avg_pay_samp_all;

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



				data r4;set r4;keep e4 p4 r4 e4star p4star dummythis &partition &service_type_id &contractor_cluster;


				proc sort data=r4; by  &service_type_id;

				
				data r3;set r3;keep e3 p3 r3 e3star p3star dummythis &service_type_id ;
				proc sort data=r3; by &service_type_id;

				data ratefile2;
				merge r3 r4;
				by &service_type_id;
				keep r3 r4 e3 e4 p3 p4 e3star e4star p3star p4star &partition &service_type_id  &contractor_cluster;
				run;
				proc sort data=ratefile2;by &service_type_id &contractor_cluster;

				data r6;set r6;keep e6 p6 r6 e6star p6star dummythis &service_type_id &contractor_cluster;
				proc sort data=r6;by &service_type_id &contractor_cluster;
				data ratefile2;
				merge ratefile2 r6;
				by &service_type_id &contractor_cluster;
				run;

				proc means data=temppaid noprint missing nway;class &strata &partition &contractor_cluster cid ;
				var &numerator &denominator dummylines &auxiliary;
				output out=claims sum=&numerator &denominator lines &auxiliary;

				proc sort;by &partition &contractor_cluster;
				proc sort data=ratefile1;by &partition &contractor_cluster;
				data claims;merge claims(in=a) ratefile1 ;by &partition &contractor_cluster;if a;run;

				proc sort;by &partition &strata;
				proc sort data=proj_all_paid;by &partition &strata;
				data claims;merge claims(in=a) proj_all_paid ;by &partition &strata;if a;


				proc sort data=weights2;by &strata;
				proc sort data=claims;by &strata;
			    

				data claims;merge claims(in=a) weights2;by &strata ;if a;
				theta1=&numerator - r1*&denominator;
				theta2=&numerator - r5*&denominator;

				diff1 = &numerator - r1*&denominator-((e2-r1*p2)/projpaid_all)*&denominator;
				diff2 = &numerator - r5*&denominator-((e2-r5*p2)/projpaid_all)*&denominator;
				dummyclaims=1;run;

				proc means data=claims noprint missing;by &strata &partition &contractor_cluster;
				var  &numerator &denominator diff1 diff2 lines dummyclaims theta1 theta2 &auxiliary;
				output out=clusterrates  sum=&numerator &denominator d1 d2 lines claims sum_theta1 sum_theta2 &auxiliary
					n=d5 d6 n1 n2 d7 d10 d22 d23 d24 var= d3 samp_pay_var diff1 diff2 d8 d11 d20 d21 samp_pay_var_aux;

				data clusterrates;merge clusterrates(in=a) weights2 ; by &strata;if a;
				proc sort;by &partition &contractor_cluster;
				data clusterrates;merge clusterrates(in=a)  ratefile1; by &partition &contractor_cluster;if a;
				proc sort; by &partition &strata;
				data clusterrates;merge clusterrates(in=a)  proj_all_paid ;by &partition &strata;if a;
				data clusterrates;merge clusterrates(in=a) total_file ;by &partition ;if a;
				kscye1=(e2-r1*p2)/projpaid_all;
				kscye2=(e2-r5*p2)/projpaid_all;
				*avg_pay_samp_all=(projpaid_all/weight)/nall;
				avg_pay_samp_domain=(&denominator/claims);
				avg_pay_samp_domain_aux=(&auxiliary/claims);
				rate=&numerator/&denominator;

				s21_temp1   =((claims-1)/(nall-1))*diff1 ;
				s21_temp2	=-(kscye1**2)*((claims-1)/(nall-1))*samp_pay_var_aux ;
				s21_temp3 	=(kscye1**2)*var_paid_all_aux*((n_ki-1)/(nall-1)) ;
				s21_temp4	=(claims/(nall-1))*(1-claims/nall)*((sum_theta1/claims)**2) ; 
				s21_temp5 	=2*(claims/(nall-1))*kscye1*(sum_theta1/claims)*(((n_ki)/(nall))*avg_pay_samp_all_aux - avg_pay_samp_domain_aux);
				s21_temp6 	=(n_ki/(nall-1))*(1-n_ki/nall)*(kscye1**2)*(avg_pay_samp_all_aux**2);

				s22_temp1   =((claims-1)/(nall-1))*diff2 ;
				s22_temp2	=-(kscye2**2)*((claims-1)/(nall-1))*samp_pay_var_aux ;
				s22_temp3 	=(kscye2**2)*var_paid_all_aux*((n_ki-1)/(nall-1)) ;
				s22_temp4	=(claims/(nall-1))*(1-claims/nall)*((sum_theta2/claims)**2) ; 
				s22_temp5 	=2*(claims/(nall-1))*kscye2*(sum_theta2/claims)*(((n_ki)/(nall))*avg_pay_samp_all_aux - avg_pay_samp_domain_aux);
				s22_temp6 	=(n_ki/(nall-1))*(1-n_ki/nall)*(kscye2**2)*(avg_pay_samp_all_aux**2);

				s21 = sum(s21_temp1,s21_temp2, s21_temp3, s21_temp4, s21_temp5, s21_temp6);
				s22 = sum(s22_temp1,s22_temp2, s22_temp3, s22_temp4, s22_temp5, s22_temp6);

				piece=(1/(p1star**2))*((payments**2)/(projpaid_all**2))*(weight**2)*nall*s21;
				*piece=(1/((weight*&denominator)**2))*(weight**2)*nall*s21;

				piececluster=(1/(p5star**2))*((payments**2)/(projpaid_all**2))*(weight**2)*nall*s22;
				run;

				proc means data = clusterrates noprint missing sum;
				var piece n2 e1star p1star lines claims &numerator &denominator;
				output out=total sum=piece n2 t1 t2 lines claims &numerator &denominator mean=t3 t4 e2star p2star t5 t6 t7 t8;
				run;

				proc means data=clusterrates noprint missing;
				class &contractor_cluster;
				var piececluster n2 e5star p5star lines claims &numerator &denominator;
				output out=clustertotal sum=piececluster n2 t1 t2 lines claims &numerator &denominator mean=t3 t4 e2star p2star t5 t6 t7 t8;
				run;
			
				data clustertotal;set clustertotal; if &contractor_cluster ne  " ";

				data final;
				set total clustertotal;

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

				proc means data=temppaid noprint missing nway;class &strata &partition  &service_type_id &contractor_cluster cid ;
				var &numerator &denominator dummylines &auxiliary;
				output out=claims sum=&numerator &denominator lines &auxiliary;

				proc sort;by &partition &service_type_id &contractor_cluster;
				proc sort data=ratefile2;by &partition  &service_type_id  &contractor_cluster;

				data claims;merge claims(in=a) ratefile2 ;by &partition &service_type_id   &contractor_cluster;if a;
				proc sort;by &partition &strata;run;
				data claims;merge claims(in=a) proj_all_paid;by &partition &strata;if a;
				theta1=&numerator - r3*&denominator;
				theta2=&numerator - r6*&denominator;

				diff1 = &numerator - r3*&denominator-((e4-r3*p4)/projpaid_all)*&denominator;;
				diff2 = &numerator - r6*&denominator-((e4-r6*p4)/projpaid_all)*&denominator;;
				dummyclaims=1;
				run;


				proc means data=claims noprint missing nway;class &strata &partition &service_type_id &contractor_cluster;
				var  &numerator &denominator diff1 diff2 lines dummyclaims theta1 theta2 &auxiliary;
				output out=clusterrates  sum=&numerator &denominator d1 d2 lines claims sum_theta1 sum_theta2 &auxiliary
					n=d5 d6 n3 n4 d7 d10 d22 d23 d24 var= d3 samp_pay_var diff1 diff2 d8 d11 d20 d21 samp_pay_var_aux;



				data clusterrates; merge clusterrates(in=a) weights2; by &strata;if a;
			
				proc sort; by &partition &service_type_id &contractor_cluster;
				data clusterrates;merge clusterrates(in=a) ratefile2; by &partition &service_type_id &contractor_cluster;if a;
				proc sort; by &partition &strata;
				data clusterrates;merge clusterrates(in=a)  proj_all_paid ;by &partition &strata;if a;
				data clusterrates;merge clusterrates(in=a) total_file ;by &partition ;if a;
				kscye1=(e4-r3*p4)/projpaid_all;
				kscye2=(e4-r6*p4)/projpaid_all;

				avg_pay_samp_domain=(&denominator/claims);
				avg_pay_samp_domain_aux =(&auxiliary/claims);

				rate=&numerator/&denominator;

				s21_temp1   =((claims-1)/(nall-1))*diff1 ;
				s21_temp2	=-(kscye1**2)*((claims-1)/(nall-1))*samp_pay_var_aux ;
				s21_temp3 	=(kscye1**2)*var_paid_all_aux*((n_ki-1)/(nall-1)) ;
				s21_temp4	=(claims/(nall-1))*(1-claims/nall)*((sum_theta1/claims)**2) ; 
				s21_temp5 	=2*(claims/(nall-1))*kscye1*(sum_theta1/claims)*(((n_ki)/(nall))*avg_pay_samp_all_aux - avg_pay_samp_domain_aux);
				s21_temp6 	=(n_ki/(nall-1))*(1-n_ki/nall)*(kscye1**2)*(avg_pay_samp_all_aux**2);

				s22_temp1   =((claims-1)/(nall-1))*diff2 ;
				s22_temp2	=-(kscye2**2)*((claims-1)/(nall-1))*samp_pay_var_aux ;
				s22_temp3 	=(kscye2**2)*var_paid_all_aux*((n_ki-1)/(nall-1)) ;
				s22_temp4	=(claims/(nall-1))*(1-claims/nall)*((sum_theta2/claims)**2) ; 
				s22_temp5 	=2*(claims/(nall-1))*kscye2*(sum_theta2/claims)*(((n_ki)/(nall))*avg_pay_samp_all_aux - avg_pay_samp_domain_aux);
				s22_temp6 	=(n_ki/(nall-1))*(1-n_ki/nall)*(kscye2**2)*(avg_pay_samp_all_aux**2);

				s21 = sum(s21_temp1,s21_temp2,s21_temp3,s21_temp4,s21_temp5,s21_temp6);
				s22 = sum(s22_temp1,s22_temp2,s22_temp3,s22_temp4,s22_temp5,s22_temp6);

				piece=(1/(p3star**2))*((payments**2)/(projpaid_all**2))*(weight**2)*nall*s21;
				piececluster=(1/(p6star**2))*((payments**2)/(projpaid_all**2))*(weight**2)*nall*s22;
				run;

data error.clusterrates;
set clusterrates;
run;

				proc sort data = clusterrates tagsort;by &service_type_id;
				proc means data = clusterrates noprint missing;
				by  &service_type_id;
				var piece n4 e3star p3star lines claims &numerator &denominator;
				output out=total sum=piece n4 t1 t2 lines claims &numerator &denominator mean=t3 t4 e4star p4star t5 t6 t7 t8;

				proc sort data=clusterrates tagsort;by &contractor_cluster &service_type_id;
				proc means noprint missing;
				by  &contractor_cluster &service_type_id;
				var piececluster n4 e6star p6star lines claims &numerator &denominator;
				output out=clustertotal sum=piececluster n4 t1 t2 lines claims &numerator &denominator mean=t3 t4 e4star p4star t5 t6 t7 t8;
	

				data finalby;
				set total clustertotal;

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
				if ucl lt .10 then ci95=compress(clcl)||" -    "||left(cucl);
				if ucl ge .10 then ci95=compress(clcl)||" -  "||left(cucl);
				if ucl ge 1 then ci95=compress(clcl)||" -"||left(cucl);

				if &contractor_cluster=" " then &contractor_cluster="zall";
				keep &contractor_cluster &service_type_variable ci95 projerr projpaid samperr samppaid rate sampled_line_items sampled_claims sdtaylor lcl ucl;

				data error.&service_type_variable.&dataset.results;
				set results;
				run;

%mend;

