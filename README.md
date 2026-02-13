# Hourly Energy Consumption Forecasting

### Reproducible Time-Series ML Pipeline using SARIMA & MLflow

An end-to-end machine learning pipeline that forecasts **hourly
electricity demand (MW)** using a configurable SARIMA model.\
The project is built as a reproducible ML system --- with CLI execution,
modular components, and experiment tracking.

------------------------------------------------------------------------

## Overview

Electricity providers must estimate short-term power demand accurately.

Poor forecasts cause: - grid instability - generator scheduling
inefficiencies - financial losses

This project predicts future hourly load using historical consumption
data and logs all experiments for comparison and reproducibility.

------------------------------------------------------------------------

## Features

-   Modular ML pipeline architecture
-   YAML-based configuration
-   Command line execution
-   MLflow experiment tracking
-   Automatic model saving
-   Evaluation metrics logging
-   Reproducible training runs
-   Clean project structure (production-style)

------------------------------------------------------------------------

## Project Structure

    EnergyPrediction/
    │
    ├── data/
    │   ├── raw/
    │   └── processed/
    │
    ├── Models/
    │
    ├── notebooks/
    │   └── experiments.ipynb
    │
    ├── src/
    │   ├── components/
    │   │   ├── data_ingestion.py
    │   │   ├── data_transform.py
    │   │   └── model.py
    │   │
    │   ├── config.py
    │   └── pipeline.py
    │
    ├── configuration.yaml      # central configuration
    ├── main.py                 # CLI entrypoint
    ├── Makefile
    ├── requirements.txt
    └── README.md

------------------------------------------------------------------------

## Pipeline Workflow

### 1) Data Ingestion

-   Loads CSV dataset
-   Converts `Datetime` column to timestamp
-   Aggregates duplicate timestamps
-   Sets datetime index

### 2) Data Transformation

-   Converts data to hourly frequency
-   Interpolates missing values
-   Keeps last 30 days of observations
-   Saves processed dataset

### 3) Train/Test Split

80% training\
20% testing

### 4) Model Training

A SARIMA model is trained using parameters from the configuration file.

### 5) Evaluation

Metrics computed: - MAE (Mean Absolute Error) - RMSE (Root Mean Squared
Error) - MAPE (Mean Absolute Percentage Error)

### 6) Experiment Tracking

MLflow logs: - hyperparameters - evaluation metrics - trained model -
configuration file

------------------------------------------------------------------------

## Configuration

All behavior is controlled via:

`configuration.yaml`

Example:

``` yaml
project_name : "Hourly forecasting of Energy Consumption"

data:
  raw : "data/raw/"
  processed : "data/processed/"

model:
  name : "SARIMA"
  version : "v1"
  order : [1,0,2]
  seasonal_order: [1,1,0,24]
```

You can change model parameters or directories without editing Python
code.

------------------------------------------------------------------------

## Model

Model Used: **SARIMA (Seasonal ARIMA)**

Reason: Electric load has strong daily seasonality (24-hour cycle).\
SARIMA models both trend and periodic behavior.

------------------------------------------------------------------------

## Installation

### 1. Clone repository

``` bash
git clone https://github.com/<your-username>/EnergyPrediction.git
cd EnergyPrediction
```

### 2. Create virtual environment

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## Running the Project

### Start MLflow Tracking Server

Required before training:

``` bash
mlflow server --host 127.0.0.1 --port 5000
```

Open UI in browser:

http://127.0.0.1:5000

------------------------------------------------------------------------

### Train Model

``` bash
python main.py --mode train
```

This will: - load data - preprocess - train model - evaluate - save
model - log experiment to MLflow

------------------------------------------------------------------------

### Predict Mode

``` bash
python main.py --mode predict
```

------------------------------------------------------------------------

## Makefile Commands

    make venv     # create virtual environment
    make install  # install dependencies
    make train    # run training pipeline
    make clean    # remove artifacts

------------------------------------------------------------------------

## Output Artifacts

After training:

    Models/
        SARIMA_v1.pkl

    data/processed/
        processed_data.csv

MLflow will also store the experiment run and parameters.

------------------------------------------------------------------------

## Evaluation Metrics

  Metric   Description
  -------- ---------------------------------------------------
  MAE      Average absolute prediction error
  RMSE     Penalizes large errors
  MAPE     Percentage error (most important for forecasting)

------------------------------------------------------------------------

## Limitations

-   Only univariate forecasting
-   No weather or holiday features
-   Short training window (30 days)
-   Not designed for long-horizon forecasting

------------------------------------------------------------------------

## Future Work

-   Add weather data (temperature)
-   Add exogenous regressors
-   Retraining scheduling
-   API deployment (FastAPI)
-   Docker containerization
-   CI/CD pipeline

------------------------------------------------------------------------

## Author

Prabhdeep Singh

------------------------------------------------------------------------

## License

MIT License
