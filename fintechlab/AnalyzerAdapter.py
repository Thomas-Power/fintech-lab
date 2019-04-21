import pandas as pd
import numpy as np
from fintechlab.TickerSchema import TickerSchema
from fintechlab.DataAnalyzer import DataAnalyzer

#Class used to format data to retain modular independence of analyzer class
class AnalyzerAdapter:
	def __init__(self):
		self.analyzer = DataAnalyzer()
		
	def get_divergence_from_linear_regression(self, series):
		series_r = self.linear_regress_time_series(series)
		divergence = series["Value"].values - series_r["Value"].values
		ticker_name = series["ticker_name"] + " divergence from linear regression"
		return TickerSchema.create(series["Date"], ticker_name, divergence)


	def get_series_relation(self, series_one, series_two):
		date = series_one["Date"]
		ticker_name = series_one["ticker_name"] + " / " + series_two["ticker_name"]
		value = self.analyzer.get_series_relation(series_one["Value"], series_two["Value"])
		return TickerSchema.create(date, ticker_name, value)
		
	def linear_regress_time_series(self, series):
		value = np.vstack(series['Value'].values)
		date = np.vstack(np.arange(0, len(series['Date'].values)))
		value_pred = self.analyzer.linear_regress_series(value, date)
		return TickerSchema.create(series["Date"], series["ticker_name"], value_pred)
		
	def linear_regress_series(self, series_x, series_y):
		x_values = np.vstack(series_x['Value'].values)
		y_values = np.vstack(series_y['Value'].values)
		value_pred = self.analyzer.linear_regress_series(x_values, y_values)
		ticker_name = series_x["ticker_name"].iloc[0] + "'s linear relationship to " + series_y["ticker_name"].iloc[0]
		return TickerSchema.create(series_x["Date"], ticker_name, value_pred)
		
	def percent_change_series(self, series, days_increment=5):
		percent_change = self.analyzer.percent_change_series(series["Value"].values, days_increment)
		series = series[::days_increment]
		return TickerSchema.create(series["Date"][1:], series["ticker_name"][1:], percent_change)
		
	def change_series(self, series, days_increment=5):
		percent_change = self.analyzer.change_series(series["Value"].values, days_increment)
		series = series[::days_increment]
		return TickerSchema.create(series["Date"][1:], series["ticker_name"][1:], percent_change)
		
	def kernal_density_estimation(self, x_series, y_series, nbins = 64):
		x_series = x_series["Value"].values
		y_series = y_series["Value"].values
		return self.analyzer.kernal_density_estimation(x_series, y_series, nbins)
		
	def get_distribution_slice_from_tensor(self, tensor, x_value):
		x, y , z = tensor
		x = x[:,0]
		return self.analyzer.get_distribution_slice_from_tensor(x, y, z, x_value)
		
	def get_maximum_vector(self, x_series, y_series):
		return self.analyzer.get_maximum_vector(x_series, y_series)
		
	def get_p_date_on_guassian(self, time_series, date=-1):
		value_today = time_series["Value"].iloc[date]
		series = time_series["Value"].values
		return self.analyzer.p_on_gaussian(series, value_today)
		
	def gaussian_probability_of_divergence_from_linear_regression(self, data, view, i):
			i_data = data.iloc[i-view:i]
			i_data = self.get_divergence_from_linear_regression(i_data)
			today = self.get_p_date_on_guassian(i_data)
			sign = 1 if (today[1] > 0) else -1
			return today[0] * sign
			
	def get_series_of_gaussian_probability_of_divergence_from_linear_regression(self, data, view):
		results = []
		for i in range(view, len(data), 1):
			probality = self.gaussian_probability_of_divergence_from_linear_regression(data, view, i)
			results.append(probality)
		results = np.vstack(results)
		symbol = data["ticker_name"]
		ticker_name = "Probability of " +  symbol + " divergence from " + str(view) + " day linear regression"
		return TickerSchema.create(data["Date"].iloc[view:len(data)], ticker_name, results)		
	
	def get_gaussian_distribution(self, time_series):
		return self.analyzer.gaussian_distribution(time_series["Value"].values)
		
	def get_beta_distribution(self, time_series):
		return self.analyzer.beta_distribution(time_series["Value"].values)
		
	def get_distributive_gaussian_projection(self, data, projection, forward_length):
		projection_values = self.analyzer.distributive_gaussian_projection(data["Value"].values, projection, forward_length)
		projection_dates = pd.date_range(start=data["Date"].iloc[-1], periods=forward_length+1)
		ticker_name = data["ticker_name"] + " " + str(forward_length) + " day projection"
		return TickerSchema.create(projection_dates, ticker_name, projection_values)		
	
	
	
	