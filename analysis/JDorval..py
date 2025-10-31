import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

annual = pd.read_csv('../data/combined_bank_data_annual.csv')
#print(annual.head())
# 1. What's the total size of your dataset?
print(f"Total rows: {len(annual)}")
print(f"Total columns: {len(annual.columns)}")

# 2. Calculate missing percentages for key columns
missing_pct = (annual.isna().sum() / len(annual) * 100).sort_values(ascending=False)
print("\nTop 20 columns with missing data:")
print(missing_pct.head(20))

# 3. Check if the _QTR_Annual columns should even exist
print("\nColumns with '_QTR_Annual' suffix:")
qtr_annual_cols = [col for col in annual.columns if '_QTR_Annual' in col]
print(qtr_annual_cols)

# 4. Are these duplicate columns? Check if you have both versions:
print("\nDo you have duplicate columns?")
for col in qtr_annual_cols:
    base_name = col.replace('_QTR_Annual', '_Annual')
    if base_name in annual.columns:
        print(f"  {col} AND {base_name} both exist!")