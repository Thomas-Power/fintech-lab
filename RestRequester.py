import requests

#Makes call to retrieve data from alphavantage
class RestRequester:
	def __init__(self):
		self.HTTP = "https://www.alphavantage.co/query?"
		self.DATATYPE = "&datatype=csv"
		self.APIKEY = "&apikey=NGWAIYPTBUN0C0JZ"

	def source_daily_prices(self, symbol, outputsize):
		function = "&function=TIME_SERIES_DAILY"
		symbol = "&symbol=" + symbol
		outputsize = "&outputsize=" + outputsize
		r = requests.get(self.HTTP + function + symbol + outputsize + self.DATATYPE + self.APIKEY)
		return r.content
