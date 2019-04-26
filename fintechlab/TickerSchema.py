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
		
	def get_meta_values(Ticker):
		ticker_name = str(Ticker["ticker_name"].iloc[0])
		start_date = str(Ticker["Date"].iloc[0])
		end_date = str(Ticker["Date"].iloc[-1])
		return ticker_name, start_date, end_date