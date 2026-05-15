import requests
import pandas as pd 
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

CSV_PATH = "/usr/local/airflow/include/data/retail_sales.csv"

API_URL = "https://dummyjson.com/products"

def extract_csv():
    df = pd.read_csv(CSV_PATH)
    return df 

def extract_api():
    session = requests.Session()

    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500,502,503 , 504]
    )
    session.mount("https://" , HTTPAdapter(max_retries=retry))

    headers = {
        "User-Agent" :"Mozilla/5.0"
    }
    response = session.get(API_URL, headers=headers , timeout=20)
    #response = requests.get(API_URL)
    response.raise_for_status()
    data = response.json()
    return pd.DataFrame(data["products"])