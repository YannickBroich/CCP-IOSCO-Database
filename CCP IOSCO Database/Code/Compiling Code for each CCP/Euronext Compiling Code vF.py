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
    """Transformiert ReportLevelIdentifier in DefaultFund basierend auf spezifischen Regeln."""
    mapping = {
        'WHOLESALES': 'Euronext_DefaultFund_WHOLESALES',
        'RETAILS': 'Euronext_DefaultFund_RETAILS',
        'DERIVATES': 'Euronext_DefaultFund_DERIVATES',
        'EQUITIES': 'Euronext_DefaultFund_EQUITIES',
        'IDEX': 'Euronext_DefaultFund_IDEX',
        'CCG_EQUITY': 'Euronext_DefaultFund_CCG_EQUITY',
        'CCG_BOND': 'Euronext_DefaultFund_CCG_BOND',
        'CCG_AGREX': 'Euronext_DefaultFund_CCG_AGREX',
        'CCG_IDEX': 'Euronext_DefaultFund_CCG_IDEX',
        'CC&G': 'Euronext_DefaultFund_CC&G',
        'CCG': 'Euronext_DefaultFund_CCG',
        'AGREX': 'Euronext_DefaultFund_CCG_AGREX'
    }
    return mapping.get(report_level_identifier, '')

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
        try:
            xl = pd.ExcelFile(os.path.join(folder_path, file), engine='openpyxl') 
            for sheet in xl.sheet_names:
                if sheet.startswith('CCP1_DataFile_') or sheet.startswith('AggregateData') or sheet.startswith('AggregatedData'):
                    logging.info(f"Processing sheet {sheet}")
                    df = xl.parse(sheet_name=sheet, header=3)  
                    description_column_exists = 'Description' in df.columns
                    
                    for index, row in df.iterrows():
                        transformed_row = transform_number_variables(row, description_column_exists)
                        transformed_row['ReportDate'] = row['ReportDate']
                        transformed_row['CCP'] = 'Euronext'
                        transformed_row['ClearingService'] = row['ReportLevelIdentifier']
                        transformed_row['DefaultFund'] = transform_default_fund(row['ReportLevelIdentifier'])
                        combined_df = pd.concat([combined_df, transformed_row.to_frame().T], ignore_index=True)
        except Exception as e:
            logging.error(f"Error processing file {file}: {e}")
    
    
    combined_df.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')

    
    combined_df = combined_df.groupby(['ReportDate', 'DefaultFund'], as_index=False).first()
    
    return combined_df

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\Euronext'
    combined_df = process_excel_files(folder_path)
    
    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\Euronext_CompiledData.xlsx'
    combined_df.to_excel(output_file, index=False)
    logging.info(f"Data combined and saved to {output_file}")

if __name__ == "__main__":
    main()
