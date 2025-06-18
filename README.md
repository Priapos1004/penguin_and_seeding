# Penguin 🐧 and Seeding 🌱

This Repository is experimenting with GA test-generation in combination with source code analysis.

**IMPORTANT:** Run all the console code in the directory of this readme file.

## Getting Started 🚀

Let's start by installing the necessary packages 📦

Afterwards, you can run the [installation testing notebook](notebooks/installation_testing.ipynb) to see if pynguin works.

### Using `conda`

How to [download conda](https://www.anaconda.com/download).

```
conda create -yn pen_see python=3.10
conda activate pen_see
pip install -e pynguin_0_41_0/.
pip install -r requirements.txt
```

To clean up the environment 🗑️:

```
conda deactivate
conda remove -yn pen_see --all
```

## Folder Structure 🗂️

```text
penguin_and_seeding/
├── .github/workflows/          # GitHub Workflow Configuration
├── documents/                  # Project Planning and Documentation
├── notebooks/                  # Jupyter Notebooks for Experimentation
├── scripts/                    # Python Scripts
|   ├── config.py               # Settings of Environmental Variables
|   └── examples/               # Functions for Benchmarking the Approaches
├── pynguin_0_41_0/             # Cloned Pynguin Repository (Version 0.41.0)
|   ├── README.md               # Documentation of Pynguin
|   └── src/pynguin/            # Pynguin Code
├── .gitignore                  # Files and Directories to Be Excluded from Git Version Control
├── LICENSE                     # License for this Repository
├── requirements.txt            # Library Requirements
├── pyproject.toml              # Configuration of Style Checks
└── README.md
```

## Run Benchmark Script

The configuration for the benchmark run can be changed in [config.py](scripts/config.py).

Afterwards, run the following command:

```shell
python scripts/run_pynguin_benchmark.py
```

*No other scripts besides config.py need to be touched :-)*

## Custom Seeding Strategies

The code for the custom seeding strategies can be found in the [custom_seeding](pynguin_0_41_0/src/pynguin/custom_seeding/__init__.py) directory.

The script [main_seeder.py](pynguin_0_41_0/src/pynguin/custom_seeding/main_seeder.py) is the bridge between the pynguin code and our custom seeding.

The interface for our seeding strategies can be found in [base_strategy.py](pynguin_0_41_0/src/pynguin/custom_seeding/strategy/base_strategy.py). The implementations of this interface are then selectable in [strategy_selector.py](pynguin_0_41_0/src/pynguin/custom_seeding/strategy/strategy_selector.py) and handed-over to [main_seeder.py](pynguin_0_41_0/src/pynguin/custom_seeding/main_seeder.py).

The specification of the information passed down from Pynguin to the seeding strategies is defined in the schema [MainSeederFunctionOutput](pynguin_0_41_0/src/pynguin/custom_seeding/schema/main_seeder_schema.py).

## Code Style 💅

Run `ruff` to find style issues in your code:

```shell
ruff check .
```

You can automatically fix most issues with:

```shell
ruff check . --fix
```

*BUT ALWAYS CHECK THE CHANGES MADE BY RUFF!*
