from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class TranspiledCall:
    source_file: str
    macro_name: str
    arguments: dict[str, Any]
    sas_block: str


def run_transpiled_macro(source_file: str, macro_name: str, arguments: dict[str, Any], sas_block: str) -> TranspiledCall:
    """Execute a transpiled macro call.

    Current behavior returns a structured call object so callers can inspect,
    test, and progressively replace SAS-text execution with native Python logic.
    """
    return TranspiledCall(
        source_file=source_file,
        macro_name=macro_name,
        arguments=arguments,
        sas_block=sas_block,
    )


def run_transpiled_program(source_file: str, sas_block: str) -> TranspiledCall:
    return run_transpiled_macro(source_file=source_file, macro_name="__program__", arguments={}, sas_block=sas_block)


def write_artifact(path: str | Path, content: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content, encoding="utf-8")
    return out
