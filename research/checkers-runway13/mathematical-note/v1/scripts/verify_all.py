#!/usr/bin/env python3
"""Public proof replay; does not modify source certificates or run optimization."""
import argparse
from pathlib import Path
import os
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--source-root", type=Path, required=True,
                    help="pinned repository or hash-bound public source subset")
parser.add_argument("--output-dir", type=Path, required=True,
                    help="new directory for fresh receipts")
parser.add_argument("--stage", default="all", choices=["all", "public-tests", "local", "retention", "bounds", "domains", "conditions", "legacy"])
args = parser.parse_args()
runner = Path(__file__).resolve().parents[1] / "verification/reproduce.py"
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", OPENBLAS_NUM_THREADS="1")
env.pop("PYTHONPATH", None)
raise SystemExit(subprocess.call([sys.executable, str(runner), "--source", str(args.source_root.resolve()),
                                 "--output", str(args.output_dir.resolve()), "--stage", args.stage], env=env))
