import pandas as pd
from sklearn.utils import resample

# Wczytaj dane
data_file = "02-16-2018.csv"  # Replace with your file path
df = pd.read_csv(data_file, low_memory=False)

# Podstawowe informacje


# Usuwanie brakujących wartości
df_cleaned = df.dropna()

# Usuwanie duplikatów
df_cleaned = df_cleaned.drop_duplicates()

# Usuwanie wybranych kolumn (tylko jeśli istnieją)
columns_to_drop = ['Fwd PSH Flags', 'Bwd PSH Flags', 'Fwd URG Flags', 'Bwd URG Flags', 
                   'CWE Flag Count', 'Fwd Byts/b Avg', 'Fwd Pkts/b Avg', 'Fwd Blk Rate Avg',
                   'Bwd Byts/b Avg', 'Bwd Pkts/b Avg', 'Bwd Blk Rate Avg']
df_cleaned = df_cleaned.drop(columns=[col for col in columns_to_drop if col in df_cleaned.columns])

print(df_cleaned.info())


# Analiza kolumny 'Label'
print("\nUnikalne wartości w kolumnie 'Label':")
print(df_cleaned['Label'].value_counts())

# Zapisanie oczyszczonego zbioru danych
df_cleaned.to_csv("cleaned_data.csv", index=False)
print("\nOczyszczony zbiór danych zapisano do 'cleaned_data.csv'.")
