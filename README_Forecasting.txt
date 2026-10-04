NORTHSTAR - FORECASTING LEAD PACKAGE

FILES NEEDED IN THE SAME FOLDER:
1. forecasting.py
2. northstar_daily_sku_market_cleaned.csv

INSTALL ONCE:
py -m pip install -r requirements_forecasting.txt

RUN:
py forecasting.py

THE SCRIPT WILL CREATE A FOLDER NAMED:
forecast_outputs

OUTPUTS:
- forecast_metrics.csv
- forecast_predictions.csv
- feature_importance.csv
- forecast_summary.txt
- forecast_NS-003.png
- forecast_NS-033.png
- forecast_NS-048.png

FORECAST DESIGN:
- Training end: June 2, 2022
- Holdout/Test: June 3-30, 2022 (28 days)
- Series:
  * NS-003 | France | E-commerce | Home Storage | Asia-Suez
  * NS-033 | France | E-commerce | Home Storage | Regional-Europe
  * NS-048 | France | E-commerce | Home Storage | Air-Or-Other
- Baseline: Seasonal Naive, 28-day lag
- Second method: Random Forest using recursive lag/rolling/calendar features
- Evaluation: MAE and WAPE

PRESENTATION IDEA:
"As Forecasting Lead, I used the team-cleaned dataset and trained models only on data through June 2, 2022. I held out June 3 to June 30 as an unseen 28-day test period. I first used a 28-day seasonal-naive forecast as the baseline, then compared it with a Random Forest model using leakage-safe historical lag and calendar features. Forecast accuracy was evaluated using MAE and WAPE."

IMPORTANT:
Lower MAE/WAPE means lower forecasting error. Forecasting results do not by themselves prove that route exposure caused changes in sales.
