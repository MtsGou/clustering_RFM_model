import numpy as np
import pandas as pd

# To save model
import pickle

# Load dataset
df = pd.read_csv('./data/data.csv', sep=",", encoding="ISO-8859-1")

# Save as json
json = df.to_json('./data/input_data.json', orient='records', lines=True)
