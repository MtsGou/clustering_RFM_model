import streamlit as st

st.set_page_config(page_title="What is RFM?", page_icon = './img/icon.png')

st.title("What is RFM?")
st.sidebar.write('About RFM and its strategies, as well as targeting marketing.')

st.markdown('''RFM stands for Recency, Frequency and Monetary. For each customer, each of these three values ​​are obtained. 
Recency stands for the number of days since the customer's last purchase. Frequency tells how many purchases the customer has made since registering. 
And finally, Monetary represents how much the customer spends on purchases, for example, the average value of transactions. 
''')

st.image("./img/RFM.png")

st.markdown('''
This technique is widely used by companies to help develop business strategies, as it allows them to better understand customers, using an approach known as Targeting Marketing, 
which consists of mapping and classifying customers, with the aim of retaining and rewarding the most regular customers and also attracting those who may not become customers.
In this project, the RFM clusters allow us to classify each client's profile into four groups, and it is up to the company to analyze each cluster and understand what each one represents. 
To achieve this, this application also shows the average RFM value for each of the clusters, for a given data sample.
''')
