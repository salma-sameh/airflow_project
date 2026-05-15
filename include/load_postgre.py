import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook


def incremental_load_sales(df):

    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cursor = conn.cursor()

    cursor.execute("SELECT sale_id FROM fact_sales")
    existing = {r[0] for r in cursor.fetchall()}

    new_df = df[~df["sale_id"].isin(existing)]

    for _, row in new_df.iterrows():
        cursor.execute("""
            INSERT INTO fact_sales
            (sale_id, product_id, customer_id, quantity, price, sale_date)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, tuple(row))

    conn.commit()

    print(f"[LOAD] Inserted {len(new_df)} sales rows")


def incremental_load_products(df):

    hook = PostgresHook(postgres_conn_id="postgres_dw")
    conn = hook.get_conn()
    cursor = conn.cursor()

    df = df.rename(columns={"id": "product_id"})

    cursor.execute("SELECT product_id FROM dim_products")
    existing = {r[0] for r in cursor.fetchall()}

    new_df = df[~df["product_id"].isin(existing)]

    for _, row in new_df.iterrows():
        cursor.execute("""
            INSERT INTO dim_products
            (product_id, title, category, price)
            VALUES (%s,%s,%s,%s)
        """, (
             row["product_id"],
                row["title"],
                row["category"],
                row["price"]
        ))

    conn.commit()

    print(f"[LOAD] Inserted {len(new_df)} product rows")