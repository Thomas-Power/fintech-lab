import mysql.connector

#Implementation of required functions for data retrieval and verification using MySQL server
class Database:
	#replace variables with appropriate credentials
	def __init__(self):
		self.db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="password",
			database="stock_data"
		)
		self.cursor = self.db.cursor()
	
	#retrieves time series values from database
	def select(self, values):
		sql = "SELECT * FROM relational_tickers WHERE ticker_name = %s AND time >= %s AND time <= %s"
		self.cursor.execute(sql, values)
		result = self.cursor.fetchall()
		return result
		
	#inserts time series values into database
	def insert(self, values):
		sql = "INSERT IGNORE INTO relational_tickers (time, ticker_name, value) VALUES (%s, %s, %s)"
		self.cursor.executemany(sql, values)
		self.db.commit()
	
	#retrieves meta values used to track availability of date ranges in local database
	def select_meta(self, ticker_name):
		sql_meta_select = "SELECT * FROM tickers_meta WHERE ticker_name = %s"
		self.cursor.execute(sql_meta_select, [ticker_name])
		compare_values = self.cursor.fetchall()
		return compare_values
		
	#replace meta values used to track availability of date ranges in local database	
	def replace_meta(self, values):
		sql_meta_replace = "REPLACE INTO tickers_meta (ticker_name, start_date, end_date) VALUES (%s, %s, %s)"
		self.cursor.execute(sql_meta_replace, values)
		self.db.commit()