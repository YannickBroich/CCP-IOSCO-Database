# -*- coding: utf-8 -*-
"""
Created on Fri Apr 18 13:08:45 2025

@author: Yannick
"""

import pandas as pd


file_path = r"C:{Your Path}\CCP IOSCO Database\Database\Database\CCP_IOSCO_Database - III On CCP Level.xlsx"
df = pd.read_excel(file_path)


drop_keywords = ['percentage', 'percent', 'date', 'time', 'day', 'effective', 'maturity']
numeric_cols = df.select_dtypes(include='number').columns.tolist()
filtered_cols = [col for col in numeric_cols if not any(kw in col.lower() for kw in drop_keywords)]


df_eu = df.groupby('Quarter')[filtered_cols].sum(min_count=1).reset_index()


output_path = r"C:{Your Path}\CCP IOSCO Database\Database\Database\CCP_IOSCO_Database - IV On EU Level.xlsx"
df_eu.to_excel(output_path, index=False)

print(output_path)

print("File saved successfully:")
print(output_path)
