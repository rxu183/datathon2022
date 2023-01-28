import pandas as pd

df = pd.read_csv("beginner.csv")
cleaned = df[["City","State","Zip Code"]]
updated = cleaned.dropna()
print(updated)
