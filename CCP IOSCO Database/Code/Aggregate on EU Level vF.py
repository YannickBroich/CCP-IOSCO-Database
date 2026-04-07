

import pandas as pd


file_path = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\03. Final Panel\CCP_IOSCO_Database - III On CCP Level.xlsx"
df = pd.read_excel(file_path)


drop_keywords = ['percentage', 'percent', 'date', 'time', 'day', 'effective', 'maturity']
numeric_cols = df.select_dtypes(include='number').columns.tolist()
filtered_cols = [col for col in numeric_cols if not any(kw in col.lower() for kw in drop_keywords)]


df_eu = df.groupby('Quarter')[filtered_cols].sum(min_count=1).reset_index()


output_path = r"YOUR_PATH_TO_REPLICATION_PACKAGE\Replication Package\Database\03. Final Panel\CCP_IOSCO_Database - IV On EU Level.xlsx"
df_eu.to_excel(output_path, index=False)

print(output_path)
