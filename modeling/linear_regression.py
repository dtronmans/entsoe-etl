import pandas as pd
from sklearn.linear_model import LinearRegression


def train_load_forecast_model(
        actual_flattened: list,
        lag_list: list = [1, 96, 672],
        prediction_ahead: int = 96
):
    # Convert to DataFrame
    df = pd.DataFrame(actual_flattened)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Add lag features
    for lag in lag_list:
        df[f'lag_{lag}'] = df['load_mw'].shift(lag)
    df['gt'] = df['load_mw'].shift(-prediction_ahead) # this means the gt value is one day ahead

    # Drop rows with missing lags
    df = df.dropna().reset_index(drop=True) # since the last lag is 192, one week is dropped

    # Create feature matrix and target
    X = df[[f'lag_{lag}' for lag in lag_list]]
    y = df['gt']
    gt_timestamps = df['timestamp']

    split_idx = int(0.8 * len(X))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    test_timestamps = gt_timestamps.iloc[split_idx:]

    # Train linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    return model, X_test, y_test.reset_index(drop=True), y_pred, test_timestamps.reset_index(drop=True)
