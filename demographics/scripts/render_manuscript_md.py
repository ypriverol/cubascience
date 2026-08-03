#!/usr/bin/env python3
"""
Generate the web-facing Markdown manuscripts from the LaTeX sources.

The Spanish manuscript is a scientific mirror of the English one, so both now
live in LaTeX and the Markdown that the site serves is derived rather than
hand-maintained. That is the whole point: a hand-written Markdown copy drifted
from the LaTeX in the previous revision (the methodological note still carried a
superseded ~38k mortality residual while the body said ~77k).

Requires pandoc on PATH.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MS = ROOT / "manuscript"

TARGETS = [
    ("es", MS / "es" / "latex" / "main.tex", MS / "es" / "cuba-despoblacion-2021-2026.md"),
    ("en", MS / "en" / "latex" / "main.tex", MS / "en" / "cuba-depopulation-2021-2026.md"),
]

TEMPLATE = Path(__file__).resolve().parent / "templates" / "manuscript.gfm"
# Both manuscripts share one bibliography; the Spanish LaTeX points at it too.
REFS = MS / "en" / "latex" / "refs.bib"
ABSTRACT_TITLE = {"es": "Resumen", "en": "Abstract"}

HEADER = {
    "es": (
        "> **Generado automáticamente** desde `latex/main.tex` por "
        "`scripts/render_manuscript_md.py`. No editar a mano: los cambios se pierden.\n"
        "> Versión maquetada (PDF): `Cuba_despoblacion_2021-2026_manuscrito.pdf`.\n"
        "> Preprint; no revisado por pares. Código y datos: "
        "<https://github.com/ypriverol/cubascience> (`demographics/`).\n"
    ),
    "en": (
        "> **Auto-generated** from `latex/main.tex` by "
        "`scripts/render_manuscript_md.py`. Do not edit by hand; changes are lost.\n"
        "> Typeset version (PDF): `cuba-depopulation-2021-2026.pdf`.\n"
        "> Preprint; not peer reviewed. Code and data: "
        "<https://github.com/ypriverol/cubascience> (`demographics/`).\n"
    ),
}


def _fix_figure_paths(md: str) -> str:
    """Point image links at ../../figures/, where the PNGs actually live."""
    return re.sub(r"\]\((?!\.\./|https?:)([^)]*?\.png)\)", r"](../../figures/\1)", md)


def render(lang: str, tex: Path, out: Path) -> Path:
    md = subprocess.run(
        # --standalone keeps \title and the abstract, which pandoc otherwise
        # drops as metadata and silently omits from the body. The explicit
        # template avoids pandoc's default YAML block, which would publish the
        # absolute local path of refs.bib.
        ["pandoc", "-f", "latex", "-t", "gfm", "--wrap=none", "--standalone",
         "--template", str(TEMPLATE),
         "-M", f"abstract-title={ABSTRACT_TITLE[lang]}",
         "--bibliography", str(REFS), "--citeproc", str(tex)],
        capture_output=True, text=True, check=True,
    ).stdout
    out.write_text(HEADER[lang] + "\n" + _fix_figure_paths(md), encoding="utf-8")
    return out


def main() -> None:
    if shutil.which("pandoc") is None:
        raise SystemExit("pandoc not found on PATH")
    for lang, tex, out in TARGETS:
        if not tex.exists():
            print(f"skip {lang}: {tex} missing", file=sys.stderr)
            continue
        print("wrote", render(lang, tex, out))


if __name__ == "__main__":
    main()
