# Data Wrangling
import numpy as np
import pandas as pd
from sklearn.preprocessing import scale
import calendar
import datetime as dt

# To save model
import pickle

# normalization and scaler
from sklearn.preprocessing import StandardScaler, scale

# model
from sklearn.decomposition import PCA
import scipy.cluster.hierarchy as shc
from sklearn.cluster import AgglomerativeClustering

from sklearn.pipeline import make_pipeline


# Load dataset
df = pd.read_csv('./data/data.csv', sep=",", encoding="ISO-8859-1")

# Drop NaN values
df.dropna(inplace = True);

# Drop negative values
df = df.query("Quantity > 0 and UnitPrice > 0")

# Drop duplicated rows
df = df.drop_duplicates()

# Data types correction
df['CustomerID'] = df['CustomerID'].astype('int').astype('string')

# Drop distant outliers
df = df.query('Quantity < 3500')
df = df.query('UnitPrice < 2000')

# Feature engineering - add total price column
df['TotalPrice'] = df['Quantity']*df['UnitPrice']

# Reset index
df.reset_index(inplace=True)

# Datetime type correction
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], format='%m/%d/%Y %H:%M')

# Only relevant columns
df = df[['CustomerID', 'InvoiceNo', 'InvoiceDate', 'TotalPrice']]

# Last date for recency calculation
last_date = max(df['InvoiceDate'])

# RFM dataset
rfm = df.groupby(['CustomerID', 'InvoiceNo','InvoiceDate'])['TotalPrice'].agg('sum').reset_index()
rfm['R (days)'] = last_date - rfm['InvoiceDate']
rfm = (
    rfm.groupby('CustomerID')
    .agg({'R (days)' : np.min, 'CustomerID': 'count', 'TotalPrice': 'mean'})
)

rfm['R (days)'] = rfm['R (days)'].apply(lambda x: x.days)

rfm['TotalPrice'] = rfm['TotalPrice'].apply(lambda x: "{:.2f}".format(x))
rfm.rename(columns = {'CustomerID':'F', 'TotalPrice': 'M (R$)'}, inplace = True)

rfm.reset_index(inplace=True)

# Correction float type
rfm['M (R$)'] = rfm['M (R$)'].astype(float)

# Outlier filtering
rfm = rfm[rfm['M (R$)'] < rfm['M (R$)'].quantile(.95)]
rfm = rfm[rfm['F'] < rfm['F'].quantile(.99)]

rfm = rfm.reset_index().drop(columns = 'index')

scaler = StandardScaler()
df_rfm_scaled = scaler.fit_transform(rfm.set_index('CustomerID')[['R (days)', 'F', 'M (R$)']])

df_rfm_scaled = pd.DataFrame(df_rfm_scaled)

rfm_scaled = pd.merge(rfm, df_rfm_scaled, left_index=True, right_index=True).drop(columns = ['R (days)', 'F', 'M (R$)'])

# Hierarchical model agglomerative
cluster = AgglomerativeClustering(n_clusters=4) 
cluster_labels = cluster.fit_predict(rfm_scaled.drop(columns=['CustomerID']))
rfm_scaled['cluster_number'] = cluster_labels

# PCA model
pca=PCA(n_components=2)
pc=pca.fit_transform(rfm_scaled.drop(columns = ['CustomerID', 'cluster_number']))

#agg_pipeline = make_pipeline(StandardScaler(), cluster)
#PCA_pipeline = make_pipeline(StandardScaler(), pca)

with open('./model/model_cluster.pkl', 'wb') as file_model:
    pickle.dump(cluster, file_model)

with open('./model/PCA.pkl', 'wb') as file_model:
    pickle.dump(pca, file_model)