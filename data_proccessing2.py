import pandas as pd

DATA_PATH = "/Users/srikarpoladi/Downloads/prooject/testing/data1/online_retail_II_cleaned.csv"
COMPLETE_DATA = "/Users/srikarpoladi/Downloads/prooject/testing/data1/complete.csv"

class DATA_PROC2():
    def __init__(self, data_path):
        self.path = data_path

    def read_data(self):
        df = pd.read_csv(self.path)
        return df

    def agg_data(self, df):
        df = df.sort_values("InvoiceDate")
        df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
        df["date"] = df["InvoiceDate"].dt.date
        df["total_price"] = df["Quantity"] * df["Price"]
        df_agg = df.groupby("date", as_index=False).agg( total_rev=("total_price", "sum"), ord_cnt=("Invoice","nunique"),  units=("Quantity","count") )
        return df_agg
    
    def saveing(self, df, path):
        df.to_csv(path, index=False)
        print("saved data")


if __name__ == "__main__":
    data_proc2 = DATA_PROC2(DATA_PATH)
    df = data_proc2.read_data()
    df_agg = data_proc2.agg_data(df)
    data_proc2.saveing(df_agg, COMPLETE_DATA)
    #print(df_agg.head(50))
    #print(f"size of df {len(df_agg)}")