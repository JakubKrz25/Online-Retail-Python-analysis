"""Derived tables for the statistical analyses.

Guest purchases (CustomerID == GUEST_ID) are excluded from every customer-level
table: they are many different people merged into one ID and would dominate
any per-customer statistic.
"""
import pandas as pd

from src.cleaning import GUEST_ID


def orders(retail):
    """One row per invoice: date, customer, country, basket value and size."""
    return (retail.groupby("InvoiceNo", observed=True)
                  .agg(InvoiceDate=("InvoiceDate", "first"),
                       InvoiceHour=("InvoiceHour", "first"),
                       CustomerID=("CustomerID", "first"),
                       Country=("Country", "first"),
                       OrderValue=("Total", "sum"),
                       NItems=("Quantity", "sum"),
                       NLines=("StockCode", "size"))
                  .reset_index())


def customers(retail, snapshot_date=None):
    """One row per registered customer with RFM features.

    Recency   = days from the last purchase to snapshot_date
    Frequency = number of distinct invoices
    Monetary  = total revenue
    """
    known = retail.loc[retail["CustomerID"] != GUEST_ID]
    if snapshot_date is None:
        snapshot_date = known["InvoiceDate"].max() + pd.Timedelta(days=1)

    cust = (known.groupby("CustomerID", observed=True)
                 .agg(Country=("Country", lambda s: s.mode().iat[0]),
                      FirstPurchase=("InvoiceDate", "min"),
                      LastPurchase=("InvoiceDate", "max"),
                      Frequency=("InvoiceNo", "nunique"),
                      Monetary=("Total", "sum"),
                      NItems=("Quantity", "sum")))
    cust["Recency"] = (snapshot_date - cust["LastPurchase"]).dt.days
    cust["Tenure"] = (snapshot_date - cust["FirstPurchase"]).dt.days
    cust["AvgOrderValue"] = cust["Monetary"] / cust["Frequency"]
    cust["IsRepeatBuyer"] = cust["Frequency"] > 1
    return cust.reset_index()


def repeat_purchase_dataset(retail, cutoff, horizon_days=90):
    """Features from purchases before `cutoff`, target = buys again within `horizon_days` after it.

    Used in notebooks/05_repeat_purchase.ipynb. Splitting by time avoids leaking
    future information into the features.
    """
    cutoff = pd.Timestamp(cutoff)
    past = retail.loc[retail["InvoiceDate"] < cutoff]
    future = retail.loc[(retail["InvoiceDate"] >= cutoff)
                        & (retail["InvoiceDate"] < cutoff + pd.Timedelta(days=horizon_days))]

    X = customers(past, snapshot_date=cutoff)
    buyers = set(future.loc[future["CustomerID"] != GUEST_ID, "CustomerID"])
    X["BuysAgain"] = X["CustomerID"].isin(buyers)
    return X
