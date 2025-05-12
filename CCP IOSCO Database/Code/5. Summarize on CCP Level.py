# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:43:03 2024

@author: Yannick
"""

import pandas as pd
from openpyxl import load_workbook


file_path = r"C:\{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Database - II Converted into Euro.xlsx"
wb = load_workbook(file_path, data_only=True, read_only=True)
ws = wb['Sheet1']

data = list(ws.values)
columns = data[0]
rows = data[1:]
df = pd.DataFrame(rows, columns=columns)


df['ReportDate'] = pd.to_datetime(df['ReportDate'], errors='coerce')
df = df.dropna(subset=['ReportDate'])
df['Quarter'] = df['ReportDate'].dt.to_period('Q').astype(str)


for col in df.columns:
    if col not in ['CCP', 'Quarter', 'ReportDate']:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')


df.drop(columns=['ClearingService', 'DefaultFund', 'Currency'], inplace=True, errors='ignore')


numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
aggregated = df.groupby(['CCP', 'Quarter'], as_index=False)[numeric_cols].sum(min_count=1)


output_path = r"C:\{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Database - III On CCP Level.xlsx"
aggregated.to_excel(output_path, index=False)

