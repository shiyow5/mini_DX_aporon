import pandas as pd
import numpy as np
import json
from datetime import timedelta
from Excel2Dataframe import get_deadline

test_data = "/home/satosho/mini_DX/mini_DX_aporon/Datas/test_data.xlsx"
ref_data = "/home/satosho/mini_DX/mini_DX_aporon/Datas/production_create_description.json"

df = get_deadline(test_data)

with open(ref_data, "r", encoding="utf-8") as f:
    refs = json.load(f)


def transform_dataframe(df):
    required_columns = {"製品規格名称", "名称2"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns: {required_columns - set(df.columns)}")
    
    date_columns = [col for col in df.columns if col not in required_columns]
    transformed_rows = []
    
    for _, row in df.iterrows():
        base_row = {"製品規格名称": row["製品規格名称"], "名称2": row["名称2"]}
        
        for date_col in date_columns:
            value = row[date_col]
            if pd.notna(value) and isinstance(value, (int, float)):
                if row["名称2"] in refs.keys():
                    processing = refs[row["名称2"]]["processing"]
                    new_rows = [{**base_row, **{col: np.nan for col in date_columns}} for _ in range(len(processing))]
                    for i, process_row in enumerate(processing):
                        for j in range(len(process_row)):
                            now_day = date_col - timedelta(days=len(process_row)-j)
                            new_rows[i][now_day] = process_row[j] * value
                        
                    transformed_rows += new_rows
    
    return pd.DataFrame(transformed_rows)

df = transform_dataframe(df)

df.to_excel("output.xlsx", index=False)

print("Excelファイルに保存しました。")