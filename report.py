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
        self.filePath = r"files/report.csv"
        self.newFile = r'C:\Users\Min Chen\Development\Stock-Scanner\Files\output.xlsx'
        self.today = date.today()
        self.start = date.today() + relativedelta(months=-3)
        self.exportList = pd.DataFrame()
        self.solution = pd.DataFrame()
        self.symbols = []
        self.table = pd.read_csv(open(self.filePath, encoding="ANSI"), sep='\t=', names=['Order', 'symbol', 'Name', 'Yoy', 'small cap', 'big cap'], header=None, index_col=None, engine='python')
        self.table_new = self.table[1:]['symbol'].str.replace('"', '')
        self.names = self.table[1:]['Name'].str.replace('"', '').to_list()
        self.data = yf.download(self.dataclean(), start=self.start, end=self.today)['Adj Close']
        self.exportList = self.exportList.append(self.data)
        self.daily_returns = self.data.pct_change()

    def _exportListSheet(self):  # Download Data
        self.exportList = self.exportList.append(self.data)
        return self.exportList

    def dataclean(self):  # Return the list of symbol
        symbols = []
        for i in range(len(self.table_new)):
            if int(self.table_new.iloc[i]) > 600000:
                symbol = self.table_new.iloc[i] + '.SS'
            else:
                symbol = self.table_new.iloc[i] + '.SZ'
            symbols.append(symbol)
        return symbols

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
