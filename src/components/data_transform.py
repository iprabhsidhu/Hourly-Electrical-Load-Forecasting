import pandas as pd

def process_data(cfg, df):
    df = df.asfreq('h')
    df['AEP_MW'] = df['AEP_MW'].interpolate(method='linear')
    df = df.loc[df.index.max() - pd.Timedelta(days=30): df.index.max()]
    df.to_csv(cfg.PROCESSEDDATADIR / 'processed_data.csv')
    return df
