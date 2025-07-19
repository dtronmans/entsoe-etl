from jobs.netherlands_load import netherlands_load
from modeling.linear_regression import train_load_forecast_model
from utils.enums import LoadType
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    n_days = 60
    forecast_flattened = netherlands_load(type_load=LoadType.FORECAST, n_days=n_days)
    actual_flattened = netherlands_load(type_load=LoadType.ACTUAL, n_days=n_days)

    lag_features = [1, 96, 672]
    prediction_ahead = 96 # one day ahead prediction

    model, X_test, y_test, y_pred, test_timestamps = train_load_forecast_model(actual_flattened, lag_features, prediction_ahead)
    predicted_output = [
        {'timestamp': ts, 'load_mw': float(pred)}
        for ts, pred in zip(test_timestamps, y_pred)
    ]

    visualize_double_load_var(actual_flattened, predicted_output)
