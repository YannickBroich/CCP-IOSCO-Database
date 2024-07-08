# -*- coding: utf-8 -*-
"""
Created on Mon May 27 21:29:01 2024

@author: User
"""

import pandas as pd
import os
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def transform_default_fund(report_level_identifier):
    """Transform ReportLevelIdentifier to DefaultFund based on specific rules."""
    mapping = {
        'Cboe Clear Europe NV': 'CBOE_DefaultFund',
        'Cash Equities': 'CBOE_DefaultFund_CEQ',
        'Equity Derivatives': 'CBOE_DefaultFund_EQD',
        'EuroCCP NV': 'CBOE_DefaultFund',
        'Equity derivatives': 'CBOE_DefaultFund_EQD'
    }
    return mapping.get(report_level_identifier, '')

def transform_number_variables(df, description_column_exists=True):
    numeric_columns = [col for col in df.columns if col.startswith(('4.', '6.', '7.', '16.', '17.', '18.', '20'))]
    if description_column_exists:
        descriptions = df['Description'].unique() if 'Description' in df.columns else ['']
        for desc in descriptions:
            for col in numeric_columns:
                new_col_name = f"{col}_{desc}"
                df[new_col_name] = df[col]
        df.drop(columns=numeric_columns, inplace=True)
    return df

def clean_nan_values(cell):
    """Replace cells containing 'nan' or variations of 'nan' with an empty string."""
    if isinstance(cell, str) and 'nan' in cell.lower():
        return ''
    return cell

def process_excel_files(folder_path):
    files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]
    combined_data = pd.DataFrame()

    special_files = [
        'CPMI-IOSCO-Quantative-Disclosure-31-March-2020.xlsx',
        'CPMI-IOSCO-Quantitative-Disclosure-30-June-2020.xlsx',
        'CPMI-IOSCO-Quantitative-Disclosure-30-June-2021.xlsx',
        'CPMI-IOSCO-Quantitative-Disclosure-31-March-2021.xlsx'
    ]

    for file in files:
        file_path = os.path.join(folder_path, file)
        logging.info(f"Processing {file_path}")
        try:
            xl = pd.ExcelFile(file_path)
            for sheet in xl.sheet_names:
                if any(pattern in sheet for pattern in ['CCP_DataFile_', 'CCP1_DataFile_', 'CCP1_DataFile_6.2', 'CCP1_DataFile_6_2']) or sheet == 'AggregatedDataFile':
                    logging.info(f"Processing sheet {sheet}")
                    try:
                        df = xl.parse(sheet_name=sheet)
                        logging.info(f"Loaded sheet {sheet} with {len(df)} rows and columns: {df.columns.tolist()}")

                        required_columns = ['ReportDate', 'ReportLevelIdentifier']
                        if not all(col in df.columns for col in required_columns):
                            logging.warning(f"Sheet {sheet} in file {file_path} is missing required columns. Skipping this sheet.")
                            continue

                        description_column_exists = 'Description' in df.columns

                        df = transform_number_variables(df, description_column_exists)
                        df['CCP'] = 'CBOE Clear Europe'
                        df['ClearingService'] = df['ReportLevelIdentifier']

                        if file in special_files and sheet == 'CCP_DataFile_23':
                            df['Currency'] = df['Description']
                        else:
                            df['Currency'] = df.get('Currency', 'USD')

                        df['DefaultFund'] = df['ReportLevelIdentifier'].apply(transform_default_fund)

                        combined_data = pd.concat([combined_data, df], ignore_index=True)

                    except Exception as e:
                        logging.error(f"Error processing sheet {sheet} in {file_path}: {e}")
        except PermissionError as e:
            logging.error(f"Permission denied: {e}")
        except Exception as e:
            logging.error(f"Error opening file {file_path}: {e}")

    if combined_data.empty:
        logging.error("No data was processed. Please check the sheet names and data.")
        return pd.DataFrame()

    combined_data['DefaultFund'] = combined_data['ClearingService'].apply(transform_default_fund)

    combined_data = combined_data.groupby(['ReportDate', 'ClearingService', 'Currency'], as_index=False).agg(
        lambda x: x.iloc[0] if x.name in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] else x.sum() if pd.api.types.is_numeric_dtype(x) else ' '.join(x.astype(str))
    )

    combined_data.fillna('', inplace=True)
    
    
    combined_data = combined_data.applymap(clean_nan_values)
    combined_data = combined_data.applymap(lambda x: '' if x in ['0', 0] else x)

    
    combined_data.drop(['Description', 'ReportLevelIdentifier', 'ReportLevel'], axis=1, inplace=True, errors='ignore')
    return combined_data

def main():
    folder_path = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\CBOE Clear'
    combined_df = process_excel_files(folder_path)
    
    if combined_df.empty:
        logging.error("No data combined. Exiting.")
        return

    final_columns_order = ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency'] + [col for col in combined_df.columns if col not in ['ReportDate', 'CCP', 'ClearingService', 'DefaultFund', 'Currency']]
    combined_df = combined_df[final_columns_order]
    
    output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\CBOE_Clear_CompiledData.xlsx'
    try:
        combined_df.to_excel(output_file, index=False)
        logging.info(f"Data combined and saved to {output_file}")
    except PermissionError as e:
        logging.error(f"Permission denied: {e}")

if __name__ == "__main__":
    main()
