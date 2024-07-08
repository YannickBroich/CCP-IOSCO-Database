# -*- coding: utf-8 -*-
"""
Created on Thu May 2 14:12:56 2024

Author: User
"""

import pandas as pd
import re

file_path = r"{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Databasepreconversion.xlsx"
df = pd.read_excel(file_path)

# Exchangerate as of 29.4.2024
conversion_rates = {
        'AUD': 0.62,
        'BLR': 0.28,
        'BRL': 0.17,
        'CAD': 0.68,
        'CHF': 1.03,    
        'CLP': 0.00099,
        'CNH': 0.1278,
        'CNY': 0.13,
        'COP': 0.00023,
        'CZ': 0.04,
        'DKK': 0.13,
        'EUR': 1,
        'EURO': 1,
        'GBP': 1.18,
        'HKD': 0.12,
        'HRK': 0.13,
        'HUF': 0.0025,
        'ILS': 0.24,
        'INR': 0.011,
        'JPY': 0.0057,
        'KRW': 0.00067,
        'MXN': 0.051,
        'NOK': 0.087,
        'NZD': 0.57,
        'PLN': 0.23,
        'SEK': 0.088,
        'SGD': 0.68,
        'THB': 0.025,
        'TRY': 0.028,
        'TWD': 0.028,
        'USD': 0.92,
        'ZAR': 0.051
}

def get_currency_code(row):
    if pd.notna(row['Currency']) and row['Currency'] in conversion_rates:
        return row['Currency']
   # elif row['Currency'] in ['ETD', 'OTC'] and pd.notna(row['Description']):
        #for code in conversion_rates:
            #if re.search(r'\b' + re.escape(code) + r'\b', row['Description']):
                #return code
    return None 

def convert_currency(amount, src_currency, target_currency='EUR'):
    if src_currency and src_currency in conversion_rates and target_currency in conversion_rates:
        converted_amount = amount * conversion_rates[src_currency]
        return converted_amount
    return amount

columns_to_convert = [col for col in df.columns[7:300]]  

for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')

for col in columns_to_convert:
    df[col] = df.apply(lambda row: convert_currency(row[col], get_currency_code(row)), axis=1)

# Drop the "Description" column
#df.drop(columns=['Description'], inplace=True)

output_path = r"{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Database.xlsx"
df.to_excel(output_path, index=False)
