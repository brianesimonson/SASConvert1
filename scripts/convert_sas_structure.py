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

MACRO_RE = re.compile(r"%macro\s+([A-Za-z0-9_]+)\s*(\((.*?)\))?\s*;", re.IGNORECASE | re.DOTALL)
INCLUDE_RE = re.compile(r"%include\s+\"([^\"]+)\"", re.IGNORECASE)


def snake(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", name).strip("_").lower()
    return s or "module"


def py_safe(name: str) -> str:
    out = snake(name)
    if out and out[0].isdigit():
        out = f"m_{out}"
    return out


def convert_file(src: Path, dst: Path) -> None:
    text = src.read_text(errors="ignore")
    rel = src.relative_to(ROOT)

    macros = []
    for m in MACRO_RE.finditer(text):
        name = m.group(1)
        arg_raw = (m.group(3) or "").strip()
        args = [a.strip() for a in arg_raw.split(",") if a.strip()] if arg_raw else []
        macros.append((name, args))

    includes = INCLUDE_RE.findall(text)

    lines: list[str] = []
    lines.append('"""Auto-generated structure mirror from SAS source.')
    lines.append("")
    lines.append(f"Source: {rel}")
    lines.append('"""')
    lines.append("")
    lines.append("from __future__ import annotations")
    lines.append("")
    lines.append("from typing import Any")
    lines.append("")
    lines.append("")

    if includes:
        lines.append("INCLUDES = [")
        for inc in includes:
            lines.append(f'    "{inc}",')
        lines.append("]")
        lines.append("")

    if macros:
        for macro_name, macro_args in macros:
            fn = py_safe(macro_name)
            arg_sig = ", ".join(f"{py_safe(a)}: Any = None" for a in macro_args)
            if arg_sig:
                arg_sig += ", "
            lines.append(f"def {fn}({arg_sig}*args: Any, **kwargs: Any) -> None:")
            lines.append(f'    """Converted entrypoint for SAS macro %{macro_name}."""')
            lines.append("    raise NotImplementedError(")
            lines.append(f'        "Macro %{macro_name} from {rel} has not been fully ported yet."')
            lines.append("    )")
            lines.append("")
    else:
        lines.append("def run_program(*args: Any, **kwargs: Any) -> None:")
        lines.append('    """Placeholder for SAS program without explicit %macro definitions."""')
        lines.append("    raise NotImplementedError(")
        lines.append(f'        "Program {rel} has not been fully ported yet."')
        lines.append("    )")

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

    # top-level init
    lines = ['"""Structure mirror modules generated from SAS sources."""', ""]
    for sub_pkg in sorted(top_subpackages):
        lines.append(f"from . import {sub_pkg.name}  # noqa: F401")
    lines.append("")
    (OUT_ROOT / "__init__.py").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
