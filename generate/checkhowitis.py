import pandas as pd

df = pd.read_csv("raw_logs.csv")
print(df.head())
print(df["status_code"].value_counts(normalize=True))
