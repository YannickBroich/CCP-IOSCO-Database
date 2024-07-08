# -*- coding: utf-8 -*-
"""
Created on Fri Apr 12 01:42:38 2024

@author: User
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_number_variables(row, description_column_exists=True):
    transformed_row = row.copy()
    for column in row.index:
        if column.startswith('4.') or column.startswith('6.') or column.startswith('7.') or column.startswith('16.') or column.startswith('17.') or column.startswith('18.') or column.startswith('20'):
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
            if sheet.startswith('CCPA_DataFile_') or sheet == 'CCPA_AggregateDataFile':
                logging.info(f"Processing sheet {sheet}")
                try:
                    df = xl.parse(sheet_name=sheet)
                    logging.info(f"Loaded sheet {sheet} with {len(df)} rows and columns: {df.columns.tolist()}")

                   
                    required_columns = ['ReportDate', 'ReportLevelIdentifier']
                    if not all(col in df.columns for col in required_columns):
                        logging.warning(f"Sheet {sheet} in file {file} is missing required columns. Skipping this sheet.")
                        continue

                    description_column_exists = 'Description' in df.columns

                    for index, row in df.iterrows():
                        transformed_row = transform_number_variables(row, description_column_exists)
                        transformed_row['ReportDate'] = row['ReportDate']
                        transformed_row['CCP'] = 'CCP Austria'
                        transformed_row['ClearingService'] = 'CCPA'
                        transformed_row['DefaultFund'] = 'CCPA_DefaultFund'
                        transformed_row['Currency'] = 'EUR'

                        combined_df = pd.concat([combined_df, transformed_row.to_frame().T], ignore_index=True)

                except Exception as e:
                    logging.error(f"Error processing sheet {sheet} in {file}: {e}")

    if combined_df.empty:
        logging.error("No data was processed. Please check the sheet names and data.")
        return pd.DataFrame()

    combined_df.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')

    
    combined_df = combined_df.groupby(['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'], as_index=False).sum()

    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\CCP Austria'
    combined_df = process_excel_files(folder_path)
    
    if combined_df.empty:
        logging.error("No data combined. Exiting.")
        return

    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\CCPA_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False)
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()
