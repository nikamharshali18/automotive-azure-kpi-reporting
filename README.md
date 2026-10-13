# Automotive Azure KPI Reporting

Beginner-friendly sample project for automotive production, sales, and quality reporting using Python/PySpark, Azure Data Factory, ADLS Gen2, Delta Lake, SQL, and Power BI.

## Project status
This repository contains sample data, local KPI logic and tests, Databricks notebook templates, and Azure/Power BI setup guides. Azure resources and Power BI reports must be configured in your own subscription/workspace; this repository is not pre-deployed.

## Architecture
CSV sources → ADF → ADLS Gen2 Bronze → Databricks/PySpark → Silver Delta → Gold KPI outputs → Power BI.

## Quick start (local tests)
Requires Python 3.10+ and Git.
```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest
python -m automotive_kpi.cli --data-dir data/source
```

If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that terminal, then activate again.

## Expected sample KPIs
- Produced: 2,500
- Production target: 2,650
- Achievement: 94.34%
- Sold: 500
- Revenue: 684,000,000 illustrative currency units
- Inspected: 2,500
- Defects: 50
- Defect rate: 2.00%

## Folder guide
- `data/source/`: synthetic CSV input files.
- `src/automotive_kpi/`: runnable local Python KPI implementation.
- `tests/`: automated tests.
- `databricks/notebooks/`: PySpark/Delta notebook scripts; update ADLS paths before running in Databricks.
- `sql/`: reporting query examples.
- `adf/`: pipeline configuration guide.
- `powerbi/`: dashboard/DAX guide.
- `docs/`: project design and test documentation.

## Security
Never commit passwords, Azure keys, tokens, `.env` files, or confidential data. Use managed identity or an approved secret-management method in Azure.
