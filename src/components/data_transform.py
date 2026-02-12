import pandas as pd
from src.components.data_ingestion import load_data
from src.config import cfg

def process_data():
    df = load_data()
    df = df.asfreq('h')
    df['AEP_MW'] = df['AEP_MW'].interpolate(method='linear')
    df = df.loc[df.index.max() - pd.Timedelta(days=60): df.index.mx()]
    df.to_csv(cfg.PROCESSEDDATADIR / 'processed_data.csv')
