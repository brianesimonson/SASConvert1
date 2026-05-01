"""Auto-generated SAS->Python structural conversion module.

Source: Reconcile Macro/PrintMessage_Macro.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

def printtolog(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %PrintToLog."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """proc printto log = "&log_folder./&log_file_cv";
quit;"""
    return run_transpiled_macro(source_file="Reconcile Macro/PrintMessage_Macro.sas", macro_name="PrintToLog", arguments=_arguments, sas_block=_sas_block)

def printmessage(message: Any = None, *args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %PrintMessage."""
    _arguments = {
        "message": message,
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """options nonotes nomprint nosymbolgen nomlogic;
%PrintToScreen;
data _null_;
put 30*'-' / &message. / 30*'-';
run;
%PrintToLog;
options formdlim="*" compress=yes symbolgen mprint mlogic notes;"""
    return run_transpiled_macro(source_file="Reconcile Macro/PrintMessage_Macro.sas", macro_name="PrintMessage", arguments=_arguments, sas_block=_sas_block)

def printtoscreen(*args: Any, **kwargs: Any):
    """Converted entrypoint for SAS macro %PrintToScreen."""
    _arguments = {
        "args": args,
        "kwargs": kwargs,
    }
    _sas_block = """proc printto;
quit; """
    return run_transpiled_macro(source_file="Reconcile Macro/PrintMessage_Macro.sas", macro_name="PrintToScreen", arguments=_arguments, sas_block=_sas_block)

