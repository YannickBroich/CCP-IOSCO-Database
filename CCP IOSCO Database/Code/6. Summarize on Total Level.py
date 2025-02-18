# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:10:43 2024

@author: Yannick
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


file_path = r"\CCP_IOSCO_Database_Summed.xlsx"
df = pd.read_excel(file_path)


if 'CCP' not in df.columns or '4.3.15_PreHaircut' not in df.columns or 'ReportDate' not in df.columns:
    raise ValueError("The relevant rows 'CCP', '4.3.15_PreHaircut' and 'ReportDate' are missing in the file.")


df['ReportDate'] = pd.to_datetime(df['ReportDate'], errors='coerce')


if df['ReportDate'].isnull().all():
    raise ValueError("Daterow could not be converted.")


plt.figure(figsize=(12, 8))


ccps = df['CCP'].unique()
for ccp in ccps:
    ccp_data = df[df['CCP'] == ccp].sort_values(by='ReportDate')
    
    ccp_data = ccp_data.set_index('ReportDate').reindex(pd.date_range(start=ccp_data['ReportDate'].min(), end=ccp_data['ReportDate'].max(), freq='D'))
    
    plt.plot(ccp_data.index, ccp_data['4.3.15_PreHaircut'], label=ccp, marker='o', linestyle='-', alpha=0.75)


plt.title('Linegraph CCPs')
plt.xlabel('Datum')
plt.ylabel('4.3.15_PreHaircut (logarithmisch)')
plt.yscale('log')
plt.legend(title='CCP', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
