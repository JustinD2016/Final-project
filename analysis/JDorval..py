import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv(r'data\bank_innovation_dataset_FINAL.csv')
print("Sparceness of the dataset: ", len(data[data.isnull() > 0.9])/len(data))