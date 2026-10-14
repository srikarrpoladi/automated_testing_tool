#Option 3 — 56 to 179 days of historical data
#This is an initial baseline implementation. The production version should use time-series backtesting, account for serially correlated errors and assess whether extrapolating a linear trend is reasonable.

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

DATA = "/Users/srikarpoladi/Downloads/prooject/testing/data1/complete.csv"

class MORE():
    def __init__(self, path):
        self.path = path

    def read_data(self):
        df = pd.read_csv(self.path)
        df["date"] = pd.to_datetime(df["date"])
        df = df[(df["date"] >= "2010-02-01") & (df["date"] <= "2010-09-01")]
        return df

    def prep(self, df):
        df = df.sort_values("date")
        start = df["date"].min()
        df["day_index"] = (df["date"] - start).dt.days

        df["weekday"] = df["date"].dt.dayofweek
        return df


    def regression_impact(self, df, launch_date):
        features = pd.get_dummies(
            df[["day_index", "weekday"]],
            columns=["weekday"],
            dtype=int
        )

        launch_date = pd.Timestamp(launch_date)
        pre_mask = df["date"] < launch_date
        post_mask = ~pre_mask

        model = LinearRegression()
        model.fit(
            features.loc[pre_mask],
            df.loc[pre_mask, "total_rev"]
        )

        expected_daily = model.predict(features.loc[post_mask])

        expected_daily = np.maximum(expected_daily, 0)

        actual = df.loc[post_mask, "total_rev"].sum()

        expected = expected_daily.sum()

        return {
            "actual revenue": actual,
            "expected revenue": expected,
            "estimated impact revenue": actual - expected,
            "estimated_lift_pct":
                (actual / expected - 1) * 100
        }

if __name__ == "__main__":
    more = MORE(DATA)
    df = more.read_data()
    prep_df = more.prep(df)
    results = more.regression_impact(prep_df, launch_date="2010-06-25")
    for metric, score in results.items():
        if 'revenue' in metric:
            print(f"{metric} : ${round(score,2)}")
        else:
            print(f"{metric} : {round(score,2)}%")

