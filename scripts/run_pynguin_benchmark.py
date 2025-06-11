import os
import sys
import subprocess
import webbrowser
from pynguin.configuration import Configuration, TestCaseOutputConfiguration, ExportStrategy
from pynguin.generator import set_configuration, run_pynguin

EXAMPLES_DIR = "examples"
RESULTS_DIR = "pynguin_results"
HTMLCOV_DIR = "htmlcov"

def ensure_directories():
    os.makedirs(RESULTS_DIR, exist_ok=True)

def find_python_modules(directory):
    """Returns list of tuples: (module_name, module_path)"""
    py_files = [f for f in os.listdir(directory) if f.endswith(".py")]
    modules = []
    for file in py_files:
        mod_name = file[:-3]  # remove .py
        modules.append((mod_name, os.path.join(directory, file)))
    return modules

def run_pynguin_on_module(module_name, budget_seconds=30):
    print(f"\n▶ Running Pynguin on module: {module_name}")
    output_config = TestCaseOutputConfiguration(
        export_strategy=ExportStrategy.PY_TEST,
        format_with_black=True,
        output_path=RESULTS_DIR
    )
    cfg = Configuration(
        project_path=".",
        module_name=f"{EXAMPLES_DIR}.{module_name}",
        test_case_output=output_config
    )

    cfg.stopping.maximum_search_time = budget_seconds

    set_configuration(cfg)
    rc = run_pynguin()
    print(f"Pynguin return code for {module_name}: {rc}")

def run_tests_and_coverage():
    cmd = [
        sys.executable, "-m", "coverage", "run",
        "--source", EXAMPLES_DIR,
        "-m", "pytest", RESULTS_DIR, "-q"
    ]
    print("▶ Running:", " ".join(cmd))
    proc = subprocess.run(cmd, capture_output=True, text=True)

    print(proc.stdout)
    if proc.returncode != 0:
        print("─── STDERR ───", file=sys.stderr)
        print(proc.stderr, file=sys.stderr)
        raise RuntimeError(f"pytest failed with exit code {proc.returncode}")

def generate_coverage_report():
    print("\nTests passed. Generating coverage report…\n")
    subprocess.run([sys.executable, "-m", "coverage", "report", "-m"], check=True)
    subprocess.run([sys.executable, "-m", "coverage", "html", "-d", HTMLCOV_DIR], check=True)

def open_coverage_in_browser():
    abs_path = os.path.abspath(os.path.join(HTMLCOV_DIR, "index.html"))
    file_url = f"file://{abs_path}"
    print(f"\nFile URL:\n{file_url}")
    webbrowser.open(file_url)

def main():
    ensure_directories()
    modules = find_python_modules(EXAMPLES_DIR)

    # 1. Generate tests for all modules
    for mod_name, _ in modules:
        run_pynguin_on_module(mod_name)

    # 2. Run all tests in one coverage run
    run_tests_and_coverage()

    # 3. Generate and display coverage report
    generate_coverage_report()
    open_coverage_in_browser()

if __name__ == "__main__":
    main()
