import sqlite3 as sql
import pandas as pd


class Dataingestion:
    # Constructor to create and instantiate connection to the DB
	def __init__(self):
		self.chunksize = 10000
		self.sql_data = 'products.sqlite'
		self.con = sql.connect(self.sql_data)
		self.cur = self.con.cursor()

	# Destructor to close the connection
	def __del__(self):
		self.cur.close()
		self.con.close()
	
	# Data Ingestion into SQlite3
	def ingest_data(self):
		# Create the table
		self.cur.execute(
			"create table IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sku TEXT, description TEXT)")
		try:
			for df in pd.read_csv('products.csv', chunksize=self.chunksize, index_col=0):
				# get output ready for database export
				output = df.itertuples()
				data = tuple(output)
				# Fill the table
				self.cur.executemany(
					"insert into products (name, sku, description) values (?,?,?)", data)
			# Commit only if all the data is ingested without error.
			self.con.commit()
			return True, 'success'
		except Exception as e:
			return False, e

	# create aggregate table
	def aggregate(self):
		try:
			self.cur.execute(
				"create table IF NOT EXISTS aggregate as select name, count(*) as 'no_of_products' from products GROUP BY sku")
			self.con.commit()
			return True, 'success'
		except Exception as e:
			return False, e


if __name__ == '__main__':
	dataingestion = Dataingestion()

	is_ingested, status = dataingestion.ingest_data()
	is_created, agg_status = dataingestion.aggregate()
	
	if is_ingested and status == 'success':
		print('Data Ingestion Completed!')
	else:
		print('Data Ingestion Failed!')
		print(status)
	
	if is_created and agg_status == 'success':
    		print('Aggregate Table Created Successfully!')
	else:
		print('Aggregate Table Creation Failed!')
		print(agg_status)

	del dataingestion

