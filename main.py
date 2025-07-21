from jobs.netherlands_load import netherlands_load
from utils.enums import LoadType
from utils.date_utils import align_lists
from visualize.visualize_time_series import visualize_double_load_var

if __name__ == "__main__":
    n_days = 30
    forecast_flattened = netherlands_load(type_load=LoadType.FORECAST, n_days=n_days)
    actual_flattened = netherlands_load(type_load=LoadType.ACTUAL, n_days=n_days)

    forecast_flattened, actual_flattened = align_lists(forecast_flattened, actual_flattened)

    visualize_double_load_var(actual_flattened, forecast_flattened)
