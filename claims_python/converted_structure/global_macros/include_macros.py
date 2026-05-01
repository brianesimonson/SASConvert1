"""Auto-generated SAS->Python structural conversion module.

Source: Global Macros/include macros.sas
"""

from __future__ import annotations

from typing import Any
from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program

INCLUDES = [
    "&mainpath./Global Macros/raterun_Stage1 level and national overall.sas",
    "&mainpath./Global Macros/combined ratio estimator.sas",
    "&mainpath./Global Macros/double_ratio_estimator.sas",
    "&mainpath./Global Macros/combined ratio estimator 2.sas",
]

def run_program(*args: Any, **kwargs: Any):
    """Program entrypoint for SAS file without %macro declarations."""
    _sas_block = """* 8/6/2024 -- CC: updated syntax based on new Linux system requirements
* 08/24/2012 -- SL : Change the reference for the double_ratio_estimator ;
* 11/7/2012 -- CC: added a sort into combined ratio estimator called combined ratio estimator 2;

%include "&mainpath./Global Macros/raterun_Stage1 level and national overall.sas"/source2;

%include "&mainpath./Global Macros/combined ratio estimator.sas"/source2;

%include "&mainpath./Global Macros/double_ratio_estimator.sas"/source2;

%include "&mainpath./Global Macros/combined ratio estimator 2.sas"/source2;
"""
    return run_transpiled_program(source_file="Global Macros/include macros.sas", sas_block=_sas_block)
