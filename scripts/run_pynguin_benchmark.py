"""Script to run Pynguin on all Python modules in a directory, generate tests, and report coverage."""
import logging
import os
import subprocess
import sys
import webbrowser

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
    os.makedirs(experiment_settings.RESULTS_DIR, exist_ok=True)

def find_python_modules(directory):
    """Returns list of tuples: (module_name, module_path)"""
    py_files = [f for f in os.listdir(directory) if f.endswith(".py")]
    modules = []
    for file in py_files:
        mod_name = file[:-3]  # remove .py
        modules.append((mod_name, os.path.join(directory, file)))
    return modules

def run_pynguin_on_module(module_name, strategy: str | None, budget_seconds: int):
    logger.info(f"▶ Running Pynguin on module: {module_name}")
    output_config = TestCaseOutputConfiguration(
        export_strategy=ExportStrategy.PY_TEST,
        format_with_black=True,
        output_path=experiment_settings.RESULTS_DIR
    )

    parent_module = experiment_settings.EXAMPLES_DIR.replace("/", ".")
    cfg = Configuration(
        project_path=".",
        module_name=f"{parent_module}.{module_name}",
        test_case_output=output_config
    )

    cfg.stopping.maximum_search_time = budget_seconds
    if isinstance(strategy, str):
        cfg.seeding.initial_population_seeding = True
        cfg.seeding.initial_population_strategy = strategy

    set_configuration(cfg)
    rc = run_pynguin()
    logger.debug(f"Pynguin return code for {module_name}: {rc}")

def run_tests_and_coverage():
    parent_module = experiment_settings.EXAMPLES_DIR.replace("/", ".")
    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--source", parent_module,
        "-m", "pytest", experiment_settings.RESULTS_DIR, "-q"
    ]
    logger.debug("▶ Running:", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)

    logger.debug(proc.stdout)
    if proc.returncode != 0:
        print("─── STDERR ───", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")

def generate_coverage_report():
    logger.info("Tests passed. Generating coverage report…\n")
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], check=True)
    subprocess.run([sys.executable, "-m", "coverage", "html", "-d", experiment_settings.HTMLCOV_DIR], check=True)

def open_coverage_in_browser():
    abs_path = os.path.abspath(os.path.join(experiment_settings.HTMLCOV_DIR, "index.html"))
    file_url = f"file://{abs_path}"
    logger.info(f"File URL:\n{file_url}")
    webbrowser.open(file_url)

def main(strategy: str | None, budget_seconds: int):
    ensure_directories()
    modules = find_python_modules(experiment_settings.EXAMPLES_DIR)

    # 1. Generate tests for all modules
    for mod_name, _ in modules:
        run_pynguin_on_module(mod_name, strategy=strategy, budget_seconds=budget_seconds)

    # 2. Run all tests in one coverage run
    run_tests_and_coverage()

    # 3. Generate and display coverage report
    generate_coverage_report()
    open_coverage_in_browser()

if __name__ == "__main__":
    main(
        strategy=experiment_settings.CUSTOM_SEEDING_STRATEGY,
        budget_seconds=experiment_settings.BUDGET_PER_FILE_IN_SECONDS
    )
