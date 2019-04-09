from AnalyzerAdapter import AnalyzerAdapter
from DatabaseAdapter import DatabaseAdapter
from GraphDisplayer import GraphDisplayer

#A high level class used to conveniently source data and produce graphs using other libraries in the package
class GraphFactory:
	def __init__(self):
		self.analyzer = AnalyzerAdapter()
		self.db = DatabaseAdapter()
		self.graphDisplay = GraphDisplayer()
		
	#Sources data for and produces a time series displaying the gaussian propability of a tickers current value relative
	#to its distance from its linear regressed analogue
	def source_series_of_gaussian_probability_of_divergence_from_linear_regression(self, symbol, start_date, end_date=None, length_days=50):
		series = self.db.select(symbol, start_date, end_date)
		self.series_of_gaussian_probability_of_divergence_from_linear_regression(series, length_days)
		
	#Sources data for and produces a time series displaying the gaussian propability of a tickers current value relative
	#to its distance from its linear regressed analogue
	def source_relational_series_of_gaussian_probability_of_divergence_from_linear_regression(self, symbol_one, symbol_two, start_date, end_date=None, length_days=50):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		relational_series = self.analyzer.get_series_relation(series_one, series_two)
		self.series_of_gaussian_probability_of_divergence_from_linear_regression(relational_series, length_days)
		
	#Produces a time series displaying the gaussian propability of a tickers current value relative
	#to its distance from its linear regressed analogue
	def series_of_gaussian_probability_of_divergence_from_linear_regression(self, data, length_days=50):
		result = self.analyzer.get_series_of_gaussian_probability_of_divergence_from_linear_regression(data, length_days)
		self.linear_regress_simple_time_series(result, "Probability")
		
	#Sources data for and produces a histogram of a commodities value in a specified period of time
	def source_time_series_histogram(self, symbol, start_date, end_date=None, metric="Value in USD", bins=100):
		data = self.db.select(symbol, start_date, end_date)
		self.time_series_histogram(data, metric, bins)
	
	#Produces a histogram of a commodities value in a specified window of time
	def time_series_histogram(self, data, metric="Value in USD", bins=100):
		symbol = data["ticker_name"].iloc[0]
		start = str(data["Date"].iloc[0])
		end = str(data["Date"].iloc[-1])
		title = "Value of " + symbol + " from " + start + " to " + end
		self.graphDisplay.histogram(data["Value"], axis_labels=[metric, "Probability"], title=title, bins=bins)
		
	#Sources data for and produces a guassian representation of a commodities value in a specified window of time
	def source_time_series_gaussian(self, symbol, start_date, end_date=None, metric="Value in USD"):
		data = self.db.select(symbol, start_date, end_date)
		self.time_series_distribution(data, metric)
		
	#Produces a guassian representation of a commodities value in a specified window of time
	def time_series_gaussian(self, data, metric="Value in USD"):
		symbol = data["ticker_name"].iloc[0]
		start = str(data["Date"].iloc[0])
		end = str(data["Date"].iloc[-1])
		title = "Value of " + symbol + " from " + start + " to " + end
		distribution =  self.analyzer.get_gaussian_distribution(data)
		self.graphDisplay.distribution_line(distribution, axis_labels=[metric, "Probability"], title=title)
		
	#Sources data for and displays the beta relationship of two commodities displaying frequency on a colormesh heat map
	def source_colormesh_beta_relationship(self, symbol_one, symbol_two, start_date, end_date=None, days_increment=5, data_partitions=64):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.colormesh_beta_relationship(series_one, series_two, days_increment, data_partitions) 
	
	#Sources data for and displays the beta relationship of two commodities displaying frequency on a colormesh heat map
	#Relates the two commodities in terms of the value of a common metric
	def source_relational_colormesh_beta_relationship(self, symbol_one, symbol_two, common_metric, start_date, end_date=None, days_increment=5, data_partitions=64):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		dji = self.db.select(common_metric, start_date, end_date)
		series_one = self.analyzer.get_series_relation(series_one, dji)
		series_two = self.analyzer.get_series_relation(series_two, dji)
		self.colormesh_beta_relationship(series_one, series_two, days_increment, data_partitions) 
		
	#Displays the beta relationship of two commodities displaying frequency on a colormesh heat map
	def colormesh_beta_relationship(self, commodity_one, commodity_two, days_increment=5, data_partitions=64):
		change_one = self.analyzer.percent_change_series(commodity_one, days_increment)
		change_two = self.analyzer.percent_change_series(commodity_two, days_increment)
		kde = self.analyzer.kernal_density_estimation(change_one, change_two, data_partitions)
		symbol_one = commodity_one["ticker_name"].iloc[0]
		symbol_two = commodity_two["ticker_name"].iloc[0]
		axis_labels = [symbol_one + " % Change", symbol_two + " % Change"]
		title = "β - Relationship " + symbol_one + " to " + symbol_two
		self.graphDisplay.colormesh(kde, axis_labels=axis_labels, title=title)
		
	#Sources data for and displays the distribution of the beta relationship between 
	#two commodities at a specific slice of the first symbols price movement
	def source_beta_relationship_distribution_slice(self, symbol_one, symbol_two, percent_change, start_date, end_date=None, days_increment=5, data_partitions=64):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.beta_relationship_distribution_slice(series_one, series_two, percent_change, days_increment, data_partitions) 
		
	#Displays the distribution of the beta relationship between two commodities at 
	#a specific slice of the first symbols price movement
	def beta_relationship_distribution_slice(self, commodity_one, commodity_two, percent_change, days_increment=5, data_partitions=64):
		change_one = self.analyzer.percent_change_series(commodity_one, days_increment)
		change_two = self.analyzer.percent_change_series(commodity_two, days_increment)
		kde = self.analyzer.kernal_density_estimation(change_one, change_two, data_partitions)
		x_value, y_series, z_series = self.analyzer.get_distribution_slice_from_tensor(kde, percent_change)
		maximum_point = self.analyzer.get_maximum_vector(y_series, z_series)
		symbol_one = commodity_one["ticker_name"].iloc[0]
		symbol_two = commodity_two["ticker_name"].iloc[0]
		axis_labels = [symbol_two + " % Change", "Probability"]
		title = symbol_one + " when " + symbol_two + " changes " + str(round(x_value, 2)) + "%"
		self.graphDisplay.distribution_line([y_series, z_series], [maximum_point], axis_labels, title)
		
	#Sources data for and displays the beta relationship of two commodities displaying frequency on a colormesh heat map
	#and displays a linear regression of the relationship
	def source_colormesh_linear_regress_beta_relationship(self, symbol_one, symbol_two, start_date, end_date=None, days_increment=5):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.colormesh_linear_regress_beta_relationship(series_one, series_two, days_increment)
	
	#Displays the beta relationship of two commodities and displays a linear regression of the relationship
	def colormesh_linear_regress_beta_relationship(self, commodity_one, commodity_two, days_increment=None):
		change_one = self.analyzer.percent_change_series(commodity_one, days_increment)
		change_two = self.analyzer.percent_change_series(commodity_two, days_increment)
		data_lr = self.analyzer.linear_regress_series(change_one, change_two)
		kde = self.analyzer.kernal_density_estimation(change_one, change_two)
		symbol_one = commodity_one["ticker_name"].iloc[0]
		symbol_two = commodity_two["ticker_name"].iloc[0]
		axis_labels = [symbol_one + " % Change", symbol_two + " % Change"]
		title = "β - Relationship " + symbol_one + " to " + symbol_two
		self.graphDisplay.colormesh(kde, [[data_lr["Value"], change_two["Value"]]], axis_labels, title)
	
		
	#Sources the data for and displays the beta relationship of two commodities	
	def source_beta_relationship(self, symbol_one, symbol_two, start_date, end_date=None, days_increment=5):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.beta_relationship(series_one, series_two, days_increment)
	
	#Displays the beta relationship of two commodities
	def beta_relationship(self, commodity_one, commodity_two, days_increment=None):
		change_one = self.analyzer.percent_change_series(commodity_one, days_increment)
		change_two = self.analyzer.percent_change_series(commodity_two, days_increment)
		data_lr = self.analyzer.linear_regress_series(change_one, change_two)
		symbol_one = commodity_one["ticker_name"].iloc[0]
		symbol_two = commodity_two["ticker_name"].iloc[0]
		axis_labels = [symbol_one + " % Change", symbol_two + " % Change"]
		title = "β - Relationship " + symbol_one + " to " + symbol_two
		self.graphDisplay.cross_axis([[change_one["Value"].values.tolist(), change_two["Value"].values.tolist()]], [[data_lr["Value"], change_two["Value"]]], axis_labels, title)
		
	#Sources the data for and displays the beta relationship of two commodities	as a 3D graph
	def source_beta_relationship_3d(self, symbol_one, symbol_two, start_date, end_date=None, days_increment=5):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.beta_relationship_3d(series_one, series_two, days_increment)
		
	#Displays the beta relationship of two commodities as a 3D graph
	def beta_relationship_3d(self, series_one, series_two, days_increment=None):
		change_one = self.analyzer.percent_change_series(series_one, days_increment)
		change_two = self.analyzer.percent_change_series(series_two, days_increment)
		kde = self.analyzer.kernal_density_estimation(change_one, change_two)
		symbol_one = series_one["ticker_name"].iloc[0]
		symbol_two = series_two["ticker_name"].iloc[0]
		axis_labels = [symbol_one + " % Change", symbol_two + " % Change", "Probability density"]
		title = "β - Relationship " + symbol_one + " to " + symbol_two
		self.graphDisplay.surface_3d(kde, axis_labels=axis_labels, title=title)
	
	#Displays the time series value of a commodity in terms of the value of another
	def relational_series(self, commodity_one, commodity_two):
		data = self.analyzer.get_series_relation(commodity_one, commodity_two)
		title = "Value of " + data["ticker_name"].iloc[0] + " over time"
		self.graphDisplay.simple_time_series(data, "Relative Value", title)
		
	#Sources the data for and displays time series value of a commodity in terms of the value of another
	def source_relational_series(self, symbol_one, symbol_two, start_date, end_date=None):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.relational_series(series_one, series_two)
	
	#Displays time series value of a commodity in terms of the value of another along with 
	#the linear regression of the series
	def linear_regress_relational_series(self, commodity_one, commodity_two):
		data = self.analyzer.get_series_relation(commodity_one, commodity_two)
		title = "Value of " + data["ticker_name"].iloc[0] + " over time"
		lr_data = self.analyzer.linear_regress_time_series(data)
		self.graphDisplay.simple_time_multiseries([data, lr_data], "Relative Value", title)
		
	#Sources the data for and displays the time series value of a commodity in terms of the value of another 
	#along with the linear regression of the series
	def source_linear_regress_relational_series(self, symbol_one, symbol_two, start_date, end_date=None):
		series_one = self.db.select(symbol_one, start_date, end_date)
		series_two = self.db.select(symbol_two, start_date, end_date)
		self.linear_regress_relational_series(series_one, series_two)
		
	#Sources the data for and displays a time series of data
	def source_simple_time_series(self, symbol, start_date, end_date=None, metric="Value in USD"):
		data = self.db.select(symbol, start_date, end_date)
		self.simple_time_series(data, metric)
		
	#Displays a time series of data
	def simple_time_series(self, data, metric="Value in USD"):
		title = "Value of " + data["ticker_name"].iloc[0] + " over time"
		self.graphDisplay.simple_time_series(data, metric, title)
		
	#Sources the data for and displays a time series of two commodities along-side each other
	def source_simple_time_multiseries(self, symbol_one, symbol_two, start_date, end_date=None, metric="Value in USD"):
		data_one = self.db.select(symbol_one, start_date, end_date)
		data_two = self.db.select(symbol_two, start_date, end_date)
		self.simple_time_multiseries([data_one, data_two], metric)
		
	#Displays multiple time series in parrelel
	def simple_time_multiseries(self, data, metric="Value in USD"):
		title = "Value over time"
		self.graphDisplay.simple_time_multiseries(data, metric, title)
		
	#Displays the plot and linear regression of a time series
	def linear_regress_simple_time_series(self, data, metric="Value in USD"):
		title = data["ticker_name"].iloc[0]
		lr_data = self.analyzer.linear_regress_time_series(data)
		self.graphDisplay.simple_time_multiseries([data, lr_data], metric, title)
		
	#Sources the data for and plots a time series and its linear regression
	def source_linear_regress_simple_time_series(self, symbol, start_date, end_date=None, metric="Value in USD"):
		data = self.db.select(symbol, start_date, end_date)
		self.linear_regress_simple_time_series(data, metric)
		
		
		