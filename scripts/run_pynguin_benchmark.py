"""Script to run Pynguin on all Python modules in a directory, generate tests, and report coverage."""
import json
import logging
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pandas as pd
from config import experiment_settings
from logging_config import setup_logging
from pynguin.configuration import (
    Configuration,
    ExportStrategy,
    TestCaseOutputConfiguration,
)
from pynguin.generator import run_pynguin, set_configuration

setup_logging(
    focus_on=experiment_settings.FOCUS_ON_LOGGING
)

logger = logging.getLogger(__name__)

def ensure_directories():
    results_dir = Path(experiment_settings.RESULTS_DIR)
    if results_dir.exists():
        shutil.rmtree(results_dir)
    results_dir.mkdir(parents=True, exist_ok=True)

def find_python_modules(directory: str) -> list[tuple[str, str]]:
    """
    Recursively find all .py files under `directory` and return
    a list of (module_name, module_path) tuples.

    module_name is the relative path from `directory` with path
    separators replaced by dots, and without the .py suffix.

    e.g. if directory="/proj/src" and you have "/proj/src/foo/bar/baz.py",
    you'll get ("foo.bar.baz", "/proj/src/foo/bar/baz.py").
    """
    root = Path(directory)
    modules: list[tuple[str, str]] = []
    for path in root.rglob("*.py"):
        # Optional: skip __init__.py if you don’t want package modules
        if path.name == "__init__.py":
            continue

        # Compute the “dotted” module name
        rel = path.relative_to(root).with_suffix("")  # e.g. foo/bar/baz
        mod_name = ".".join(rel.parts)               # e.g. foo.bar.baz

        modules.append((mod_name, str(path)))
    return modules

def run_pynguin_on_module(module_name, strategy: str | None, budget_seconds: int, seed: int):
    print()
    logger.info(f"▶ Running Pynguin on module: {module_name}")
    output_config = TestCaseOutputConfiguration(
        export_strategy=ExportStrategy.PY_TEST,
        format_with_black=False,
        output_path=experiment_settings.RESULTS_DIR
    )

    parent_module = experiment_settings.EXAMPLES_DIR.replace("/", ".")
    cfg = Configuration(
        project_path=".",
        module_name=f"{parent_module}.{module_name}",
        test_case_output=output_config
    )

    cfg.seeding.seed = seed
    cfg.stopping.maximum_search_time = budget_seconds
    if isinstance(strategy, str):
        cfg.seeding.initial_population_seeding = True
        cfg.seeding.initial_population_strategy = strategy

    set_configuration(cfg)
    rc = run_pynguin()
    if rc != 0:
        logger.warning("Pynguin run failed with exit code %d for module %s", rc, module_name)

def run_tests_and_coverage() -> bool:
    parent_module = experiment_settings.EXAMPLES_DIR.replace("/", ".")
    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--source", parent_module,
        "-m", "pytest", experiment_settings.RESULTS_DIR, "-q"
    ]
    logger.debug("▶ Running:", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)

    logger.debug(proc.stdout)
    if proc.returncode == 5:
        logger.warning("No tests found in %s", experiment_settings.RESULTS_DIR)
        return False
    elif proc.returncode != 0:
        print("─── STDERR ───", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")
    else:
        return True

def generate_coverage_report(strategy: str | None, budget_seconds: int, seed: int):
    logger.info("Generating JSON coverage report")

    # Generate JSON report from coverage
    json_report_path = experiment_settings.JSON_DIR + f"/coverage__{strategy}__{budget_seconds}__{seed}.json"
    subprocess.run([
        sys.executable, "-m", "coverage", "json", "-o", json_report_path, "-q"
    ], check=True)

    logger.info(f"JSON coverage report saved to: {json_report_path}")

def merge_coverage_reports() -> pd.DataFrame:
    json_dir_path = Path(experiment_settings.JSON_DIR)
    
    # Pattern to match filenames like: coverage__strategy__budget__seed.json
    pattern = re.compile(r"coverage__(.*?)__(\d+)__(\d+)\.json")
    
    records = []

    for json_file in json_dir_path.glob("coverage__*__*__*.json"):
        match = pattern.match(json_file.name)
        if not match:
            continue

        strategy, budget_seconds, seed = match.groups()
        budget_seconds = int(budget_seconds)
        seed = int(seed)

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)

            timestamp = data.get("meta", {}).get("timestamp")

            for file_name, file_data in data.get("files", {}).items():
                record = {
                    "file_name": file_name,
                    "summary_num_statements": file_data.get("summary", {}).get("num_statements"),
                    "summary_missing_lines": file_data.get("summary", {}).get("missing_lines"),
                    "summary_excluded_lines": file_data.get("summary", {}).get("excluded_lines"),
                    "summary_percent_covered": file_data.get("summary", {}).get("percent_covered"),
                    "budget_seconds": budget_seconds,
                    "seed": seed,
                    "strategy": strategy,
                    "timestamp": timestamp
                }
                records.append(record)

        except Exception as e:
            print(f"Failed to process {json_file}: {e}")

    return pd.DataFrame(records)

def main(strategies: list[str | None], budget_seconds: int, seeds: list[int]):
    start_time = time.perf_counter()
    modules = find_python_modules(experiment_settings.EXAMPLES_DIR)
    if not modules:
        logger.warning(
            "No Python modules found in the specified directory '%s'.",
            experiment_settings.EXAMPLES_DIR
        )
        return

    for strategy in strategies:
        for seed in seeds:
            ensure_directories()
            logger.info("Starting Pynguin benchmark with strategy: '%s', budget: %d seconds, seed: %d", strategy, budget_seconds, seed)
            # 1. Generate tests for all modules
            for mod_name, _ in modules:
                run_pynguin_on_module(
                    mod_name,
                    strategy=strategy,
                    budget_seconds=budget_seconds,
                    seed=seed
                )

            # 2. Run all tests in one coverage run
            coverage_successful = run_tests_and_coverage()

            # 3. Generate and display coverage report
            if coverage_successful:
                generate_coverage_report(
                    strategy=strategy,
                    budget_seconds=budget_seconds,
                    seed=seed
                )
            print("\n\n")
    
    logger.info("All modules processed -> Merging coverage reports.")
    merged_reports = merge_coverage_reports()
    logger.info("Save merged coverage reports to CSV and Excel files.")
    merged_reports.to_csv(
        experiment_settings.JSON_DIR + "/merged_coverage_reports.csv",
        index=False
    )
    merged_reports.to_excel(
        experiment_settings.JSON_DIR + "/merged_coverage_reports.xlsx",
        index=False
    )
    logger.info(
        "Pynguin benchmark completed in %.2f seconds.",
        time.perf_counter() - start_time
    )

if __name__ == "__main__":
    main(
        strategies=experiment_settings.CUSTOM_SEEDING_STRATEGIES,
        budget_seconds=experiment_settings.BUDGET_PER_FILE_IN_SECONDS,
        seeds=experiment_settings.RANDOM_SEEDS
    )
