import pandas as pd
import unicodedata

def get_deadline(excel_path):
    df = pd.read_excel(excel_path)
    df.columns = [pd.to_datetime(col, origin="1899-12-30", unit="D").date() if isinstance(col, (int, float)) else col for col in df.columns]
    
    return df

def get_correspondence(excel_path):
    df = pd.read_excel(excel_path)
    df["group"] = df.apply(
        lambda row: "・".join(col for col in df.columns if row[col] == "〇"),
        axis=1
    )
    df["名称2"] = df.apply(
        lambda row: convert_half_to_full_katakana(row["名称2"]),
        axis=1
    )
    
    keep_columns = ["製品規格名称", "group", "名称2"]
    df = df[keep_columns]
    
    return df

def get_production_limit(excel_path):
    df = pd.read_excel(excel_path)


def convert_half_to_full_katakana(text):
    """
    半角カタカナを全角カタカナに変換する関数。

    Args:
        text (str): 入力文字列。

    Returns:
        str: 半角カタカナが全角カタカナに変換された文字列。
    """
    # 全角への変換 (NFKC正規化)
    normalized_text = unicodedata.normalize('NFKC', text)
    return normalized_text

# テスト
if __name__ == "__main__":
    
    df = get_correspondence('/home/satosho/mini_DX/mini_DX_aporon/Datas/correspondence.xlsx')
    print(df)
