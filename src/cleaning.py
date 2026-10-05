"""Cleaning steps from notebooks/00_cleaning.ipynb, as reusable functions.

Usage:
    from src.cleaning import load_raw, clean
    retail, returns, accounting_adj = clean(load_raw())
"""
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = ROOT / "data" / "raw" / "retail.xlsx"
PROCESSED_DIR = ROOT / "data" / "processed"

GUEST_ID = 1  # CustomerID assigned to purchases made without a customer account

CATEGORY_COLS = ["InvoiceNo", "StockCode", "Description"]
DTYPES = {"Quantity": "Int32", "CustomerID": "Int16", **{c: "category" for c in CATEGORY_COLS}}


def load_raw(path=RAW_PATH):
    return pd.read_excel(path)


def clean(raw):
    """Return (retail, returns, accounting_adj) following the steps of 00_cleaning."""
    df = raw.copy()
    df["Description"] = df["Description"].fillna("Unspecified")
    df["CustomerID"] = df["CustomerID"].fillna(GUEST_ID)

    accounting_adj = df.loc[df["UnitPrice"] < 0]
    df = df.loc[df["UnitPrice"] > 0]  # also drops UnitPrice == 0 (incomplete records)

    returns = df.loc[df["Quantity"] < 0]
    df = df.loc[df["Quantity"] > 0]

    df = df.astype(DTYPES).drop_duplicates(keep="first", ignore_index=True)
    returns = returns.astype(DTYPES)
    accounting_adj = accounting_adj.astype(DTYPES)

    df = df.assign(Total=df["Quantity"] * df["UnitPrice"])
    df["InvoiceHour"] = df["InvoiceDate"].dt.hour.astype("Int8")
    df["InvoiceDate"] = df["InvoiceDate"].dt.normalize()

    cols = ["StockCode", "Description", "UnitPrice", "Quantity", "Total",
            "CustomerID", "InvoiceNo", "InvoiceDate", "InvoiceHour", "Country"]
    return df[cols], returns, accounting_adj


def save_processed(retail, returns, accounting_adj, out_dir=PROCESSED_DIR):
    out_dir.mkdir(parents=True, exist_ok=True)
    retail.to_parquet(out_dir / "retail.parquet")
    returns.to_parquet(out_dir / "returns.parquet")
    accounting_adj.to_parquet(out_dir / "accounting_adj.parquet")


def load_processed(name="retail", in_dir=PROCESSED_DIR):
    return pd.read_parquet(in_dir / f"{name}.parquet")
