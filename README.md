# Penguin 🐧 and Seeding 🌱

This Repository is experimenting with GA test-generation in combination with source code analysis.

**IMPORTANT:** Run all the console code in the directory of this readme file.

## Getting Started 🚀

Let's start by installing the necessary packages 📦

Afterwards, you can run the [installation testing notebook](notebooks/installation_testing.ipynb) to see if pynguin and fuzzingbook work.

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
penguin_and_fuzzingbook/
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
