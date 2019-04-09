import pandas as pd

#Schema used to keep time series data consistent for package operations
class TickerSchema:
	def create(Date, ticker_name, Value):
		df = pd.DataFrame()
		df["Date"] = Date
		df["ticker_name"] = ticker_name
		df["Value"] = Value
		return df
		
	def create_from_list(data):
		return pd.DataFrame(data, columns=["Date", "ticker_name", "Value"])