import csv
import database as db

PW = "Goksenin7!"  # IMPORTANT! Put your MySQL Terminal password here.
ROOT = "root"
DB = "ecommerce_record"  # This is the name of the database we will create in the next step - call it whatever you like.
LOCALHOST = "localhost"  # considering you have installed MySQL server on your computer

RELATIVE_CONFIG_PATH = '../config/'

USER = 'users'
PRODUCTS = 'products'
ORDER = 'orders'

connection = db.create_server_connection(LOCALHOST, ROOT, PW)

#1.A CREATING THE DATABASE
db.create_and_switch_database(connection, DB, DB)
print("1.A CREATING THE DATABASE DONE ! \n")

#1.B CREATING THE REQUIRED TABLES
def create_tabels(connection):
    print("Step1:Creating Users Table")
    db.create_table(connection, create_users_table())  # Execute our defined query
    print("Creating Users Table Done")

    print("Step2:Creating Customer Leader Board")
    db.create_table(connection, create_customer_leaderboard_table())  # Execute our defined query
    print("Creating Customer Table Done")

    print("Step3:Creating Orders Table")
    db.create_table(connection, create_orders_table())  # Execute our defined query
    print("Creating Orders Table Done")

    print("Step4:Creating Products Table")
    db.create_table(connection, create_products_table())  # Execute our defined query
    print("Creating Products Table Done")

    print("ALL Table Creations Completed")

    print("\n")
    print("1.B CREATING TABLES DONE ! \n")

#3.C CREATE Customer_Leaderboard Table
def create_customer_leaderboard_table():
    # creating the users table to hold the user basic information
    return """
    	CREATE TABLE customer_leaderboard (
    	  customer_id varchar(10) PRIMARY KEY,
    	  total_value DOUBLE NOT NULL,
    	  customer_name VARCHAR(50) NOT NULL,
    	  customer_email VARCHAR(50) NOT NULL,
    	  CONSTRAINT cust_leader_board_customer_id FOREIGN KEY (customer_id) REFERENCES users(user_id)    	  
    	  
    	)
    	"""


def create_users_table():
        return """
    	CREATE TABLE users(
    	  user_id VARCHAR(10) NOT NULL PRIMARY KEY,
    	  user_name varchar(45) NOT NULL,
    	  user_email varchar(45) NOT NULL,
    	  user_password varchar(45) NOT NULL,
    	  user_address varchar(45) NOT NULL,
    	  is_vendor TINYINT(1))
    	"""

def create_orders_table():
    return """
    	CREATE TABLE orders(
    	  order_id INT NOT NULL PRIMARY KEY,
    	  total_value DOUBLE NOT NULL,
    	  order_quantity INT NOT NULL,
    	  reward_point INT NOT NULL,
    	  vendor_id varchar(10) NOT NULL,
    	  customer_id VARCHAR(10),
    	  CONSTRAINT fk_orders_vendor_id FOREIGN KEY (vendor_id) REFERENCES users(user_id),
    	  CONSTRAINT fk_orders_customer_id FOREIGN KEY (customer_id) REFERENCES users(user_id)              	  
    	)
    	"""

def create_products_table():
    return """
    	CREATE TABLE products(
    	  product_id VARCHAR(45) NOT NULL PRIMARY KEY,
    	  product_name VARCHAR(45) NOT NULL,
    	  product_description VARCHAR(100) NOT NULL,
    	  product_price DOUBLE NOT NULL,
    	  emi_available varchar(10) NOT NULL,
    	  vendor_id VARCHAR(10) NOT NULL,
    	  CONSTRAINT fk_products_vendor_id FOREIGN KEY (vendor_id) REFERENCES users(user_id)   	     	  
    	)
    	"""

#Trigger the Table Creations
create_tabels(connection)

# if you have created the table in UI, then no need to define the table structure
# If you are using python to create the tables, call the relevant query to complete the creation


# 2.A PROBLEM STATEMENT - INSERT METHOD IN THE RELEVANT CSV FILE
with open(RELATIVE_CONFIG_PATH + USER + '.csv', 'r') as f:
    val = []
    data = csv.reader(f)
    for row in data:
        val.append(tuple(row))
    val.pop(0)

    sql = """insert into users(user_id, user_name, user_email, user_password, user_address, is_vendor)
                 values(%s,%s,%s,%s,%s,%s)"""
    db.insert_many_records(connection=connection, sql=sql, val=val)

    print("2.A USERS TABLE INSERTION DONE ! \n")
    """
    Here we have accessed the file data and saved into the val data struture, which list of tuples.
    Now you should call appropriate method to perform the insert operation in the database.
    """

with open(RELATIVE_CONFIG_PATH + PRODUCTS + '.csv', 'r') as f:
    val = []
    data = csv.reader(f)
    for row in data:
        val.append(tuple(row))
    val.pop(0)

    sql = """insert into products(product_id,product_name,product_price,product_description,vendor_id,emi_available)
                   values(%s,%s,%s,%s,%s,%s)"""
    db.insert_many_records(connection=connection, sql=sql, val=val)

    print("2.A PRODUCTS TABLE INSERTION DONE ! \n")

    """
    Here we have accessed the file data and saved into the val data struture, which list of tuples. 
    Now you should call appropriate method to perform the insert operation in the database. 
    """

with open(RELATIVE_CONFIG_PATH + ORDER + '.csv', 'r') as f:
    val = []
    data = csv.reader(f)
    for row in data:
        val.append(tuple(row))

    val.pop(0)

    sql = """insert into orders(order_id,customer_id,vendor_id,total_value,order_quantity,reward_point)
                       values(%s,%s,%s,%s,%s,%s)"""
    db.insert_many_records(connection=connection, sql=sql, val=val)

    print("2.A ORDER TABLE INSERTION DONE ! \n")
    """
    Here we have accessed the file data and saved into the val data struture, which list of tuples. 
    Now you should call appropriate method to perform the insert operation in the database. 
    """
