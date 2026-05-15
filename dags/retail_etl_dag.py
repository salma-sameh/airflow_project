from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

from include.extract import extract_csv, extract_api
from include.transform import transform_sales, transform_products
from include.validate import validate_sales, validate_products
from include.load_postgre import incremental_load_sales, incremental_load_products


default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="retail_etl_postgre",
    start_date=datetime(2024, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    default_args=default_args,
    tags=["retail", "postgre", "etl"]
) as dag:

    def run_sales():
        df = extract_csv()
        df = transform_sales(df)
        validate_sales(df)
        incremental_load_sales(df)

    def run_products():
        df = extract_api()
        df = transform_products(df)
        validate_products(df)
        incremental_load_products(df)

    sales_task = PythonOperator(
        task_id="sales_pipeline",
        python_callable=run_sales
    )

    product_task = PythonOperator(
        task_id="product_pipeline",
        python_callable=run_products
    )

    [sales_task, product_task]