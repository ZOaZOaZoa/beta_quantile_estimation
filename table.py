import numpy as np
import pandas as pd
from scipy.special import betaincinv
from tqdm import tqdm

first = 0.1
last = 100
total = 100
probability = 0.95

table = []
a_list = b_list = np.linspace(first, last, total).tolist()
for a in tqdm(a_list, leave=False):
    row = []
    for b in b_list:
        row += [betaincinv(a, b, probability),]
    table += [row, ]

table_df = pd.DataFrame(table, columns=b_list, index=a_list)
table_df.to_excel('betincinv_table.xlsx')