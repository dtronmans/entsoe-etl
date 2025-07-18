from jobs.netherlands_load import netherlands_load
from modeling.linear_regression import train_load_forecast_model
from modeling.predict_range_with_model import predict_range_with_model
from utils.enums import LoadType
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    n_days = 60
    forecast_flattened = netherlands_load(type_load=LoadType.FORECAST, n_days=n_days)
    actual_flattened = netherlands_load(type_load=LoadType.ACTUAL, n_days=n_days)

    model, X_test, y_test, y_pred = train_load_forecast_model(actual_flattened)
    #
    model_preds = predict_range_with_model(model, actual_flattened, len(actual_flattened) - 672 - 672, len(actual_flattened) - 1 - 672)
    # print(model_preds)

    visualize_double_load_var(actual_flattened, model_preds)
