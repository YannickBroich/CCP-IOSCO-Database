# -*- coding: utf-8 -*-
"""
Created on Tue May 21 11:37:11 2024

@author: User
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_number_variables(row, description_column_exists=True):
    transformed_row = {}
    for column in row.index:
        if (column.count('_') == 2 or column.count('.') == 2) and all(part.isdigit() for part in column.replace('.', '_').split('_')):
            if description_column_exists and 'Description' in row:
                new_column_name = f"{column.replace('_', '.')}_{row['Description']}"
            else:
                new_column_name = column.replace('_', '.')
            if new_column_name not in transformed_row:
                transformed_row[new_column_name] = row[column]
            else:
                logging.warning(f"Duplicate column name {new_column_name} in row {row.name}, skipping...")
    return transformed_row

def process_csv_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]
    combined_data = []

    for file in files:
        logging.info(f"Processing {file}")
        try:
            df = pd.read_csv(os.path.join(folder_path, file))
            logging.info(f"Columns in {file}: {df.columns.tolist()}")
            description_column_exists = 'Description' in df.columns
            if 'ReportDate' not in df.columns or 'ReportLevelIdentifier' not in df.columns:
                logging.error(f"Required columns missing in {file}")
                continue
            
            for _, row in df.iterrows():
                transformed_row = transform_number_variables(row, description_column_exists)
                transformed_row['ReportDate'] = row['ReportDate']
                transformed_row['CCP'] = 'ICE Clear'
                transformed_row['ClearingService'] = row['ReportLevelIdentifier']
                transformed_row['DefaultFund'] = 'ICEClear_DefaultFund'
                transformed_row['Currency'] = row.get('Currency', 'USD')  
                combined_data.append(transformed_row)

        except Exception as e:
            logging.error(f"Error processing {file}: {e}")

    combined_df = pd.DataFrame(combined_data)
    combined_df = combined_df.groupby(['ReportDate', 'ClearingService', 'Currency'], as_index=False).first()

    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\ccp_cpmi_iosco_data\data\ICE Clear'  
    combined_df = process_csv_files(folder_path)

    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + \
                          [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]

    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\ICEClear_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False)
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()
