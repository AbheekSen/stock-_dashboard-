"""
run_pipeline.py
----------------
Master runner — executes all 5 pipeline steps in sequence.

Usage:
    python run_pipeline.py                # Full pipeline
    python run_pipeline.py --steps 1 2   # Run only steps 1 and 2
    python run_pipeline.py --steps 3 4 5 # Run steps 3–5 (data already fetched)
"""

import subprocess
import sys
import time
import argparse
import os

STEPS = [
    (1, "scripts/01_data_ingestion.py",     "Data Ingestion"),
    (2, "scripts/02_feature_engineering.py","Feature Engineering"),
    (3, "scripts/03_comparative_analysis.py","Comparative Analysis"),
    (4, "scripts/04_charts.py",             "Charts & Dashboard"),
    (5, "scripts/05_powerbi_export.py",     "Power BI Export"),
]

def run_step(script, label):
    print(f"\n{'─'*55}")
    print(f"  Running: {label}")
    print(f"{'─'*55}")
    start = time.time()
    result = subprocess.run([sys.executable, script], capture_output=False)
    elapsed = time.time() - start
    if result.returncode == 0:
        print(f"\n  ✔  {label} completed in {elapsed:.1f}s")
        return True
    else:
        print(f"\n  ✖  {label} FAILED (exit code {result.returncode})")
        return False


def main():
    parser = argparse.ArgumentParser(description="Stock Dashboard Pipeline Runner")
    parser.add_argument("--steps", nargs="+", type=int, default=[1,2,3,4,5],
                        help="Steps to run (default: all)")
    args = parser.parse_args()

    os.makedirs("data", exist_ok=True)
    os.makedirs("outputs", exist_ok=True)
    os.makedirs("outputs/charts", exist_ok=True)

    selected = [s for s in STEPS if s[0] in args.steps]

    print("=" * 55)
    print("  Stock Market Dashboard — Full Pipeline")
    print("=" * 55)
    print(f"\n  Steps to run: {[s[0] for s in selected]}")

    pipeline_start = time.time()
    failed = []

    for step_num, script, label in selected:
        ok = run_step(script, f"Step {step_num}: {label}")
        if not ok:
            failed.append(step_num)
            print(f"\n  [WARN] Step {step_num} failed. Continuing with remaining steps...")

    total = time.time() - pipeline_start

    print(f"\n{'='*55}")
    print(f"  Pipeline complete in {total:.1f}s")
    if failed:
        print(f"  Failed steps: {failed}")
    else:
        print("  All steps succeeded ✔")
    print(f"{'='*55}")
    print("\n  Outputs:")
    for path in [
        "data/market_data.db",
        "outputs/01_raw_data.xlsx",
        "outputs/02_indicators.xlsx",
        "outputs/03_comparative_analysis.xlsx",
        "outputs/powerbi_dataset.xlsx",
        "outputs/dashboard.html",
        "outputs/charts/",
    ]:
        exists = os.path.exists(path)
        mark = "✔" if exists else "✖"
        print(f"  {mark}  {path}")


if __name__ == "__main__":
    main()
