import numpy as np
import pandas as pd
from scipy.special import betaincinv
from tqdm import tqdm

table = []
a_list = b_list = np.linspace(0.1, 100, 250).tolist()
for a in tqdm(a_list, leave=False):
    row = []
    for b in b_list:
        row += [betaincinv(a, b, 0.95),]
    table += [row, ]

table_df = pd.DataFrame(table, columns=b_list, index=a_list)
table_df.to_excel('betincinv_table.xlsx')