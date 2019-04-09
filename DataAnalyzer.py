import pandas as pd
import numpy as np
from sklearn import linear_model
from scipy.stats import beta
from scipy.stats import kde
from scipy.stats import lognorm
from scipy.stats import norm
import math

#Object to contain relevant mathematical operations
class DataAnalyzer:
	def get_series_relation(self, x_series, y_series):
		return x_series / y_series
		
	def linear_regress_series(self, x_series, y_series):
		x_series = np.vstack(x_series)
		y_series = np.vstack(y_series)
		
		regr = linear_model.LinearRegression()
		regr.fit(y_series, x_series)
		y_pred = regr.predict(y_series)
		return y_pred
		
	def percent_change_series(self, data, days_increment=5):
		data = data[::days_increment]
		return ((data[:-1] / data[1:]) -1) * 100
		
	def change_series(self, data, days_increment=5):
		data = data[::days_increment]
		return (data[:-1] / data[1:])
		
	def percent_change_series(self, data, days_increment=5):
		data = data[::days_increment]
		return (data[:-1] / data[1:])
		
	def kernal_density_estimation(self, x_series, y_series, nbins=64):
		data = np.array([np.vstack(x_series), np.vstack(y_series)])
		data.shape = (2, int(data.size/2))
		data = data.T
		k = kde.gaussian_kde(data.T)
		xi, yi = np.mgrid[x_series.min():x_series.max():nbins*1j, y_series.min():y_series.max():nbins*1j]
		zi = k(np.vstack([xi.flatten(), yi.flatten()]))
		result = (xi, yi, zi.reshape(xi.shape))
		return result
		
	def get_distribution_slice_from_tensor(self, x_series, y_array, z_array, x_value):
		bucketed_indice = np.digitize(x_value, x_series)
		x_bucketed = x_series[bucketed_indice]
		y_series = y_array[bucketed_indice]
		z_series = z_array[bucketed_indice]
		result = (x_bucketed, y_series, z_series)
		return result
		
	def get_maximum_vector(self, x_series, y_series):
		max_y = np.amax(y_series)
		index_max = np.where(y_series == np.amax(y_series))
		return [x_series[index_max][0], max_y]
		
	def divergence_from_linear_regression(self, x_series, y_series):
		data_r = self.linear_regress_series(x_series, y_series)
		return x_series - data_r
		
	def distributive_gaussian_projection(self, series, projection, forward_length, include_latest=True):
		growth_rate = self.change_series(series)
		mu = np.mean(growth_rate)
		sigma = np.std(growth_rate)
		projected_growth_rate = norm.ppf(projection)
		latest = series[-1]
		print(projected_growth_rate)
		result = []
		if include_latest:
			result.append(latest)
		for i in range(0, forward_length, 1):
			latest = latest * projected_growth_rate
			result.append(latest)
		return result
		
	def gaussian_distribution(self, series, i=100):
		mu = np.mean(series)
		sigma = np.std(series)
		x_scale = np.linspace(mu - 3*sigma, mu + 3*sigma, i)
		y_distribution = norm.pdf(x_scale, mu, sigma)
		return (x_scale, y_distribution)
		
	def p_on_gaussian(self, series, value):
		mu = np.mean(series)
		sigma = np.std(series)
		probability = norm.cdf(value, mu, sigma) /100
		return (value, probability)
		
	def beta_distribution(self, series):
		a, b, loc, scale = beta.fit(series)
		x_pdf = np.linspace(beta.ppf(0.01, a, b), beta.ppf(0.99, a, b), 100)
		x = np.linspace(loc, scale+loc, 100)
		y = beta.pdf(x_pdf, a, b, scale=scale)
		return (x, y)