import pandas
import datetime
from RestAdapter import RestAdapter
from Database import Database
from TickerSchema import TickerSchema

#Adapter class, used to verify and prepare data for input and output from database 
#and keep actual database implementation independent from greater system
class DatabaseAdapter:
	def __init__(self):
		self.restadapter = RestAdapter()
		self.db = Database()

	#inserts time series values into database
	def insert(self, values):
		self.db.insert(values)
	
	#retrieves time series values from database
	def select(self, ticker_name, start_date, end_date=None):
		if end_date is None:
			end_date=datetime.date.today().strftime("%Y-%m-%d")
		self.verify_dates_available(ticker_name, start_date, end_date)
		values = [ticker_name, start_date, end_date]
		result = self.db.select(values)
		result = TickerSchema.create_from_list(result)
		return result
		
	#replace meta values used to track availability of date ranges in local database
	def replace_meta(self, new_values):
		self.db.replace_meta(new_values)
	
	#Verifies if data is available offline, otherwise sources data from REST API
	def verify_dates_available(self, ticker_name, start_date, end_date):
		replace_values = False
		new_values = [ticker_name, start_date, end_date]
		compare_values = self.db.select_meta(ticker_name)
		
		if compare_values != []:
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
			request_data = self.restadapter.get_daily_prices(ticker_name).values.tolist()
			if len(request_data) > 0:
				print("Adding new data...")
				self.db.insert(request_data)
				self.db.replace_meta(new_values)
			else:
				print("No data found from request!")	