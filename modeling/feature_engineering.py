import pandas as pd
from sklearn.preprocessing import StandardScaler


def prepare_train_test_data(
        actual_flattened: list,
        lag_list: list = [1, 96, 672],
        prediction_ahead: int = 96
):
    df = pd.DataFrame(actual_flattened)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Add lag features
    for lag in lag_list:
        df[f'lag_{lag}'] = df['load_mw'].shift(lag)
    df['gt'] = df['load_mw'].shift(-prediction_ahead)

    # Drop rows with missing lags or targets
    df = df.dropna().reset_index(drop=True)

    # Feature matrix and target
    X = df[[f'lag_{lag}' for lag in lag_list]]
    y = df['gt']
    timestamps = df['timestamp']

    # Train-test split (80/20)
    split_idx = int(0.8 * len(X))
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]
    test_timestamps = timestamps.iloc[split_idx:]

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    return X_train_scaled, X_test_scaled, y_train, y_test, test_timestamps.reset_index(drop=True)
