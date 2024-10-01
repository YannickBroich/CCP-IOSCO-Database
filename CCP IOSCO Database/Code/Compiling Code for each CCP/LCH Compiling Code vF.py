# -*- coding: utf-8 -*-
"""
Created on Sat Sep 21 11:14:18 2024

@author: Yannick
"""

import os
import pandas as pd


def restore_column_format(df):
    
    df.columns = [col.replace('_', '.') if any(c.isdigit() for c in col) else col for col in df.columns]
    return df


def correct_misaligned_rows(df):
    
    if 'Currency' not in df.columns:
        print("Currency column missing, skipping correction.")
        return df

    
    for col in df.columns:
        if col.startswith('5_'):
            misaligned_rows = df['Currency'].isna() & df[col].notna()
            if misaligned_rows.any():
                print(f"Detected misalignment in column '{col}'. Correcting rows...")
                
                df.loc[misaligned_rows, 'Currency'] = df.loc[misaligned_rows, col]
                df.loc[misaligned_rows, col] = None  
    return df


def transform_number_variables(df, description_column_exists=True):
    
    cols_to_transform = [col for col in df.columns if any(col.startswith(prefix) for prefix in ['4.', '6.', '7.', '16.', '17.', '18.', '20'])]

    
    if description_column_exists and 'Description' in df.columns:
        
        new_col_names = {col: f"{col}_{df['Description']}" for col in cols_to_transform}
    else:
        
        new_col_names = {col: col for col in cols_to_transform}

   
    df.rename(columns=new_col_names, inplace=True)

    
    if description_column_exists and 'Description' in df.columns:
        df.drop(cols_to_transform, axis=1, inplace=True, errors='ignore')  

    return df

# Directory and file paths
directory = r'{Your Path}\CCP IOSCO Databasen\Raw Data\LCH'
output_file = r'{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\LCH_CompiledDatavf.xlsx'
sheet_name_patterns = ["LCHLTD_DataFile_", "CCP1_DataFile_", "LCHSA_DataFile_", "CCP_DataFile_", 
                       "LCHLTD_AggregatedDataFile", "LCHSA_AggregatedDataFile", "CCP_AggregateDataFile", "AggregatedDataFile"]

combined_data = []


for filename in os.listdir(directory):
    if filename.endswith(".xlsx"):
        file_path = os.path.join(directory, filename)
        xls = pd.ExcelFile(file_path)
        print(f"File: {filename}")
        for sheet_name in xls.sheet_names:
            print(f"  Found sheet: {sheet_name}")
            if any(pattern in sheet_name for pattern in sheet_name_patterns):
                print(f"    Processing sheet: {sheet_name}")
                df = pd.read_excel(file_path, sheet_name=sheet_name)
                
                
                df = restore_column_format(df)
                
                
                print(f"Columns in {sheet_name}: {df.columns.tolist()}")
                
                if not df.empty:
                    
                    df = correct_misaligned_rows(df)

                   
                    df = transform_number_variables(df, description_column_exists='Description' in df.columns)
                    df['CCP'] = 'LCH'
                    df['DefaultFund'] = 'LCH_DefaultFund'
                    combined_data.append(df)
                else:
                    print(f"    Sheet {sheet_name} is empty, skipping.")


if combined_data:
    
    combined_df = pd.concat(combined_data, ignore_index=True)
    combined_df.dropna(how='all', inplace=True)

   
    combined_df = combined_df.groupby(['ReportDate', 'ReportLevelIdentifier', 'Currency'], as_index=False).first()

    
    ordered_columns = ['ReportDate', 'CCP', 'ReportLevelIdentifier', 'DefaultFund', 'Currency']
    numeric_columns = [col for col in combined_df.columns if col not in ordered_columns]
    combined_df = combined_df[ordered_columns + numeric_columns]

    
    combined_df.rename(columns={'ReportLevelIdentifier': 'ClearingService'}, inplace=True)

    
    combined_df.to_excel(output_file, index=False)
    print(f"Combined data saved to {output_file}")
else:
    print("No data found to combine.")
