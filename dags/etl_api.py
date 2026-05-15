from airflow import DAG
#from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime
import json
import requests

with DAG (
    dag_id = "API_ETL_DAG" , 
    start_date = datetime(2025,5,6),
    schedule= "@daily" , 
    catchup=False

) as dag :
    @task
    def extract():
        response = requests.get("https://dummyjson.com/products")
        data = response.json()
        print("extracted data:" , data)
        return data 
    
    @task
    def transform(data):
        results = []

        for item in data:
            if isinstance(item, dict):
                category = str(item.get("category", "unknown")).upper()
            else:
                category = "UNKNOWN"

            results.append(category)

        return results
    
    @task
    def load(data):
        
        with open("/tmp/name.json" , "w") as f:
            json.dump(data,f) 
            
            
    user_data=extract()
    transformed_data=transform(user_data) 
    load(transformed_data)        