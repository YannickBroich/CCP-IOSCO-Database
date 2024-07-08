# -*- coding: utf-8 -*-
"""
Created on Sun May 26 14:27:22 2024

@author: User
"""

import os
import pandas as pd


def transform_number_variables(row, description_column_exists=True):
    transformed_row = row.copy()
    for column in row.index:
        if any(column.startswith(prefix) for prefix in ['4.', '6.', '7.', '16.', '17.', '18.', '20']):
            if description_column_exists and 'Description' in row:
                new_column_name = f"{column}_{row['Description']}"
            else:
                new_column_name = column
            transformed_row[new_column_name] = row[column]
            if description_column_exists and 'Description' in row:
                transformed_row.drop(column, inplace=True)
    return transformed_row


directory = r'C:\{Your Path}\CCP IOSCO Database\Raw Data\LCH'
output_file = r'C:\{Your Path}\CCP IOSCO Database\Database\Compiled Datasets\LCH_CompiledData.xlsx'
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
                if not df.empty:
                    df = df.apply(transform_number_variables, axis=1, description_column_exists='Description' in df.columns)
                    df['CCP'] = 'LCH'
                    df['DefaultFund'] = 'LCH_DefaultFund'
                    combined_data.append(df)
                else:
                    print(f"    Sheet {sheet_name} is empty, skipping.")


if combined_data:
    
    combined_data = [df for df in combined_data if not df.dropna(how='all').empty]

    
    combined_df = pd.concat(combined_data)
    combined_df = combined_df.groupby(['ReportDate', 'ReportLevelIdentifier', 'Currency'], as_index=False).first()

   
    ordered_columns = ['ReportDate', 'CCP', 'ReportLevelIdentifier', 'DefaultFund', 'Currency']
    numeric_columns = [col for col in combined_df.columns if col not in ordered_columns]
    combined_df = combined_df[ordered_columns + numeric_columns]

    
    combined_df.rename(columns={'ReportLevelIdentifier': 'ClearingService'}, inplace=True)

    
    combined_df.to_excel(output_file, index=False)
    print(f"Combined data saved to {output_file}")
else:
    print("No data found to combine.")
