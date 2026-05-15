def validate_sales(df):

    required = [
        "sale_id",
        "product_id",
        "customer_id",
        "quantity",
        "price",
        "sale_date"
    ]

    for col in required:
        if col not in df.columns:
            raise Exception(f"Missing column: {col}")

    if df.isnull().sum().sum() > 0:
        raise Exception("Null values found")

    print(f"[VALIDATION OK] Sales rows: {len(df)}")


def validate_products(df):

    if "id" not in df.columns:
        raise Exception("Missing product id")

    print(f"[VALIDATION OK] Products rows: {len(df)}")