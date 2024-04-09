import pickle
import uvicorn
import pandas as pd
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel
from pipeline_data import pipeline

# Init API
app = FastAPI()

data_cluster = None
rfm = None

# Load model
with open('./model/model_cluster.pkl', 'rb') as file:
    cluster_model = pickle.load(file)

# Home
@app.get('/')
def home():
    return 'Welcome to the RFM cluster Prediction API!Check /info to see project description and explanatory.'

# Description
@app.get('/info')
def info():
    return 'This is a hierarchical cluster model to categorize customers in a company based'\
         + 'in RFM (recency, frequency, monetary).' \
         + 'Use data specifying variables \"InvoiceNo\",\"Quantity\",'\
         + '\"InvoiceDate\",\"UnitPrice\" ,\"CustomerID\", using \'%m/%d/%Y %H:%M\' format for date.'\
         + '/predict - for cluster prediction for the customers. /cluster_analysis - for cluster analysis'



# Template data
class Sale(BaseModel):
    InvoiceNo: str
    Quantity: int
    InvoiceDate: str
    UnitPrice: float
    CustomerID: int
    class Config:
        schema_extra = {
        'example': {
        'InvoiceNo': '536365',
        'Quantity':6,
        'InvoiceDate':'12/1/2010 8:26',
        'UnitPrice':2.55,
        'CustomerID':17850
        }
    }

class SaleList(BaseModel):
    data: List[Sale]

# Multiple prediction
@app.post('/predict')
def predict(data: SaleList):
    df_input = pd.DataFrame(data.dict()['data'])
    global data_cluster
    global rfm
    data_cluster = pipeline(df_input)[0]
    rfm = pipeline(df_input)[1]

    cluster_labels = cluster_model.fit_predict(data_cluster.drop(columns=['CustomerID']))
    data_cluster['cluster_label'] = cluster_labels
    prediction = data_cluster[['CustomerID', 'cluster_label']]

    return prediction.to_json()

# Analysis on clusters
@app.post('/cluster_analysis')
def analysis():
    global data
    global rfm

    if (data is not None):
        analysis = pd.merge(data, rfm, on = 'CustomerID').drop(columns = [0, 1, 2])
        analysis = analysis[['R (days)', 'F', 'M (R$)', 'cluster_label']]\
            .groupby('cluster_label')\
            .agg('mean')
        return analysis.to_json()
    else:
        return "No data submitted. Send to /predict first."


# API main execution
if __name__ == '__main__':
    uvicorn.run(app)