import pandas as pd
from datetime import timedelta

def predict_range_with_model(model, actual_flattened, start: int, end: int, lag_list: list = [1, 96, 672]):
    """
    Predicts a range of values using a trained linear regression model and returns them
    in the same format as actual_flattened: {'load_mw': ..., 'timestamp': ...}

    Parameters:
        model: Trained LinearRegression model
        actual_flattened (list): Original list of dicts with 'load_mw' and 'timestamp'
        start (int): Start index in the processed DataFrame (after lag drop)
        end (int): End index (exclusive)
        lag_list (list): List of lag intervals used in the model

    Returns:
        List[dict]: Predictions in original format with timestamps shifted +1 week
    """

    # Convert to DataFrame
    df = pd.DataFrame(actual_flattened)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Create lag features
    for lag in lag_list:
        df[f'lag_{lag}'] = df['load_mw'].shift(lag)

    # Drop rows with NaNs due to lagging
    df = df.dropna().reset_index(drop=True)

    # Create feature matrix for the specified range
    X = df[[f'lag_{lag}' for lag in lag_list]].iloc[start - lag_list[-1]:end - lag_list[-1]]
    timestamps = df['timestamp'].iloc[start - lag_list[-1]:end - lag_list[-1]]

    # Run prediction
    y_pred = model.predict(X)

    # Return in original format with +1 week added to timestamp
    results = [{'load_mw': float(pred), 'timestamp': ts + timedelta(weeks=1)} for pred, ts in zip(y_pred, timestamps)]
    return results
