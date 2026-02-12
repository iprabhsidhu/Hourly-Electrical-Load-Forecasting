import pandas as pd
from src.config import cfg

def load_data():
    df = pd.read_csv(cfg.RAWDATADIR / "AEP_hourly.csv")
    df['Datetime'] = pd.to_datetime('Datetime')
    df = df.groupby('Datetime').mean().reset_index()
    df.set_index('Datetime', inplace=True)
    return df
