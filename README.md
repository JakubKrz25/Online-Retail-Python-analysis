# Online retail analysis

Analysis of a UK online retailer's transactions (Dec 2010 – Dec 2011) in Python (pandas, NumPy, SciPy, statsmodels).
The project has two layers:

- **Business analysis**: customer behaviour, sales trends, product performance and revenue patterns.
- **Statistical layer**: each analysis follows one chapter of *Practical Statistics for Data Scientists*
  (Bruce, Bruce & Gedeck) and is paired with a **theory notebook** where the method is derived formally
  and checked by simulation against a known ground truth.

**Remark**: This project is a work in progress. Chapters are added as they are completed.

## Structure

```
data/
  raw/             retail.xlsx (not in the repo, see "Data" below)
  processed/       cleaned parquet files written by notebooks/00_cleaning.ipynb
src/
  cleaning.py      cleaning pipeline as functions
  features.py      order-level and customer-level (RFM) tables, repeat-purchase dataset
  stats_utils.py   own implementations of bootstrap, permutation test, Benjamini–Hochberg
notebooks/         applied analyses on the retail data
theory/            derivations + simulations, one per applied notebook
```

| # | Applied notebook | Topic (book chapter) | Theory companion | Status |
|---|---|---|---|---|
| 00 | [Data cleaning](notebooks/00_cleaning.ipynb) | data preparation | – | done |
| 01 | [Sales EDA](notebooks/01_sales_eda.ipynb) | EDA, robust estimation (ch. 1) | [Robust estimation](theory/01_robust_estimation.ipynb) | EDA done, ch. 1 planned |
| 02 | [Bootstrap CIs](notebooks/02_bootstrap_ci.ipynb) | sampling distributions, bootstrap (ch. 2) | [Bootstrap](theory/02_bootstrap.ipynb) | planned |
| 03 | [Hypothesis tests](notebooks/03_hypothesis_tests.ipynb) | tests, multiple testing, power (ch. 3) | [Testing](theory/03_testing.ipynb) | planned |
| 04 | [Regression](notebooks/04_regression.ipynb) | linear regression (ch. 4) | [OLS](theory/04_ols.ipynb) | planned |
| 05 | [Repeat purchase](notebooks/05_repeat_purchase.ipynb) | classification (ch. 5) | [Logistic MLE](theory/05_logistic_mle.ipynb) | planned |

## Findings

### 01 · Sales EDA
- Total revenue: £10.64 mln.
- The three strongest months were September–November 2011, peaking in November (pre-Christmas shopping).
- No transactions on Saturdays and lower sales on Sundays.
- Revenue peaks around the 7th–9th day of the month and between 10:00 and 15:00.

*(each chapter adds a short section here: question → method → result → caveat)*

## Data

This project uses the publicly available [Online Retail dataset](https://archive.ics.uci.edu/dataset/352/online+retail)
(UCI Machine Learning Repository, licensed under CC BY 4.0).
Download `Online Retail.xlsx` and save it as `data/raw/retail.xlsx`.

## How to run

```bash
pip install -r requirements.txt
```

Then run `notebooks/00_cleaning.ipynb` once to create `data/processed/`, after which any other notebook can be run.
