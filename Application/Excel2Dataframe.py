import pandas as pd
import unicodedata
import datetime

def get_deadline(excel_path, sheet_name = None):
    if sheet_name:
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
    else:
        df = pd.read_excel(excel_path)
    
    df.columns = [pd.to_datetime(col, origin="1899-12-30", unit="D").date() if isinstance(col, (int, float)) else col for col in df.columns]
    df.columns = [col.date() if isinstance(col, datetime.datetime) else col for col in df.columns]
    
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

def clean_name2(text: str):
    ignores = ["トレー並べ", "計量", "梱包", "ダストヘラー"]
    
    text = convert_half_to_full_katakana(text)
    word_list = [clean_name(word) for word in text.split("・")]
    for ignore in ignores:
        if ignore in word_list:
            word_list.remove(ignore)
    
    return "・".join(word_list)
        

def clean_name(text: str):
    text = convert_half_to_full_katakana(text)
    text = text.replace("釦", "スパウト")
    text = text.replace("ボタン", "スパウト")
    text = text.replace("付け", "嵌め")
    text = text.replace("トップキャップ", "キャップ")
    #text = text.replace("ネジ嵌合・スパウト嵌め", "?")
    
    return text
    

# テスト
if __name__ == "__main__":
    
    df = get_correspondence('/home/satosho/mini_DX/mini_DX_aporon/Datas/correspondence.xlsx')
    print(df)
