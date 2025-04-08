import yfinance as yf
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


today = date.today()
start = today - relativedelta(months=1)
end = today + timedelta(days=1)
print(end)
data = yf.download(tickers='000029.SZ', start=start, end=end)
data = data["Close"]

print(data)