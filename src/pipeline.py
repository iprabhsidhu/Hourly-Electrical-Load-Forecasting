import pandas as pd
from src.config import load_config
from src.components.train import Model

def main():
    df = pd.read_csv(cfg.PROCESSEDDATADIR / "processed_data.csv", index_col=0, parse_dates=True)
    cfg = load_config()
    model = Model(cfg)
    model.fit(df['AEP_MW'])
    model.save_model()

if __name__ == "__main__":
    main()
