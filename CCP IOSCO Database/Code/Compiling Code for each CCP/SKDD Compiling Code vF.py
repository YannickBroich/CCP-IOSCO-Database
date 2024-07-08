# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 01:42:38 2024

@author: User
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_default_fund_and_currency(report_level_identifier, row):
    """Transformiert ReportLevelIdentifier in DefaultFund und Currency basierend auf spezifischen Regeln."""
    mapping = {
        'SKDD-CCP': 'SKDD_DefaultFund',
        
    }
    default_fund = mapping.get(report_level_identifier, '')

    
    if 'Currency' in row.index:
        currency = row['Currency']
    else:
        currency = ''
    
    return default_fund, currency

def transform_number_variables(row, description_column_exists=True):
    transformed_row = row.copy()
    for column in row.index:
        if column.startswith('4.') or column.startswith('6.') or column.startswith('7.') or column.startswith('16.') or column.startswith('17.') or column.startswith('18.') or column.startswith('20') or column.startswith('23'):
            new_column_name = f"{column}_{row['Description']}" if description_column_exists else column
            transformed_row[new_column_name] = row[column]
            if description_column_exists:
                transformed_row.drop(column, inplace=True)
    return transformed_row

def process_excel_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    combined_df = pd.DataFrame()

    for file in files:
        logging.info(f"Processing {file}")
        xl = pd.ExcelFile(os.path.join(folder_path, file))
        for sheet in xl.sheet_names:
            if sheet.startswith('SKDD-CCP_DataFile_') or sheet == 'SKDD-CCP AggregatedDataFile':
                logging.info(f"Processing sheet {sheet}")
                try:
                    df = xl.parse(sheet_name=sheet)
                    description_column_exists = 'Description' in df.columns

                    for index, row in df.iterrows():
                        transformed_row = transform_number_variables(row, description_column_exists)
                        transformed_row['ReportDate'] = row['ReportDate']
                        transformed_row['CCP'] = 'SKDD'
                        transformed_row['ClearingService'] = row['ReportLevelIdentifier']
                        default_fund, currency = transform_default_fund_and_currency(row['ReportLevelIdentifier'], row)
                        transformed_row['DefaultFund'] = default_fund
                        transformed_row['Currency'] = currency
                        combined_df = pd.concat([combined_df, transformed_row.to_frame().T], ignore_index=True)

                except Exception as e:
                    logging.error(f"Error processing sheet {sheet} in {file}: {e}")

   
    combined_df = combined_df.groupby(['ReportDate', 'DefaultFund', 'Currency'], as_index=False).first()

    
    combined_df.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')

    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\SKDD'
    combined_df = process_excel_files(folder_path)
    
    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\SKDD_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False)
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()
