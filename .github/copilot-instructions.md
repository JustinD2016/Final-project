## Purpose

This file gives concise, actionable guidance for AI coding agents to be immediately productive in this repository.

## Quick project summary

- Project type: data-analysis / reproducible report. Core artifacts live under `analysis/` (Jupyter notebooks), `data/` (CSV datasets), and `report/` (Quarto `.qmd`).
- Primary goal: analyze combined bank datasets (2010–2021) to develop an "Innovation" score as described in `README.md`.

## Key files and folders (use these as entry points)

- `analysis/` — exploratory and analysis notebooks. Notable files: `Jdorval.ipynb`, `eda_gw.ipynb`.
  - Note: `analysis/Jdorval.ipynb` contains a code cell that imports numpy/pandas/matplotlib and reads a CSV using an absolute Windows path.
- `data/` — source CSVs: `bank_innovation_dataset_FINAL_ENRICHED.csv`, `bank_registry.csv`, `wrds_bank_data_MERGED_2010-2015.csv`, `wrds_bank_data_MERGED_2016-2021.csv`.
- `report/` — Quarto report sources, entry `report/index.qmd` and `_quarto.yml`.
- `help.py` — small utility; inspect before changing behavior that other scripts rely on.

## Project-specific patterns and gotchas

- Notebooks are the working source of truth. Changes to analysis should update notebooks and, when relevant, extract stable scripts/helpers (e.g., into `help.py`).
- Several notebooks use absolute Windows file paths (example in `analysis/Jdorval.ipynb`): prefer converting those to relative paths under `data/` so runs are reproducible:
  - Replace: r"C:\\Users\\jdorv\\Coding Fun\\Bank Innovation\\wrds_bank_data_MERGED.csv"
  - With: `data/wrds_bank_data_MERGED_2010-2015.csv` or `data/wrds_bank_data_MERGED_2016-2021.csv` or `data/bank_innovation_dataset_FINAL_ENRICHED.csv` depending on intent.
- Prefer editing notebooks in a Jupyter environment (or VS Code Notebook UI) and ensure cell-order runs cleanly from top to bottom after changes.

## Dependencies & environment (observable from code)

- Notebooks import: `numpy`, `pandas`, `matplotlib`. Quarto is used for report rendering.
- There is no `requirements.txt` in the repository—before running notebooks, ensure a Python env with at least:
  - pandas, numpy, matplotlib, jupyterlab (or jupyter), and `quarto` installed for rendering the report.

## Common tasks / how to approach them

- To run/iterate on a notebook:
  1. Open `analysis/<notebook>.ipynb` in Jupyter or VS Code Notebook.
  2. Update any absolute data path to a relative `data/` path.
  3. Run cells top-to-bottom and fix import/path errors.
- To update the report: edit `report/index.qmd` then render with Quarto (locally): `quarto render report` (Quarto must be installed).

## Examples (concrete snippets you will see and should follow)

- Reading data (convert absolute -> relative):

  - Current example in `analysis/Jdorval.ipynb`:
    data = pd.read_csv(r'C:\\Users\\jdorv\\Coding Fun\\Bank Innovation\\wrds_bank_data_MERGED.csv')

  - Replace with (preferred):
    data = pd.read_csv("../data/wrds_bank_data_MERGED_2010-2015.csv")

- Notebook imports (common top-of-notebook block):
  import numpy as np
  import pandas as pd
  import matplotlib.pyplot as plt

## When editing code

- Keep changes minimal in-place in notebooks; when logic needs re-use, extract to `help.py` or a new module and import from notebooks and scripts.
- Don't assume a requirements file—when adding libraries, also add a minimal `requirements.txt` or `environment.yml` and note it in the README.

## Integration & external dependencies

- Data are local CSVs in `data/` (no remote download code found). If you add connectors (WRDS, S3, etc.), document credentials and secure them outside this repo.
- Rendering uses Quarto—make sure Quarto is available for report generation.

## Missing/unknowns to ask the maintainer

- Preferred Python environment (conda/venv) and exact dependency versions.
- Are there canonical combined WRDS files (single merged file) to prefer over the two `wrds_bank_data_MERGED_*` files?

## If something is unclear

- Start by running the top cells in the relevant notebook (e.g., `analysis/Jdorval.ipynb`) and fix path/import errors. If you need to change the project's data layout, ask the maintainer before moving files.

---
Please review and tell me if you'd like me to (a) add a `requirements.txt`, (b) convert absolute paths in notebooks to relative automatically, or (c) add small unit tests / CI scaffolding for notebook execution.
