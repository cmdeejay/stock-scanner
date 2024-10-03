import pandas as pd
from pyspark.sql import SparkSession
import yfinance as yf
from datetime import date
from dateutil.relativedelta import relativedelta
from pandas import ExcelWriter
import numpy as np


class StockScanner:
    def __init__(self):
        pass

    def read_csv(self):
        spark = SparkSession.builder.appName("report").getOrCreate()
        filepath = r"files/weeklyreport.csv"
        df = spark.read.csv(path=filepath, header=True)
        values_list = df.select("股票代码").rdd.flatMap(lambda x: x).collect()
        print(values_list)
        pandas_df = df.toPandas()
        print(pandas_df)

    def main(self):
        self.read_csv()


scan = StockScanner().main()
