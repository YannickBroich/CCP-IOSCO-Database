# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 13:43:03 2024

@author: Yannick
"""

import pandas as pd


file_path = r"C:\{Your Path}\CCP IOSCO Database - Arbeitsversion\Database\CCP_IOSCO_Database2.xlsx"


df = pd.read_excel(file_path)


df['4.1.1'] = pd.to_numeric(df['4.1.1'], errors='coerce')
df['4.1.2'] = pd.to_numeric(df['4.1.2'], errors='coerce')


numeric_columns = df.select_dtypes(include=['number']).columns.tolist()


summed_df = df.groupby(['CCP', 'ReportDate'])[numeric_columns].sum().reset_index()


output_file_path = r"C:\{Your Path}\CCP_IOSCO_Database_Summed.xlsx"
summed_df.to_excel(output_file_path, index=False)

print("Summierung abgeschlossen und Datei gespeichert unter:", output_file_path)
