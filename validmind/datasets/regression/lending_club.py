import pandas as pd


def load_data():
    data_file = "../datasets/time_series/lending_club_loan_rates.csv"
    df = pd.read_csv(data_file, parse_dates=["DATE"], index_col="DATE")
    return df
