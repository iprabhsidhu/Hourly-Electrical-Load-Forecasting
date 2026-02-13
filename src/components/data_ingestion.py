import pandas as pd

def load_data(cfg):
    df = pd.read_csv(cfg.RAWDATADIR / "AEP_hourly.csv")
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df = df.groupby('Datetime').mean().reset_index()
    df.set_index('Datetime', inplace=True)
    return df
