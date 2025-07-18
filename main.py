from jobs.netherlands_actual_load import netherlands_actual_load
from jobs.netherlands_forecast_load import netherlands_forecast_load
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    forecast_flattened = netherlands_forecast_load(n_days=7)
    actual_flattened = netherlands_actual_load(n_days=7)

    visualize_double_load_var(actual_flattened, forecast_flattened)
