import streamlit as st

st.set_page_config(page_title="What is clustering?", page_icon = './img/icon.png')

st.title("What is clustering?")
st.sidebar.write('Understand clustering and how it can be useful for your business.')

st.markdown('''Often, when working with data, it is interesting to look for groups or collections within the samples. 
''')

st.image("./img/clustering.png")

st.markdown('''This way, patterns can be found that help to better understand the data, a business or the phenomenon studied. 
Grouping data points using artificial intelligence helps to understand more about them, and can help in making strategies in a business.
For this, machine learning algorithms are used to perform these groupings. 
To achieve this, no labels are used to compare with the results obtained by the algorithm, that is, the examples are unlabeled. This practice is called clustering.''')
