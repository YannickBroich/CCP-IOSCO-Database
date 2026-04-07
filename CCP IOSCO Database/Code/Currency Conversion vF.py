

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

#fallback rates as of 07.04.2026
def fetch_ecb_rates_with_fallback():
    fallback_rates = {
        'AUD': 0.5963,
        'BLR': 0.28,    #Belarusian Ruble - currently no reliable data available
        'BRL': 0.1674,
        'CAD': 0.6238,
        'CHF': 1.0854,
        'CLP': 0.000952, #not ECB; approx 1 EUR ≈ 1050 CLP
        'CNH': 0.1258,   #not ECB; treated as CNY (offshore yuan)
        'CNY': 0.1258,
        'COP': 0.000233, #not ECB; approx 1 EUR ≈ 4300 COP
        'CZK': 0.04075,
        'DKK': 0.1338,
        'EUR': 1.0,
        'EURO': 1.0,
        'GBP': 1.1461,
        'HKD': 0.1107,
        'HRK': 0.1327,   #Croatian Kuna - Croatia joined eurozone Jan 2023, legacy only
        'HUF': 0.002605,
        'ILS': 0.2752,
        'INR': 0.009320,
        'JPY': 0.005437,
        'KRW': 0.000572,
        'MXN': 0.04837,
        'NOK': 0.0891,
        'NZD': 0.4953,
        'PLN': 0.2333,
        'SEK': 0.0913,
        'SGD': 0.6741,
        'THB': 0.02648,
        'TRY': 0.01950,
        'TWD': 0.02696,  #not ECB; approx 1 EUR ≈ 37.1 TWD
        'USD': 0.8677,
        'ZAR': 0.0510
    }

    rates = fetch_ecb_rates()
    for k, v in fallback_rates.items():
        if k not in rates:
            rates[k] = v
    return rates


conversion_rates = fetch_ecb_rates_with_fallback()


file_path = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\02. Intermediate Panel\CCP_IOSCO_Database - I Raw Values.xlsx"
df = pd.read_excel(file_path)


def get_currency_code(row):
    if pd.notna(row['Currency']) and row['Currency'] in conversion_rates:
        return row['Currency']
    return None 

def convert_currency(amount, src_currency, target_currency='EUR'):
    if src_currency and src_currency in conversion_rates and target_currency in conversion_rates:
        return amount * conversion_rates[src_currency]
    return amount



meta_cols = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']
columns_to_convert = [col for col in df.columns if col not in meta_cols]

for col in columns_to_convert:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.'), errors='coerce')


for col in columns_to_convert:
    df[col] = df.apply(lambda row: convert_currency(row[col], get_currency_code(row)), axis=1)


output_path = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\02. Intermediate Panel\CCP_IOSCO_Database - II Converted into Euro.xlsx"
df.to_excel(output_path, index=False)
