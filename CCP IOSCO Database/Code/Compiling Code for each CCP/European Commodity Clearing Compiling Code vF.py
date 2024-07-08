# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 01:42:38 2024

@author: User
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_default_fund(report_level_identifier):
    """Transform ReportLevelIdentifier to DefaultFund based on specific rules."""
    mapping = {
        'ECC': 'ECC_DefaultFund',
    }
    return mapping.get(report_level_identifier, 'ECC_DefaultFund')

def transform_number_variables(row, description_column_exists=True):
    transformed_row = row.copy()
    columns_to_drop = []

    for column in row.index:
        if column.startswith(('4.', '6.', '7.', '16.', '17.', '18.', '20', '23')):
            new_column_name = f"{column}_{row['Description']}" if description_column_exists else column
            transformed_row[new_column_name] = row[column]
            columns_to_drop.append(column)

    transformed_row.drop(columns_to_drop, inplace=True)
    return transformed_row

def process_excel_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    combined_df = pd.DataFrame()

    for file in files:
        logging.info(f"Processing {file}")
        xl = pd.ExcelFile(os.path.join(folder_path, file))
        for sheet in xl.sheet_names:
            if sheet.startswith('ECC_DataFile_') or sheet == 'ECC_AggregateDataFile':
                logging.info(f"Processing sheet {sheet}")
                try:
                    df = xl.parse(sheet_name=sheet)
                    description_column_exists = 'Description' in df.columns

                    for index, row in df.iterrows():
                        transformed_row = transform_number_variables(row, description_column_exists)
                        transformed_row['ReportDate'] = row['ReportDate']
                        transformed_row['ClearingService'] = row['ReportLevelIdentifier']
                        transformed_row['DefaultFund'] = transform_default_fund(row['ReportLevelIdentifier'])

                      
                        if 'Currency' in row:
                            transformed_row['Currency'] = row['Currency']
                        else:
                            transformed_row['Currency'] = ''

                      
                        transformed_row['CCP'] = 'European Commodity Clearing'

                        combined_df = pd.concat([combined_df, transformed_row.to_frame().T], ignore_index=True)

                except Exception as e:
                    logging.error(f"Error processing sheet {sheet} in {file}: {e}")

    combined_df.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')

   
    combined_df = combined_df[combined_df['Currency'] != 'https://www.ecc.de/en/']

    
    combined_df = combined_df.groupby(['ReportDate', 'DefaultFund', 'ClearingService', 'Currency', 'CCP'], as_index=False).sum()

    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\European Commodity Clearing'
    combined_df = process_excel_files(folder_path)
    
    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\EuropeanCommodityClearing_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False, engine='openpyxl')
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()
