import pandas as pd

DATA_PATH = "/Users/srikarpoladi/Downloads/prooject/testing/data1/online_retail_II.csv"
CLEANED_PATH  = "/Users/srikarpoladi/Downloads/prooject/testing/data1/online_retail_II_cleaned.csv"

class DATA_PROC():
    def __init__(self, data_path):
        self.data_path = data_path

    def read_data(self):
        df = pd.read_csv(self.data_path)
        return df

    def missing(self, df):
        for col in df.columns:
            print(f"missin in {col}")
            print(df[col].isna().sum())        

    def conversion(self, df):
        int_col = "Quantity"
        date_col = "InvoiceDate"
        float_col = "Price"
        str_col = ["Description", "Country", "Invoice","StockCode"]
        col_to_conv = [int_col, date_col, float_col, str_col]
        for i in col_to_conv:
            if i == int_col:
                df[int_col] = df[int_col].astype(int)
            elif i == date_col:
                df[date_col] = pd.to_datetime(df[date_col])
            elif i == float_col:
                df[float_col] = df[float_col].astype(float)
            else:
                df["Description"] = df["Description"].fillna("unknown")
                df[str_col] = df[str_col].astype(str)
        return df

    def dropping(self, df):
        df_2 = df.drop(columns=["Customer ID", "Country"])
        df_2 = df_2[df_2["Price"] > 0]
        return df_2

    def data_quality(self, df):
        for col in df.columns:
            print(df[col].describe())

    def saving(self, df, path):
        df.to_csv(path, index=False)
        print("saveed df")

if __name__ == "__main__":
    data_proc = DATA_PROC(DATA_PATH)
    df = data_proc.read_data()
    data_proc.missing(df)
    df_conv = data_proc.conversion(df)
    df_dropped = data_proc.dropping(df_conv)
    data_proc.data_quality(df_dropped)
    data_proc.saving(df_dropped, CLEANED_PATH)

    #unit price less than 0 this is drop 5
    #check quantity less than 0 counts as return I belive 
    #need to fill missing decriptions with unknown 
    

        