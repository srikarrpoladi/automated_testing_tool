
# Option 4 — 180+ days of historical data

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.statespace.sarimax import SARIMAX

DATA = "/Users/srikarpoladi/Downloads/prooject/testing/data1/complete.csv"

class MOST:
    def __init__(self, path):
        self.path = path

    def read_data(self):
        # Load the CSV and convert dates to datetime
        df = pd.read_csv(self.path)
        df["date"] = pd.to_datetime(df["date"])
        df["date"] = df["date"].dt.normalize()
        df = df[(df["date"] >= "2009-12-01") &(df["date"] <= "2011-09-01")].copy()

        return df


    def prep(self, df, launch_date):
        df = df.sort_values("date").set_index("date")
        df = df.asfreq("D")
        df["total_rev"] = df["total_rev"].fillna(0)
        pre = df.loc[df.index < launch_date, "total_rev"]
        post = df.loc[df.index >= launch_date, "total_rev"]
        horizon = len(post)

        return df, pre, post, horizon


    def forecast(self, train, future_dates, method):

        if method == "Weekday average":
            means = train.groupby(train.index.dayofweek).mean()

            return np.array([means[d] for d in future_dates.dayofweek])

        if method == "Linear regression":
            origin = train.index.min()

            def features(idx):
                t = (idx - origin).days.to_numpy()
                weekdays = np.eye(7)[idx.dayofweek]

                return np.column_stack((t, weekdays))

            model = LinearRegression()
            model.fit(features(train.index), train.to_numpy())

            return model.predict(features(future_dates))

        if method == "SARIMA":
            model = SARIMAX(
                train,
                order=(1, 0, 0),
                seasonal_order=(1, 0, 0, 7),
                trend="c",
                enforce_stationarity=False,
                enforce_invertibility=False
            )

            fitted = model.fit(disp=False, maxiter=100)

            return np.asarray(fitted.forecast(steps=len(future_dates)))

        raise ValueError(f"Unknown model: {method}")

    def testing(self, pre, post, horizon):

        methods = [
            "Weekday average",
            "Linear regression",
            "SARIMA"
        ]

        errors = {m: [] for m in methods}

        # Backtest the last three nonoverlapping blocks
        for i in (2, 1, 0):
            stop = len(pre) - i * horizon
            train = pre.iloc[:stop - horizon]
            actual = pre.iloc[stop - horizon:stop]

            for method in methods:
                prediction = np.asarray(self.forecast(train, actual.index, method))
                prediction = np.maximum(prediction, 0)
                error = abs(actual.sum() - prediction.sum())
                errors[method].append(error)

        scores = {
            m: np.mean(errors[m])
            for m in methods
        }
        best = min(scores, key=scores.get)
        prediction = np.asarray(self.forecast(pre, post.index, best))
        expected = np.maximum(prediction, 0).sum()
        actual = post.sum()
        incremental = actual - expected
        lift = (
            incremental / expected * 100
            if expected > 0
            else float("nan")
        )

        print(
            "MODEL COMPARISON "
            "(lower average cumulative error is better)"
        )

        for m in methods:
            print(f"  {m:18s} ${scores[m]:,.2f}")

        print(f"\nSelected model:             {best}")
        print(f"Pre-launch days:            {len(pre)}")
        print(f"Post-launch days:           {len(post)}")
        print(f"Actual post-launch sales:   ${actual:,.2f}")
        print(f"Expected sales (no launch): ${expected:,.2f}")
        print(f"Estimated incremental:      ${incremental:+,.2f}")
        print(f"Estimated lift:             {lift:+.2f}%")


if __name__ == "__main__":
    most = MOST(DATA)
    df = most.read_data()
    df, pre, post, horizon = most.prep(df, launch_date="2011-08-01")
    most.testing(pre, post, horizon)
