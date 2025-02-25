import pandas as pd
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import numpy as np


class StockScanner:
    def __init__(self):
        pass

    def read_csv(self):
        filepath = r"files/weeklyreport.csv"
        df = pd.read_csv(
            filepath,
            names=["orders", "symbol", "name", "small cap", "big_cap"],
            header=None,
            index_col=None,
        )
        self.names = df["name"].tolist()
        self.names = self.names[1:]
        self.tickers = df["symbol"].values.tolist()
        self.tickers = self.tickers[1:]
        return self.tickers

    def transform(self):
        self.new_tickers = []
        for ticker in self.tickers:
            if int(ticker) > 600000:
                ticker = ticker + ".SS"
            else:
                ticker = ticker + ".SZ"
            self.new_tickers.append(ticker)

    def download(self):
        today = date.today()
        start = today - relativedelta(months=1)
        self.data = yf.download(tickers=self.new_tickers, start=start, end=today)
        self.data = self.data["Close"]
        return self.data

    def daily_returns(self):
        self.df_daily_return = self.data.pct_change(fill_method=None).sort_values(by=["Date"])

        return self.df_daily_return

    def solutions(self):
        self.solution = pd.DataFrame()
        self.solution["daily_std"] = self.df_daily_return.std()
        self.solution["daily_avg"] = self.df_daily_return.mean()
        self.solution["annual_std"] = self.solution["daily_std"] * np.sqrt(252)
        self.solution["annual_avg"] = self.solution["daily_avg"] * 252
        self.solution["ratio"] = (
            self.solution["annual_avg"] / self.solution["annual_std"]
        )
        self.solution["std>0.7"] = self.solution["annual_std"] > 0.7
        self.solution["names"] = self.names
        self.solution.sort_values(by=["ratio"], ascending=False, inplace=True)
        self.solution.reset_index(inplace=True)
        return self.solution

    def to_excel(self):
        newfile = r"weekly_output.xlsx"
        writer = ExcelWriter(newfile)
        self.data.to_excel(writer, sheet_name="Daily price")
        self.df_daily_return.to_excel(writer, sheet_name="Daily returns")
        self.solution.to_excel(writer, sheet_name="Solution")
        writer._save()
        print("report is done!")

    def main(self):
        self.read_csv()
        self.transform()
        self.download()
        self.daily_returns()
        self.solutions()
        self.to_excel()


scan = StockScanner().main()
