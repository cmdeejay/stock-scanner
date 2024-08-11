import pandas as pd
import numpy as np
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
import os
from pandas import ExcelWriter


class StockScaner:
    def __init__(self):
        yf.pdr_override()
        self.filePath = r"files/expected_report.csv"
        self.newFile = r'C:\Users\10171\Development\stockscanner\files\expected_output.xlsx'
        self.today = date.today()
        self.start = date.today() + relativedelta(months=-3)
        self.exportList = pd.DataFrame()
        self.solution = pd.DataFrame()
        self.symbols = []
        self.table = pd.read_csv(self.filePath, header=None, index_col=None)
        self.table_new = self.table.iloc[0:, 1]
        self.names = self.table.iloc[0:, 2].to_list()
        self.data = yf.download(self.dataclean(), start=self.start, end=self.today)['Adj Close']
        self.daily_returns = self.data.pct_change().sort_values(by=['Date'])

    def _exportListSheet(self):  # Download Data
        self.exportList = self.exportList.append(self.data)
        return self.exportList

    def dataclean(self):  # Return the list of symbol
        for i in range(len(self.table_new)):
            if self.table_new.iloc[i] > 600000:
                symbol = str(self.table_new.iloc[i]) + '.SS'
            else:
                symbol = str(self.table_new.iloc[i]) + '.SZ'
                if len(symbol) == 8:
                    symbol = "0" + symbol
                elif len(symbol) == 7:
                    symbol = "00" + symbol
                elif len(symbol) == 6:
                    symbol = "000" + symbol
                elif len(symbol) == 5:
                    symbol = "0000" + symbol
                elif len(symbol) == 4:
                    symbol = "00000" + symbol
            self.symbols.append(symbol)
        return self.symbols

    def _solutionSheet(self):     # Solution: Assign attributes
        self.solution['daily_std'] = self.daily_returns.std()
        self.solution['daily_average'] = self.daily_returns.mean()
        self.solution['annual_std'] = self.daily_returns.std() * np.sqrt(252)
        self.solution['annual_average'] = self.daily_returns.mean() * 252
        self.solution['ratio'] = self.solution['annual_average'] / self.solution['annual_std']
        self.solution['names'] = self.names
        self.solution.sort_values(by=['ratio'], ascending=False, inplace=True)
        self.solution.reset_index(inplace=True)
        return self.solution

    def export(self):
        writer = ExcelWriter(self.newFile)
        self._exportListSheet().to_excel(writer, "Sheet1")
        self.daily_returns.to_excel(writer, "Daily_returns")
        self._solutionSheet().to_excel(writer, "Solution")
        writer.save()
        os.startfile(self.newFile)


Scanner = StockScaner()
Scanner.export()

