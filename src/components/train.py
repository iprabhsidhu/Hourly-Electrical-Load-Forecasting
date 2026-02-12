import os
import pandas as pd
import numpy as np
from src.config import cfg
from statsmodels.tsa.statespace.sarimax import SARIMAX, SARIMAXResults

class Model:
    def __init__(self, cfg):
        self.model_name = cfg.MODEL['name']
        self.model_version = cfg.MODEL['version']

        self.order = tuple(cfg.MODEL['order'])
        self.seasonal_order = tuple(cfg.MODEL['seasonal_order'])
        
        self.fit_params = cfg.MODEL['params']

        self.save_path = cfg.MODELDIR
        self.model_res = None
        print(f"Initialized {self.model_name} {self.model_version}")

    def fit(self, series, exog=None):
        model = SARIMAX(
                series,
                exog=exog
                order=self.order
                seasonal_order=self.seasonal_order,
                enforce_stationarity=self.fit_params.get('enforce_stationarity'),
                enforce_invertibility=self.fit_params.get('enforce_invertibility')
                )

        self.model_res = model.fit(
                method = self.fit_params.get('method'),
                disp=False
        i        )
        print("Training complete")
    
    def save_model(self):
        if self.model_res is None:
            raise ValueError('no model results found to save. Fit the model first.')

        if not os.path.exist(self.save_path):
            os.makedirs(self.save_path)

        filename = f"{self.model_name}_{self.model_version}.pkl"
        fullpath = os.path.join(self.save_path, filename)
        self.model_res.save(fullpath)
        print(f'Model saved to: {fullpath}')
        
    def load_model(self):
        filename = f"{self.model_name}_{self.model_version}.pkl"
        loadpath = os.path.join(self.save_path, filename)

        if not os.path.exists(loadpath):
            raise FileNotFoundError(f"No model is found at {loadpath}")

        self.model_res = SARIMAXResults.load(load_path)
        print(f"Model {self.model_name} {self.model_version} loaded successfully.")

    def forecast(self, steps=24, exog=None):
        if self.model_res is None:
            raise RuntimeError('Model results not found. Call fit() or load_model() first.')

        return self.model_res.get_forecast(steps=steps, exog=exog).summary_frame()
