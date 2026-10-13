"""Run with Python having numpy/matplotlib/pymupdf installed and tectonic on PATH."""
from pathlib import Path
import os
import shutil
import subprocess
import sys

if sys.flags.optimize:
    raise SystemExit('Run without -O: document assertions must remain enabled.')

ROOT=Path(__file__).resolve().parent
os.chdir(ROOT)
(ROOT/'qa').mkdir(exist_ok=True)
subprocess.run([sys.executable,'make_figures.py'],check=True)
engine=shutil.which('tectonic')
if not engine:
    raise SystemExit('Install Tectonic and put tectonic on PATH; see README.md.')
subprocess.run([engine,'--keep-logs','--keep-intermediates','main.tex'],check=True)
shutil.copy2('main.pdf','checkers-with-runway-13-white-paper-v2.pdf')
subprocess.run([sys.executable,'check_pdf.py'],check=True)
