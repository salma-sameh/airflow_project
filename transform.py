import pandas as pd 
import json 

def transform_sales(df):
    df.columns = [c.lower().strip() for c in df.columns]
    df = df.drop_duplicates()
    df = df.dropna()

    df["sale_id"]     = df["sale_id"].astype(int)
    df["customer_id"] = df["customer_id"].astype(int)
    df["quantity"]    = df["quantity"].astype(int)
    df["price"]       = df["price"].astype(float)

    return df 

def transform_products(df):
    df.columns = [c.lower().strip() for c in df.columns]
    for col in df.columns:
        df[col] = df[col].apply(
            lambda x: json.dumps(x) if isinstance(x , (dict , list)) else x
        )

    df = df.drop_duplicates()
    df = df.fillna("UNknown")

    return df     

