import pandas as pd


def load_excel(file_path):
    """
    Загружает Excel-файл и возвращает DataFrame
    """
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception:
        return None