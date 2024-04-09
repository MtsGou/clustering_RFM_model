import streamlit as st

st.set_page_config(
    page_title = "RFM Clustering",
    page_icon = "./img/icon.png"
)

st.sidebar.header('Description')
st.sidebar.write('For more information, check \'What is Clustering?\' and \'What is RFM?\'.')

st.write("# Welcome to RFM clustering app!")
st.write("\n\n")

st.image("./plots/agglomerative3d.png")
st.write("\n\n")

st.markdown('''
This is a hierarchical cluster model to categorize customers in a company based in RFM (recency, frequency, monetary). This was made using data that specifies variables "InvoiceNo","Quantity","InvoiceDate","UnitPrice" ,"CustomerID", 
using \'%m/%d/%Y %H:%M\' format for date.

RFM stands for Recency, Frequency and Monetary. For each customer, each of these three values ​​are obtained. 

Recency stands for the number of days since the customer's last purchase. Frequency tells how many purchases the customer has made since registering. 

And finally, Monetary represents how much the customer spends on purchases, for example, the average value of transactions.

For more information, check \'What is Clustering?\' and \'What is RFM?\' pages.''')

st.success('Check other pages')
st.markdown('<a href="app">Application</a>', unsafe_allow_html=True)
st.markdown('<a href="what_is_clustering">About clustering</a>', unsafe_allow_html=True)
st.markdown('<a href="what_is_RFM">About RFM</a>', unsafe_allow_html=True)
