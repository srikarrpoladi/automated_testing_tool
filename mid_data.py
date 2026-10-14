import pandas as pd

DATA = "/Users/srikarpoladi/Downloads/prooject/testing/data1/complete.csv"
#14-55 days of historical data

class MID():
    def __init__(self, path):
        self.path = path

    def read_data(self):
        df = pd.read_csv(self.path)
        df["date"] = pd.to_datetime(df["date"])
        df = df[(df["date"] >= "2010-02-01") & (df["date"] <= "2010-04-20")]

        return df
    
    def by_day(self, df, launch_date, end_date):
        df["day_name"] = df["date"].dt.day_name()
        df_before = df[df["date"] < launch_date]
        df_after = df[(df["date"] >= launch_date) & (df["date"] < end_date)]

        before_by_day = df_before.groupby("day_name").agg( sales_avg=("total_rev", "mean"),  avg_ords=("ord_cnt", "mean"), avg_units=("units", "mean") )

        df_after["expected_revenue"] = df_after["day_name"].map(before_by_day["sales_avg"])
        df_after["expected_units"] = df_after["day_name"].map(before_by_day["avg_units"])
        df_after["expected_ords"] = df_after["day_name"].map(before_by_day["avg_ords"])

        sales_after = df_after["total_rev"].sum()
        sales_expected = df_after["expected_revenue"].sum()

        units_after = df_after["units"].sum()
        units_expected = df_after["expected_units"].sum()

        ords_after = df_after["ord_cnt"].sum()
        ords_expected =  df_after["expected_ords"].sum()

        return {
            "actual sales" : sales_after,
            "expected sales" : sales_expected,
            "estimated impact sales" : sales_after - sales_expected,
            "estimated sales lift pct" : round(((sales_after/sales_expected) - 1) * 100, 2),

            "actual units" : units_after,
            "expected units" : units_expected,
            "estimated impact_units" : units_after - units_expected,
            "estimated units lift_pct" : round(((units_after/units_expected) - 1) * 100, 2),
            
            "actual ords" : ords_after,
            "expected ords" : ords_expected,
            "estimated impact ords" : ords_after - ords_expected,
            "estimated ords lift pct" : round(((ords_after/ords_expected) - 1) * 100, 2),
        }

        return 


if __name__ == "__main__":
    mid = MID(DATA)
    df = mid.read_data()
    results = mid.by_day(df, launch_date="2010-03-20", end_date="2010-04-20")
    for metric, score in results.items():
        score = round(score, 2)
        if 'pct' in metric:
            print(f"{metric} : {score}%")
        elif 'sales' in metric:
            print(f"{metric} : ${score}")
        else:
            print(f"{metric} : {score}")