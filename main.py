from jobs.netherlands_load import netherlands_load
from utils.enums import LoadType
from utils.date_utils import align_lists
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    n_days = 30
    lag_features = [2, 4, 16, 32, 96]  # 15-minute units
    prediction_ahead = 1  # 15 minutes ahead

    forecast_flattened = netherlands_load(type_load=LoadType.FORECAST, n_days=n_days)
    actual_flattened = netherlands_load(type_load=LoadType.ACTUAL, n_days=n_days)

    forecast_flattened, actual_flattened = align_lists(forecast_flattened, actual_flattened)

    # X_train, X_test, y_train, y_test, test_timestamps = prepare_train_test_data(
    #     actual_flattened, lag_features, prediction_ahead
    # )

    # model, y_pred = train_linear_regression_model(X_train, y_train, X_test)
    # print(test_timestamps)

    # Adjust test timestamps for prediction horizon
    # test_timestamps = test_timestamps.shift(-prediction_ahead).dropna().reset_index(drop=True)
    # print(test_timestamps)

    # predicted_output = [
    #     {'timestamp': ts, 'load_mw': float(pred)}
    #     for ts, pred in zip(test_timestamps, y_pred)
    # ]
    #
    visualize_double_load_var(actual_flattened, forecast_flattened)
