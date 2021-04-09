# A. Steps to run the code
Latest version of Python (3.*) should be installed on your system. It comes with pip installed by default. Then follow below steps:
1. (Required) Clone the project to local 
2. (Optional) Enable your virtual environment
3. (Required) `$ pip install -r requirements.txt`
4. (Required) To Run the project- 
    `$ python etl.py`

Now, you may download sqlite DB browser to see the data in the products.sqlite DB.
https://sqlitebrowser.org/dl/

# Details of all the tables and their schema
We are using a sqlite3 database (products.sqlite)
1. Table 1: "PRODUCTS" \
    columns: ID, NAME, SKU, DESCRIPTION
    Table is created if not exists using the same python script.
    SQL Query Used: `CREATE table IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, sku TEXT, description TEXT)`
2. Table 2: "AGGREGATE" \
    columns: NAME, NO_OF_PRODUCTS
    Table is created if not exists using the same python script.
    SQL Query Used: `CREATE table IF NOT EXISTS aggregate as select name, count(*) as 'no_of_products' from products GROUP BY sku"`


# Points to achieve
1. Your code should follow concept of OOPS \
   -> It follows OOPS concepts- Class, Object, Constructor (To declare variables and build DB connection), Destructor (to destroy the object and close the connection).

2. Support for regular non-blocking parallel ingestion of the given file into a table. Consider thinking about the
scale of what should happen if the file is to be processed in 2 mins. \
   -> The code populates the given CSV within 30 seconds into the SQlite DB. The reason is that, I used a execute many operation which will ingest a chunck of data at once into the table.

3. Support for updating existing products in the table based on `sku` as the primary key. (Yes, we know about the
kind of data in the file. You need to find a workaround for it) \
   -> I introduced another column as `ID` (Autoincrement) for this purpose. Now, if someone wants to update a row based on sku then they must used `ID` field as well. In short, we can consider `ID` alone or `ID` and `SKU` to form a Candidate Key for updating the information.

4. All product details are to be ingested into a single table \
   -> This is achieved. Table name is Products.

5. An aggregated table on above rows with `name` and `no. of products` as the columns \
   -> Aggregate table is also created into the DB based on a group by on `sku`.

# What would you improve if given more days
I'd wish to do this using ETL tools like Informatica or Apache NiFi. But, the data filtering or advance validations can be done on the server end before we ingest the flat file data into a DB.