# Data Wrangling
import numpy as np
import pandas as pd
import calendar
import datetime as dt

# normalization and scaler
from sklearn.preprocessing import StandardScaler

def pipeline(df):
    # df new required data 
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

    # Correct float type
    rfm['M (R$)'] = rfm['M (R$)'].astype(float)

    rfm = rfm[rfm['M (R$)'] < rfm['M (R$)'].quantile(.95)]
    rfm = rfm[rfm['F'] < rfm['F'].quantile(.99)]

    # Correct index
    rfm = rfm.reset_index().drop(columns = 'index')

    # Scale data - standard scaler
    scaler = StandardScaler()
    df_rfm_scaled = scaler.fit_transform(rfm.set_index('CustomerID')[['R (days)', 'F', 'M (R$)']])

    df_rfm_scaled = pd.DataFrame(df_rfm_scaled)

    rfm_scaled = pd.merge(rfm, df_rfm_scaled, left_index=True, right_index=True)\
        .drop(columns = ['R (days)', 'F', 'M (R$)'])
    
    return rfm_scaled, rfm