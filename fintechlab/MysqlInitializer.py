import mysql.connector

#Initializes MySQL database and necessary tables
class MysqlInitializer:
	def setup(self):
		self.build_database_and_connect()
		self.build_table()

	def build_database_and_connect(self):
		db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="password"
		)

		mycursor = db.cursor()
		mycursor.execute("SHOW DATABASES")
		no_database = True

		for x in mycursor:
			if(x[0] == "stock_data"):
				no_database = False

		if no_database:
			mycursor.execute("SHOW DATABASES")
			mycursor.execute("CREATE DATABASE stock_data")


	def build_table(self):
		db = mysql.connector.connect(
			host="localhost",
			user="root",
			passwd="password",
			database="stock_data"
		)
		mycursor = db.cursor()
		mycursor.execute("SHOW TABLES")
		no_table = True

		for x in mycursor:
			if x[0] == "relational_tickers":
				no_table = False

		if no_table:
			mycursor.execute("CREATE TABLE relational_tickers (time DATE, ticker_name VARCHAR(255), value FLOAT(12,5), PRIMARY KEY (time, ticker_name))")
			mycursor.execute("CREATE TABLE tickers_meta (ticker_name VARCHAR(255), start_date DATE, end_date DATE, PRIMARY KEY (ticker_name))")
		