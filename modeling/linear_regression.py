import pandas as pd
from sklearn.linear_model import LinearRegression


def train_load_forecast_model(
        actual_flattened: list,
        n_days_train: int = 39,
        n_days_total: int = 53,
        lag_list: list = [1, 96, 672],
        points_per_day: int = 96
):
    """
    Trains a linear regression model on electricity load data using lag features.

    Parameters:
        actual_flattened (list): List of dicts with 'load_mw' and 'timestamp'
        n_days_train (int): Number of days to use for training (default: 23)
        n_days_total (int): Total number of days in dataset (default: 30)
        lag_list (list): List of lag intervals (in 15-min steps)
        points_per_day (int): Number of 15-min intervals per day (default: 96)

    Returns:
        model (LinearRegression): Trained model
        X_test (pd.DataFrame): Test features
        y_test (pd.Series): True test values
        y_pred (np.ndarray): Predicted values
    """

    # Convert to DataFrame
    df = pd.DataFrame(actual_flattened)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.sort_values('timestamp').reset_index(drop=True)

    # Add lag features
    for lag in lag_list:
        df[f'lag_{lag}'] = df['load_mw'].shift(lag)
    df['gt'] = df['load_mw'].shift(-672)

    # Drop rows with missing lags
    df = df.dropna().reset_index(drop=True) # since the last lag is 192, one week is dropped

    # Create feature matrix and target
    X = df[[f'lag_{lag}' for lag in lag_list]]
    y = df['gt']

    # Split into training and test sets
    n_train = n_days_train * points_per_day - lag_list[-1]
    n_forecast = (n_days_total - n_days_train) * points_per_day

    X_train = X.iloc[:n_train]
    y_train = y.iloc[:n_train]
    X_test = X.iloc[n_train:n_train + n_forecast]
    y_test = y.iloc[n_train:n_train + n_forecast]

    # Train linear regression
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    return model, X_test, y_test, y_pred
