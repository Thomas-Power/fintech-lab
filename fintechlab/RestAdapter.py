import pandas
import io
from fintechlab.RestRequester import RestRequester
from fintechlab.TickerSchema import TickerSchema

#Class to format data to and from call to REST api
class RestAdapter:
	def __init__(self):
		self.requester = RestRequester()
		
	def get_daily_prices(self, symbol, outputsize="full"):
		data = self.requester.source_daily_prices(symbol, outputsize)
		result = self.format_daily_prices(data, symbol)
		return result
		
	def format_daily_prices(self, data, symbol):	
		df = pandas.read_csv(io.StringIO(data.decode('utf-8')))
		return TickerSchema.create(df["timestamp"], symbol, df["open"])

