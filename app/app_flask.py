import pickle
import pandas as pd
from flask import Flask, request
from pipeline_data import pipeline

app = Flask(__name__)

data = None
rfm = None

# Load model
with open('./model/model_cluster.pkl', 'rb') as file:
    cluster_model = pickle.load(file)

# Home
@app.route('/', methods=['GET'])
def home():
    return '''Welcome to the RFM cluster Prediction API! 
    
    Check /info to see project description and explanatory.
    '''

# Description
@app.route('/info', methods=['GET'])
def info():
    return '''
    This is a hierarchical cluster model to categorize customers in a company based in RFM
    (recency, frequency, monetary). Use data specifying variables "InvoiceNo","Quantity","InvoiceDate","UnitPrice" ,"CustomerID", 
    using \'%m/%d/%Y %H:%M\' format for date.
    
    /predict - for cluster prediction for the customers
    /cluster_analysis - for cluster analysis
    '''

# Prediction
@app.route('/predict', methods=['POST'])
def predict():
    data_json = request.get_json()['data']
    df = pd.DataFrame(data_json)
    global data
    global rfm
    data = pipeline(df)[0]
    rfm = pipeline(df)[1]

    cluster_labels = cluster_model.fit_predict(data.drop(columns=['CustomerID']))
    data['cluster_label'] = cluster_labels
    prediction = data[['CustomerID', 'cluster_label']]

    return prediction.to_json()

# Analysis on clusters
@app.route('/cluster_analysis', methods=['POST'])
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

if __name__ == '__main__':
    app.run()
