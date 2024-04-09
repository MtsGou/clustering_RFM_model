import pickle
import pandas as pd
import streamlit as st
from pipeline_data import pipeline

st.set_page_config(page_title="RFM clustering for business strategy", page_icon = './img/icon.png')

st.sidebar.header('File Submit')
st.sidebar.write('Use this page to get the clusters for your customers, based on your CSV file.')

st.title("Predict your RFM clusters")

st.markdown("Get the hierarchical clustering model for your business submitting your CSV file:")

# MODEL

# Load model
with open('./model/model_cluster.pkl', 'rb') as file:
    cluster_model = pickle.load(file)

# Load model
with open('./model/PCA.pkl', 'rb') as file:
    PCA_model = pickle.load(file)

upload = st.file_uploader("Upload your sales file (.csv).", type = ['csv'])

st.markdown('''Specify columns \"InvoiceNo\",\"Quantity\",\"InvoiceDate\",\"UnitPrice\" ,\"CustomerID\".

    Use '%m/%d/%Y %H:%M\' format for date.

    ''')

if upload:
    df_input = pd.read_csv(upload, sep=",", encoding="ISO-8859-1")
    pipeline_results = pipeline(df_input.copy())
    data = pipeline_results[0]
    rfm = pipeline_results[1]

    #st.dataframe(data=rfm)

    cluster_labels = cluster_model.fit_predict(data.drop(columns=['CustomerID']))
    data['cluster_label'] = cluster_labels
    prediction = data[['CustomerID', 'cluster_label']]
    pca=PCA_model.fit_transform(data.drop(columns = ['CustomerID', 'cluster_label']))

    df_output = prediction

    # Show dataset with cluster label
    st.markdown('## Clusters found for your customers: ')

    st.dataframe(data=df_output.iloc[0:100,:], width=200,use_container_width=True)

    # Show dataset with analysis per cluster
    st.markdown('## Check the RFM for each cluster: ')
    analysis = pd.merge(data, rfm, on = 'CustomerID').drop(columns = [0, 1, 2])
    analysis = analysis[['R (days)', 'F', 'M (R$)', 'cluster_label']]\
            .groupby('cluster_label')\
            .agg('mean')
    
    st.dataframe(data=analysis)
    
    # Plot chart for the user
    st.markdown('## View your data points and check the clusters found:')

    pc_df=pd.DataFrame(data=pca, columns=['P1', 'P2'])
    pc_df['labels']=data['cluster_label'].astype(str)
    #fig = sns.scatterplot(data=pc_df,x='P1',y='P2',hue='labels')
    st.scatter_chart(pc_df, x='P1',y='P2', color='labels', height=500)

    st.download_button(label = 'Download CSV', data = df_output.to_csv(index=False), 
                       mime = 'text/csv', file_name = 'RFM_clustering.csv')