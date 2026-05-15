from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import json


#task 1
def extract():
    data = {
        "name" : "Ali" ,
        "age"   : 24 ,
        "city" : "cairo"
    }
    print("extracted data:" , data)
    return data 

# task 2 transform
def transform(ti):
    data = ti.xcom_pull(task_ids = "extract_data")
    data["age"]+=5
    print("transformation completed" , data)
    return data 


# task 3 load 
def load(ti):
    data = ti.xcom_pull(task_ids = "transform_data")
    with open("/tmp/output.json" , "w") as f:
        json.dump(data,f) 
        
        
with DAG (
    dag_id = "etl_simple",
    start_date = datetime(2025, 5 ,5),
    schedule = "*/2 * * * *"  ,
    catchup = False   
    
)as dag :
    task1 = PythonOperator(
        task_id = "extract_data" ,
        python_callable = extract 
    )
    
    task2 = PythonOperator(
        task_id = "transform_data" , 
        python_callable = transform
    )   
    
    task3 = PythonOperator(
        task_id ="load_data", 
        python_callable = load
    )     
        
    task1 >> task2 >> task3    