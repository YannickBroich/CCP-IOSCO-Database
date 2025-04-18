# -*- coding: utf-8 -*-
"""
Created on Thu May 2 14:12:56 2024
Updated on Apr 18 2025: Uses ECB rates with fallback

Author: Yannick
"""

import pandas as pd
import re
import requests
import xml.etree.ElementTree as ET


def fetch_ecb_rates():
    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    response = requests.get(url)
    tree = ET.fromstring(response.content)
    namespaces = {'ns': 'http://www.ecb.int/vocabulary/2002-08-01/eurofxref'}
    cube = tree.find('.//ns:Cube/ns:Cube', namespaces)

    rates = {'EUR': 1.0, 'EURO': 1.0}
    for currency in cube:
        code = currency.attrib['currency']
        rate = float(currency.attrib['rate'])
        rates[code] = 1 / rate  
    return rates

#fallback rates as of 18.04.2025
def fetch_ecb_rates_with_fallback():
    fallback_rates = {
        'AUD': 0.56,
        'BLR': 0.28, #Belarusian Rubel - currently no reliable data available
        'BRL': 0.17,
        'CAD': 0.68,
        'CHF': 1.0743,
        'CLP': 0.00099,
        'CNH': 0.1278,
        'CNY': 0.12,
        'COP': 0.00023,
        'CZK': 0.04,
        'DKK': 0.13,
        'EUR': 1.0,
        'EURO': 1.0,
        'GBP': 1.1672,
        'HKD': 0.1132,
        'HRK': 0.1327,
        'HUF': 0.0025,
        'ILS': 0.24,
        'INR': 0.011,
        'JPY': 0.006,
        'KRW': 0.00067,
        'MXN': 0.0528,
        'NOK': 0.087,
        'NZD': 0.521,
        'PLN': 0.23,
        'SEK': 0.0878,
        'SGD': 0.679,
        'THB': 0.0253,
        'TRY': 0.0295,
        'TWD': 0.0291,
        'USD': 0.87,
        'ZAR': 0.0489
    }

    rates = fetch_ecb_rates()
    for k, v in fallback_rates.items():
        if k not in rates:
            rates[k] = v
    return rates


conversion_rates = fetch_ecb_rates_with_fallback()


file_path = r"C:\{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Databasepreconversion.xlsx"
df = pd.read_excel(file_path)


def get_currency_code(row):
    if pd.notna(row['Currency']) and row['Currency'] in conversion_rates:
        return row['Currency']
    return None 

def convert_currency(amount, src_currency, target_currency='EUR'):
    if src_currency and src_currency in conversion_rates and target_currency in conversion_rates:
        return amount * conversion_rates[src_currency]
    return amount


columns_to_convert = [col for col in df.columns[7:300]]  

for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')


for col in columns_to_convert:
    df[col] = df.apply(lambda row: convert_currency(row[col], get_currency_code(row)), axis=1)


output_path = r"C:\{Your Path}\CCP IOSCO Database\Database\CCP_IOSCO_Database.xlsx"
df.to_excel(output_path, index=False)
