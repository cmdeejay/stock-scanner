import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta


today = date.today()
start = today - relativedelta(months=1)
data = yf.download(tickers='000029.SZ', start=start, end=today)

print(data)