%macro PrintToLog;

proc printto log = "&log_folder./&log_file_cv";
quit;

%mend PrintToLog;
%macro PrintMessage(message);

options nonotes nomprint nosymbolgen nomlogic;
%PrintToScreen;
data _null_;
put 30*'-' / &message. / 30*'-';
run;
%PrintToLog;
options formdlim="*" compress=yes symbolgen mprint mlogic notes;

%mend PrintMessage;
%macro PrintToScreen;

proc printto;
quit; 

%mend PrintToScreen;