from jobs.netherlands_load import netherlands_load
from modeling.models import train_random_forest_model
from utils.enums import LoadType
from modeling.feature_engineering import prepare_train_test_data
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    n_days = 5
    lag_features = [1, 2, 4, 8, 16]  # 15-minute units
    prediction_ahead = 4  # 1 hour ahead

    forecast_flattened = netherlands_load(type_load=LoadType.FORECAST, n_days=n_days)
    actual_flattened = netherlands_load(type_load=LoadType.ACTUAL, n_days=n_days)

    X_train, X_test, y_train, y_test, test_timestamps = prepare_train_test_data(
        actual_flattened, lag_features, prediction_ahead
    )

    model, y_pred = train_random_forest_model(X_train, y_train, X_test)

    # Adjust test timestamps for prediction horizon
    test_timestamps = test_timestamps.shift(-prediction_ahead).dropna().reset_index(drop=True)

    predicted_output = [
        {'timestamp': ts, 'load_mw': float(pred)}
        for ts, pred in zip(test_timestamps, y_pred)
    ]

    visualize_double_load_var(actual_flattened, predicted_output)
