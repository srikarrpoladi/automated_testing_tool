import pandas as pd

#less than 14 days
DATA = "/Users/srikarpoladi/Downloads/prooject/testing/data1/complete.csv"

class LOW():
    def __init__(self, path):
        self.path = path

    def read_data(self, launch_data, end_date):
        df = pd.read_csv(self.path)
        df = df[(df["date"] >= "2010-02-01") & (df["date"] <= "2010-02-28")]
        return df[["date"] < launch_data], df[(df["date"] >= launch_data) & (df["date"] < "2010-02-28")]

    def less_than_14_sales(self, df_before, df_after):
        daily_avg_sales_before = df_before["total_rev"].mean()
        daily_avg_sales_after = df_after["total_rev"].mean()
        obs_change_pct_sales = ((daily_avg_sales_after/daily_avg_sales_before) - 1) * 100

        return daily_avg_sales_before, daily_avg_sales_after, obs_change_pct_sales

    def less_than_14_ord_cnt(self, df_before, df_after):
        daily_avg_ord_cnt_before = df_before["ord_cnt"].mean()
        daily_avg_ord_cnt_after = df_after["ord_cnt"].mean()
        obs_change_pct_ord_cnt = ((daily_avg_ord_cnt_after/daily_avg_ord_cnt_before) - 1) * 100

        return daily_avg_ord_cnt_before, daily_avg_ord_cnt_after, obs_change_pct_ord_cnt

    def less_than_14_units(self, df_before, df_after):
        daily_avg_units_before = df_before["units"].mean()
        daily_avg_units_after = df_after["units"].mean()
        obs_change_pct_units = ((daily_avg_units_after/daily_avg_units_before) - 1) * 100

        return daily_avg_units_before, daily_avg_units_after, obs_change_pct_units

if __name__ == "__main__":
    low = LOW(DATA)
    df_before, df_after = low.read_data(launch_data="2010-02-13", end_date="2010-02-28")
    daily_avg_sales_before, daily_avg_sales_after, obs_change_pct_sales = low.less_than_14_sales(df_before, df_after)
    daily_avg_ord_cnt_before, daily_avg_ord_cnt_after, obs_change_pct_ord_cnt = low.less_than_14_ord_cnt(df_before, df_after)
    daily_avg_units_before, daily_avg_units_after, obs_change_pct_units = low.less_than_14_units(df_before, df_after)

    print(f"daily average sales before launch ${round(daily_avg_sales_before,2)}")
    print(f"daily average sales after launch ${round(daily_avg_sales_after,2)}")
    print(f"Observed Change in sales before vs after {round(obs_change_pct_sales,2)}%")
    print("--------------------------------------------------------------------------")
    print(f"daily average order count before launch {round(daily_avg_ord_cnt_before,2)}")
    print(f"daily average order count after launch {round(daily_avg_ord_cnt_after,2)}")
    print(f"Observed Change in order count before vs after {round(obs_change_pct_ord_cnt,2)}%")
    print("--------------------------------------------------------------------------")
    print(f"daily average units sold before launch {round(daily_avg_units_before,2)}")
    print(f"daily average units sold after launch {round(daily_avg_units_after,2)}")
    print(f"Observed Change in units sold before vs after {round(obs_change_pct_units,2)}%")