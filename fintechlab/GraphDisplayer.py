import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from mpl_toolkits.mplot3d import Axes3D

#Displays data using matplotlib in appropriate formatting
class GraphDisplayer:
	#Simple time series data
	def simple_time_series(self, data, metric="Value in USD", title="", file_name=None):
		fig = plt.figure()
		ax=plt.gca()
		plt.title(title)
		plt.plot(data["Date"], data["Value"])
		fig.autofmt_xdate()
		if len(data["Date"]) < 90:
			ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
		plt.ylabel(metric)
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
		
	#Plots multible times series along-side eachother
	def simple_time_multiseries(self, plot_pairs, metric="Value in USD", title="", file_name=None):
		fig = plt.figure()
		ax=plt.gca()
		plt.title(title)
		for pair in plot_pairs:
			plt.plot(pair["Date"], pair["Value"])
		fig.autofmt_xdate()
		plt.ylabel(metric)
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
		
	#Cartesian graph, for showing positive and negative values
	def cross_axis(self, scatter_pairs, plot_pairs=[], axis_labels=None, title="", file_name=None):
		fig = plt.figure()
		ax=plt.gca()
		plt.title(title)
		plt.axhline(0, color='black')
		plt.axvline(0, color='black')
		for pair in scatter_pairs:
			plt.scatter(pair[0], pair[1], s=100, marker='.', alpha=0.15)
		for pair in plot_pairs:
			plt.plot(pair[0], pair[1], color='r')
		if axis_labels is not None:
			plt.xlabel(axis_labels[0])
			plt.ylabel(axis_labels[1])
		plt.ylim(ax.get_xlim())
		ax.set_aspect('equal', 'box')
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
	
	#Applys shading and color to signify density of 3rd dimension axis
	def colormesh(self, rank_three_tensor, plot_pairs=[], axis_labels=None, title="", file_name=None):
		x, y, z = rank_three_tensor
		fig = plt.figure()
		ax = plt.gca()
		ax.set_title(title)
		ax.pcolormesh(x, y, z, shading='gouraud', cmap=plt.cm.BuGn_r)
		ax.contour(x, y, z)
		for pair in plot_pairs:
			plt.plot(pair[0], pair[1])
		if axis_labels is not None:
			plt.xlabel(axis_labels[0])
			plt.ylabel(axis_labels[1])
		plt.axhline(0, color='black')
		plt.axvline(0, color='black')
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
		
	# Produces a 3D graph 
	def surface_3d(self, rank_three_tensor, plot_pairs=[], axis_labels=None, title="", file_name=None):
		x, y, z = rank_three_tensor
		fig = plt.figure()
		ax = plt.axes(projection='3d')
		ax.set_title(title)
		for pair in plot_pairs:
			plt.plot(pair[0], pair[1], plot[2])
		if axis_labels is not None:
			plt.xlabel(axis_labels[0])
			plt.ylabel(axis_labels[1])
			plt.zlabel(axis_labels[2])
		ax.plot_surface(x, y, z, cmap=plt.cm.autumn, rstride=1, cstride=1, linewidth=0)
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
		
	#Displays plotted line, appropriate for statistical distributions
	def distribution_line(self, plot_pair, scatter_pairs=[], axis_labels=None, title="", reference=0, file_name=None):
		x, y = plot_pair
		fig = plt.figure()
		ax = plt.gca()
		plt.plot(x, y, color='b')
		if axis_labels is not None:
			plt.xlabel(axis_labels[0])
			plt.ylabel(axis_labels[1])
		for pair in scatter_pairs:
			plt.scatter(pair[0], pair[1], marker='o', color="r")
		ax.set_title(title)
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
		
	#Produces a histogram
	def histogram(self, series, plot_pairs=[], scatter_pairs=[], axis_labels=None, title="", bins=100, file_name=None):
		fig = plt.figure()
		ax = plt.gca()
		plt.hist(series, bins, density=True)
		if axis_labels is not None:
			plt.xlabel(axis_labels[0])
			plt.ylabel(axis_labels[1])
		for pair in plot_pairs:
			plt.plot(pair[0], pair[1])
		for pair in scatter_pairs:
			plt.scatter(pair[0], pair[1], marker='|', color="r")
			ax.annotate(str(round(pair[0], 2)), (pair[0], pair[1]))
		ax.set_title(title)
		if file_name is None:
			plt.show()
		else:
			fig.savefig(file_name)
			plt.close()
	
	
	
	
	
	
	
	
	
	
	
	
	
