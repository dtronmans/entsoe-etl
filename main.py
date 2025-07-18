from jobs.netherlands_load import netherlands_load
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    forecast_flattened = netherlands_load(type_load="forecast", n_days=7)
    actual_flattened = netherlands_load(type_load="actual", n_days=7)

    visualize_double_load_var(actual_flattened, forecast_flattened)
