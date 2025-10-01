import pandas as pd

def reverse_code(series: pd.Series, max_val: int = 5):
    return max_val + 1 - series

def score_paei(df_items: pd.DataFrame, df_resp: pd.DataFrame) -> pd.DataFrame:
    df = df_resp.merge(df_items[['item_id','scale','reverse']], on='item_id', how='left')
    df['adj'] = df.apply(lambda r: (6 - r['answer']) if r['reverse']==1 else r['answer'], axis=1)
    return df.groupby('scale')['adj'].sum().reset_index(name='raw')

def score_likert(df_items: pd.DataFrame, df_resp: pd.DataFrame, max_val: int = 5) -> pd.DataFrame:
    """Универсальный подсчёт для DISC/HEXACO: сумма по шкалам с учётом reverse."""
    df = df_resp.merge(df_items[['item_id','scale','reverse']], on='item_id', how='left')
    df['adj'] = df.apply(lambda r: (max_val + 1 - r['answer']) if r['reverse']==1 else r['answer'], axis=1)
    return df.groupby('scale')['adj'].sum().reset_index(name='raw')

def score_disc(df_items: pd.DataFrame, df_resp: pd.DataFrame) -> pd.DataFrame:
    return score_likert(df_items, df_resp, max_val=5)

def score_hexaco(df_items: pd.DataFrame, df_resp: pd.DataFrame) -> pd.DataFrame:
    return score_likert(df_items, df_resp, max_val=5)
