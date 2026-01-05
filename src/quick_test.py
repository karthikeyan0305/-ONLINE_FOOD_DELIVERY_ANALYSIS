import pandas as pd

df = pd.read_csv("data/raw/ONINE_FOOD_DELIVERY_ANALYSIS.csv")
print("CSV Loaded")
print(df.head())
print(df.columns)
