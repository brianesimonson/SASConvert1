from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC_DIRS = [
    ROOT / "Claims Programs",
    ROOT / "Global Macros",
    ROOT / "Reconcile Macro",
    ROOT / "Master Program",
]
OUT_ROOT = ROOT / "claims_python" / "converted_structure"

MACRO_DECL_RE = re.compile(r"%macro\s+([A-Za-z0-9_]+)\s*(\((.*?)\))?\s*;", re.IGNORECASE | re.DOTALL)
MACRO_BLOCK_RE = re.compile(
    r"%macro\s+([A-Za-z0-9_]+)\s*(\((.*?)\))?\s*;(.*?)%mend(?:\s+[A-Za-z0-9_]+)?\s*;",
    re.IGNORECASE | re.DOTALL,
)
INCLUDE_RE = re.compile(r"%include\s+\"([^\"]+)\"", re.IGNORECASE)


def snake(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s or "module"


def py_safe(name: str) -> str:
    out = snake(name)
    if out and out[0].isdigit():
        out = f"m_{out}"
    return out


def esc_triple(text: str) -> str:
    return text.replace('"""', '\\"\\"\\"')


def convert_file(src: Path, dst: Path) -> None:
    text = src.read_text(errors="ignore")
    rel = src.relative_to(ROOT)

    macro_args: dict[str, list[str]] = {}
    for m in MACRO_DECL_RE.finditer(text):
        name = m.group(1)
        arg_raw = (m.group(3) or "").strip()
        args = [a.strip() for a in arg_raw.split(",") if a.strip()] if arg_raw else []
        macro_args[name.lower()] = args

    macro_blocks: dict[str, str] = {}
    for m in MACRO_BLOCK_RE.finditer(text):
        name = m.group(1)
        body = m.group(4).strip("\n")
        macro_blocks[name.lower()] = body

    includes = INCLUDE_RE.findall(text)

    lines: list[str] = []
    lines.append('"""Auto-generated SAS->Python structural conversion module.')
    lines.append("")
    lines.append(f"Source: {rel}")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("from ...transpiled_runtime import run_transpiled_macro, run_transpiled_program")
    lines.append("")

    if includes:
        lines.append("INCLUDES = [")
        for inc in includes:
            lines.append(f'    "{inc}",')
        lines.append("]")
        lines.append("")

    if macro_args:
        for name_lower, args in macro_args.items():
            macro_name = next(k for k in macro_args.keys() if k == name_lower)
            # recover original case best-effort
            match = re.search(rf"%macro\s+({re.escape(macro_name)})", text, re.IGNORECASE)
            orig_name = match.group(1) if match else macro_name

            fn = py_safe(orig_name)
            arg_sig = ", ".join(f"{py_safe(a)}: Any = None" for a in args)
            if arg_sig:
                arg_sig += ", "
            block = macro_blocks.get(name_lower, "")
            lines.append(f"def {fn}({arg_sig}*args: Any, **kwargs: Any):")
            lines.append(f'    """Converted entrypoint for SAS macro %{orig_name}."""')
            lines.append("    _arguments = {")
            for a in args:
                lines.append(f'        "{a}": {py_safe(a)},')
            lines.append("        " + '"args": args,')
            lines.append("        " + '"kwargs": kwargs,')
            lines.append("    }")
            lines.append("    _sas_block = \"\"\"" + esc_triple(block) + "\"\"\"")
            lines.append(
                f'    return run_transpiled_macro(source_file="{rel}", macro_name="{orig_name}", arguments=_arguments, sas_block=_sas_block)'
            )
            lines.append("")
    else:
        lines.append("def run_program(*args: Any, **kwargs: Any):")
        lines.append('    """Program entrypoint for SAS file without %macro declarations."""')
        lines.append("    _sas_block = \"\"\"" + esc_triple(text) + "\"\"\"")
        lines.append(f'    return run_transpiled_program(source_file="{rel}", sas_block=_sas_block)')

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(lines) + "\n")


def write_init(package_dir: Path) -> None:
    init = package_dir / "__init__.py"
    children = sorted([p for p in package_dir.iterdir() if p.is_file() and p.suffix == ".py" and p.name != "__init__.py"])
    lines = ['"""Auto-generated package for converted SAS structure."""', ""]
    if children:
        for child in children:
            mod = child.stem
            lines.append(f"from . import {mod}  # noqa: F401")
        lines.append("")
    init.write_text("\n".join(lines) + "\n")


def main() -> None:
    if OUT_ROOT.exists():
        for p in sorted(OUT_ROOT.rglob("*.py"), reverse=True):
            p.unlink()

    top_subpackages: set[Path] = set()
    for src_dir in SRC_DIRS:
        sub_pkg = OUT_ROOT / py_safe(src_dir.name)
        sub_pkg.mkdir(parents=True, exist_ok=True)
        top_subpackages.add(sub_pkg)
        for src in sorted(src_dir.glob("*.sas")):
            dst = sub_pkg / f"{py_safe(src.stem)}.py"
            convert_file(src, dst)
        write_init(sub_pkg)

    lines = ['"""Structure mirror modules generated from SAS sources."""', ""]
    for sub_pkg in sorted(top_subpackages):
        lines.append(f"from . import {sub_pkg.name}  # noqa: F401")
    lines.append("")
    (OUT_ROOT / "__init__.py").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
