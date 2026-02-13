import os
import mlflow
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error

from src.config import load_config
from src.components.data_ingestion import load_data
from src.components.data_transform import process_data
from src.components.model import Model

class Pipeline:
    def __init__(self, mode="train"):
        self.cfg = load_config()
        self.mode = mode

        mlflow.set_tracking_uri("http://127.0.0.1:5000")
        mlflow.set_experiment(str(self.cfg.PROJECTNAME))

        self.raw_df=None
        self.processed_df = None
        self.train_df = None
        self.test_df = None
        self.model = None
    
    '''
        DATA STAGES
    '''
    def ingest(self):
        print('Stage 1/3, loading data')
        self.raw_df = load_data(self.cfg)
    
    def transform(self):
        print('Stage 2/3, Processing data')
        self.processed_df = process_data(self.cfg, self.raw_df)

    def split(self, test_size=0.2):
        print('splitting dataset')
        split_index = int(len(self.processed_df) * (1 - test_size))
        self.train_df = self.processed_df.iloc[:split_index]
        self.test_df = self.processed_df.iloc[split_index:]

    def train(self):
        print("Stage 3/3, Trainig model")
        self.model = Model(self.cfg)
        self.model.fit(self.train_df)
    
    def evaluate(self):
        print("Evaluating")

        forecast = self.model.forecast(steps=len(self.test_df))
        preds = forecast['mean']

        y_true = self.test_df.squeeze()

        mae = mean_absolute_error(y_true, preds)
        rmse = np.sqrt(mean_squared_error(y_true, preds))
        mape = np.mean(np.abs((y_true - preds) / y_true)) * 100
        
        print('---------------')
        print('Evaluation metrics')
        print('---------------')
        print(f'MAE : {mae}')
        print(f'RMSE : {rmse}')
        print(f'MAPE : {mape}')
        print('---------------')

        return mae, rmse, mape

    def log_params(self):
        model_cfg = self.cfg.MODEL

        mlflow.log_param("order", model_cfg['order'])
        mlflow.log_param("seasonal_order", model_cfg['seasonal_order'])
        mlflow.log_param("method", model_cfg['params']['method'])
        mlflow.log_param("enforce_stationarity", model_cfg['params']['enforce_stationarity'])
        mlflow.log_param("enforce_invertibality", model_cfg['params']['enforce_invertibality'])
    def log_metrices(self, mae, rmse, mape):
        mlflow.log_metric("MAE", mae)
        mlflow.log_metric("RMSE", rmse)
        mlflow.log_metric("MAPE", mape)

    def log_artifact(self):
        self.model.save_model()

        model_path = os.path.join(
                self.cfg.MODELDIR,
                f"{self.model.model_name}_{self.model.model_version}.pkl"
                )

        mlflow.log_artifact(model_path)
        mlflow.log_artifact("configuration.yaml")

    def run(self):
        with mlflow.start_run():
            
            self.log_params()

            self.ingest()
            self.transform()
            self.split()
           
            if self.mode=="train":
           
                self.train()
                mae, rmse, mape = self.evaluate()
                self.log_metrices(mae, rmse, mape)
                self.log_artifact()

            print('Pipeline executed completed.')
