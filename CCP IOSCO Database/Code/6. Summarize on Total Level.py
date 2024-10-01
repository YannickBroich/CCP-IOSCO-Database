# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 17:10:43 2024

@author: Yannick
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Datei einlesen
file_path = r"C:\Users\Yannick\Desktop\CCP_IOSCO_Database_Summed.xlsx"
df = pd.read_excel(file_path)

# Sicherstellen, dass die notwendigen Spalten vorhanden sind
if 'CCP' not in df.columns or '4.3.15_PreHaircut' not in df.columns or 'ReportDate' not in df.columns:
    raise ValueError("Die notwendigen Spalten 'CCP', '4.3.15_PreHaircut' und 'ReportDate' fehlen in der Datei.")

# Sicherstellen, dass die Datumsspalte als Datumstyp behandelt wird
df['ReportDate'] = pd.to_datetime(df['ReportDate'], errors='coerce')

# Überprüfen, ob die Datumsspalte korrekt konvertiert wurde
if df['ReportDate'].isnull().all():
    raise ValueError("Die Datumsspalte konnte nicht korrekt konvertiert werden.")

# Liniendiagramm erstellen
plt.figure(figsize=(12, 8))

# Einzigartige CCPs finden und für jeden CCP ein Liniendiagramm hinzufügen
ccps = df['CCP'].unique()
for ccp in ccps:
    ccp_data = df[df['CCP'] == ccp].sort_values(by='ReportDate')
    # Fehlende Werte als NaN einfügen, um Linien zu unterbrechen
    ccp_data = ccp_data.set_index('ReportDate').reindex(pd.date_range(start=ccp_data['ReportDate'].min(), end=ccp_data['ReportDate'].max(), freq='D'))
    # Plotten Sie nur die vorhandenen Werte
    plt.plot(ccp_data.index, ccp_data['4.3.15_PreHaircut'], label=ccp, marker='o', linestyle='-', alpha=0.75)

# Plot beschriften und anzeigen
plt.title('Liniendiagramm von 4.3.15_PreHaircut für verschiedene CCPs')
plt.xlabel('Datum')
plt.ylabel('4.3.15_PreHaircut (logarithmisch)')
plt.yscale('log')
plt.legend(title='CCP', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True)
plt.tight_layout()
plt.show()
