# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 09:30:06 2024

@author: Yannick
"""

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_default_fund(report_level_identifier):
    mapping = {
        'BMEC_Financial Derivatives': 'BMEC_Financial Derivatives',
        'BMEC_Repo': 'BMEC_Repo',
        'BMEC_Power': 'BMEC_Power',
        'BMEC_IRS': 'BMEC_IRS',
        'BMEC_Equity': 'BMEC_Equity',
        'BMEC_All': 'BMEC_All'
    }
    default_fund = mapping.get(report_level_identifier, '')
    if default_fund == '':
        logging.warning(f"Report Level Identifier '{report_level_identifier}' not found in mapping.")
    return default_fund

def transform_number_variables(row, description_column_exists=True):
    existing_columns = [
        '4.', '6.', '7.', '16.', '17.', '18.', '20', '23'
    ]
    additional_columns = [
        '4.1.1', '4.1.2', '4.1.3', '4.1.4', '4.1.5', '4.1.6', '4.1.7', '4.1.8', '4.1.9', '4.1.10',
        '4.2.1', '4.4.1', '4.4.2', '4.4.4', '4.4.8', '5.1.1', '5.2.1', '5.3.1', '5.3.2', '5.3.3',
        '5.3.4', '6.3.1', '6.4.1', '6.4.2', '6.4.3', '6.4.4', '6.4.5', '6.4.6', '6.4.7', '6.4.8',
        '6.4.9', '6.4.10', '6.4.11', '6.4.12', '6.4.13', '6.4.14', '6.5.1.1', '6.5.1.2',
        '6.5.1.3', '6.5.2', '6.5.3', '6.5.4', '6.5.5', '6.6.1', '6.7.1', '6.8.1', '7.1.1', '7.1.10',
        '7.1.11', '7.2.1', '7.3.2', '12.1.1', '12.1.2', '12.1.3', '12.2.1', '12.2.2', '12.2.3',
        '13.1.1', '13.1.2', '13.1.3.1', '13.1.3.2', '13.1.4', '14.1.1', '14.1.2', '14.1.3', '14.1.4',
        '15.1.1', '15.1.2', '15.2.1', '15.2.2', '15.2.3', '15.2.4', '15.2.5', '15.2.6', '15.2.7',
        '15.3.1', '15.3.2', '16.1.1', '16.1.2', '16.2.1', '16.2.2', '16.2.3', '16.2.4', '16.2.5',
        '16.2.6', '16.2.7', '16.2.9', '16.2.10', '16.2.11', '16.2.12', '16.2.13', '16.2.14',
        '16.2.16', '16.2.17', '16.2.18', '16.2.19', '16.2.20', '16.3.1', '16.3.2', '17.1.1',
        '17.2.1', '17.4.1', '18.1.1.1', '18.1.1.2', '18.1.1.3', '18.1.2.1', '18.1.2.2', '18.1.2.3',
        '18.1.2.4', '18.1.3.1', '18.1.3.2', '18.4.1', '18.4.2', '18.4.3', '19.1.1', '19.1.2',
        '19.1.3.1', '19.1.3.2', '19.1.4.1', '19.1.4.2', '23.1.1', '23.1.2', '23.2.1'
    ]
    
    transformed_row = row.copy()
    for column in row.index:
        if any(column.startswith(prefix) for prefix in existing_columns) or column in additional_columns:
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
            if sheet.startswith('BME CLEARING_DataFile_') or sheet == 'AggregatedDataFile':
                logging.info(f"Processing sheet {sheet}")
                try:
                    df = xl.parse(sheet_name=sheet)
                    description_column_exists = 'Description' in df.columns
                    
                    for index, row in df.iterrows():
                        report_level_identifier = row.get('ReportLevelIdentifier', None)
                        if pd.isna(report_level_identifier):
                            logging.warning(f"Row {index} in file {file}, sheet {sheet} has empty 'ReportLevelIdentifier'")
                            continue

                        logging.info(f"Processing row with ReportLevelIdentifier: {report_level_identifier}")
                        transformed_row = transform_number_variables(row, description_column_exists)
                        transformed_row['ReportDate'] = row['ReportDate']
                        transformed_row['CCP'] = 'BME Clearing'
                        transformed_row['ClearingService'] = report_level_identifier  # Use original ReportLevelIdentifier for ClearingService
                        transformed_row['DefaultFund'] = transform_default_fund(report_level_identifier)
                        logging.info(f"Transformed Row - ClearingService: {transformed_row['ClearingService']}, DefaultFund: {transformed_row['DefaultFund']}")
                        transformed_row['Currency'] = row.get('Currency', 'EUR')  # Ensure 'Currency' column is added
                        combined_df = pd.concat([combined_df, transformed_row.to_frame().T], ignore_index=True)
                        
                except Exception as e:
                    logging.error(f"Error processing sheet {sheet} in {file}: {e}")

    combined_df.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')
    
    numeric_cols = combined_df.columns.drop(['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'])
    combined_df[numeric_cols] = combined_df[numeric_cols].apply(pd.to_numeric, errors='coerce')
   
    group_columns = ['ReportDate', 'DefaultFund', 'Currency']
    aggregated_columns = {col: 'sum' for col in numeric_cols}
    aggregated_columns.update({col: 'first' for col in ['CCP', 'ClearingService']})
    combined_df = combined_df.groupby(group_columns, as_index=False).agg(aggregated_columns)
    
    combined_df.replace(0, '', inplace=True)
    
    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\BME Clearing'
    combined_df = process_excel_files(folder_path)
    
    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\BME_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False)
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()

