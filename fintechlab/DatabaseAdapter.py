import datetime
from fintechlab.RestAdapter import RestAdapter
from fintechlab.Database import Database
from fintechlab.TickerSchema import TickerSchema

#Adapter class, used to verify and prepare data for input and output from database 
#and keep actual database implementation independent from greater system
class DatabaseAdapter:
	def __init__(self):
		self.restadapter = RestAdapter()
		self.db = Database()

	#inserts time series values into database
	def insert(self, values):
		print("Adding data...")
		self.db.insert(list(values.itertuples(index=False, name=None)))
		
	#retrieves time series values from database
	def select(self, ticker_name, start_date, end_date=None):
		if end_date is None:
			end_date=datetime.date.today().strftime("%Y-%m-%d")
		if self.dates_are_unavailable(ticker_name, start_date, end_date):
			request_data = self.restadapter.get_daily_prices(ticker_name).values.tolist()
			self.db.insert(request_data)
		values = [ticker_name, start_date, end_date]
		result = self.db.select(values)
		result = TickerSchema.create_from_list(result)
		return result
		
	def select_derivitive(self, ticker_name, start_date, end_date=None):
		if end_date is None:
			end_date=datetime.date.today().strftime("%Y-%m-%d")
		values = [ticker_name, start_date, end_date]
		result = self.db.select(values)
		result = TickerSchema.create_from_list(result)
		return result
	
	#Verifies if data is available offline, otherwise sources data from REST API
	def dates_are_unavailable(self, ticker_name, start_date, end_date):
		replace_values = False
		new_values = [ticker_name, start_date, end_date]
		compare_values = self.db.select_meta(ticker_name)
		if compare_values is not None and len(compare_values) != 0:
			compare_values = compare_values[0]
			old_start = compare_values[1]
			old_end = compare_values[2]
			
			new_start = datetime.datetime.strptime(new_values[1], "%Y-%m-%d").date()
			new_end = datetime.datetime.strptime(new_values[2], "%Y-%m-%d").date()
			
			if old_start <= new_start:
				new_values[1] = old_start
			else:
				replace_values = True
			
			if old_end >= new_end:
				new_values[2] = old_end
			else:
				replace_values = True
		else:
			replace_values = True
		
		if replace_values:
			print("Data not available in database...")
			self.db.replace_meta(new_values)
		return replace_values