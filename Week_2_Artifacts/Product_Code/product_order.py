from pymongo import MongoClient
from pymongo.collection import Collection
import json
import sys

#Connection method which is responsible for returning the client object after successfully connection with MongoDb Service else will return None in case of any exception occured
def connect(host, port):
    mongo_client = None
    try:
        mongo_client = MongoClient(f'mongodb://{host}:{port}')
        
        print('Connection successfully established!')
        return mongo_client
    
    except ConnectionError as e:
        print("Exception in Connection : ", str(e))
        
    except Exception as e:
        print("Exception Occured: ", str(e))
  

#This methods aims at fetching the required db object using the provided mongo client and db name
def get_db(mongo_client, db_name):
    try:
        if mongo_client is None:
            print("MongoDB Client is not intialised")
        
        return mongo_client.get_database(db_name)
    
    except Exception as e:
        print("Exception in fetching required db : ", e)

#This methods aims at fetching the required collection object using the provided db object and collection name  
def get_collection(db_object, collection_name):
    try:
        if db_object is None:
            print("DB object is not initialised")
        
        return db_object[collection_name]
    
    except Exception as e:
        print("Exception in fetching required collection object : ", str(e))
        
        
#This method aims at inserting the provided data in json format in the given collection object
def single_insert(collection, data):
    try:
        if data is None:
            print("No data is available.")
        else:
            result = collection.insert_one(data)
            return True
        
    except Exception as e:
        print("Exception in inserting single record in collection :", e)
        return False

#This method aims at fetching single data from given collection object   
def find_single(collection, key=None, spec=None):
    try:
        result = collection.find_one(key, spec)
        print("Data fetched successfully.")
        return result
    except Exception as e:
        print("Exception in fetching single record from collection :", e)

# This method aims at fetching multiple data using the given filters from given collection object 
def find_multiple(collection, key=None, spec=None):
    try:
        result = collection.find(key, spec)
        print("Data fetched successfully.")
        return result
    except Exception as e:
        print("Exception in fetching multiple records from collection :", e)
        
def aggregate(collection, pipeline):
    try:
        result = collection.aggregate(pipeline)
        print("Data fetched successfully!")
        return result
    except Exception as e:
        print("Exception in running aggregation pipeline on the collection :", e)

def update(collection, key, spec):
    try:
        collection.update_many(key, spec)
        print("Document(s) updated successfully")
    except Exception as e:
        print("Exception while updating the collection :", e)

def delete_single(collection, key):
    try:
        collection.delete_one(key)
        print("Document deleted successfully")
    except Exception as e:
        print("Exception while deleting document from collection")

def delete_multiple(collection, key):
    try:
        collection.delete_many(key)
        print("Document(s) deleted successfully")
    except Exception as e:
        print("Exception while deleting document from collection")
        

if __name__ == "__main__":
    
    host = 'localhost'
    port = 27017
    
    mongo_client = connect(host,port)
    
    if mongo_client is None:
        sys.exit(0)

    product_order_db = get_db(mongo_client, 'product_orders_db')
    
    if product_order_db is None:
        sys.exit(0)
        
    products_collection = get_collection(product_order_db, 'products')
    
    
    if products_collection is None:
        sys.exit(0)
        
    inventory_collection = get_collection(product_order_db, 'inventory')
    
    
    if inventory_collection is None:
        sys.exit(0)
        
    users_collection = get_collection(product_order_db, 'users')
    
    
    if users_collection is None:
        sys.exit(0)
        
    orders_collection = get_collection(product_order_db, 'orders')
    
    
    if orders_collection is None:
        sys.exit(0)

    products_collection.drop()

    inventory_collection.drop()

    users_collection.drop()

    orders_collection.drop()
        
    # Populate the MongoDB collections with the JSON data

    print("\n")
    print("########################################################################################")
    print("Populate all the collections in the database, from the JSON input file")
    print("########################################################################################")
    print("\n")

    with open('db_input.json', 'r') as f:
        data = json.load(f)

        # data is a dictionary of arrays

        product_entries = data['product_entries']
        print("Product data insertion initiated")
        for product_entry in product_entries:
            single_insert(products_collection, product_entry)

        print("Product data inserted in the collection")

        print("Inventory data insertion initiated")
        inventory_entries = data['inventory_entries']
        for inventory_entry in inventory_entries:
            single_insert(inventory_collection, inventory_entry)

        print("Inventory data inserted in the collection")

        print("User data insertion initiated")
        user_entries = data['user_entries']
        for user_entry in user_entries:
            single_insert(users_collection, user_entry)

        print("User data inserted in the collection")

        print("Orders data insertion initiated")
        order_entries = data['order_entries']
        for order_entry in order_entries:
            single_insert(orders_collection, order_entry)

        print("Orders data inserted in the collection")
    
    # read the collection contents, one-by-one

    print("\n")
    print("########################################################################################")
    print("List all the collections in the database")
    print("########################################################################################")
    print("\n")

    collection_names = product_order_db.list_collection_names()
    print("All Collection Names in product order db : ", collection_names)

    print("\n")
    print("########################################################################################")
    print("Retrieve a single document from each collection")
    print("########################################################################################")
    print("\n")

    products_doc = find_single(products_collection)
    print(products_doc)

    inventories_doc = find_single(inventory_collection)
    print(inventories_doc)

    users_doc = find_single(users_collection)
    print(users_doc)

    orders_doc = find_single(orders_collection)
    print(orders_doc)
    
    ########################################################################################
    # Simple Read Queries
    ########################################################################################
    
    # Simple read queries with products

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with Product SKU SNY-11001 from Products collection")
    print("########################################################################################")
    print("\n")

    key = {"sku": "SNY-11001"}
    product_doc = find_single(products_collection, key)
    print(product_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with Product SKU SNY-11001 from Products collection, with only specific fields")
    print("########################################################################################")
    print("\n")

    spec = {"_id": 0, "brand": 1, "model": 1, "price": 1}
    product_doc = find_single(products_collection, key, spec)
    print(product_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve a NON-EXISTENT document with Product SKU SNY-11002 from Products collection")
    print("########################################################################################")
    print("\n")

    key = {"sku": "SNY-11002"}
    product_doc = find_single(products_collection, key)
    print(product_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve all documents with Brand name Samsung from Products collection")
    print("########################################################################################")
    print("\n")

    key = {"brand": "Samsung"}
    cursor = find_multiple(products_collection, key, spec)
    for doc in cursor:
        print(doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve all NON-EXISTENT documents with Brand name Huawei from Products collection")
    print("########################################################################################")
    print("\n")

    key = {"brand": "Huawei"}
    cursor = find_multiple(products_collection, key, spec)
    for doc in cursor:
        print(doc)

    
    # Simple read queries with inventory

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with Product SKU LLG-32001 from Inventory collection")
    print("########################################################################################")
    print("\n")

    key = {"sku": "LLG-32001"}
    inv_doc = find_single(inventory_collection, key)
    print(inv_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with Product SKU LLG-32001 from Inventory collection, with only specific fields")
    print("########################################################################################")
    print("\n")

    spec = {"_id": 0, "sku": 1, "quantity": 1}
    inv_doc = find_single(inventory_collection, key, spec)
    print(inv_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve the NON-EXISTENT document with Product SKU LLG-32002 from Inventory collection")
    print("########################################################################################")
    print("\n")

    key = {"sku": "LLG-32002"}
    inv_doc = find_single(inventory_collection, key)
    print(inv_doc)

    
    # Simple read queries with users

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with email ID nisha.arora@evermail.com from Users collection")
    print("########################################################################################")
    print("\n")

    key = {"email": "nisha.arora@evermail.com"}
    user_doc = find_single(users_collection, key)
    print(user_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve the document with email ID nisha.arora@evermail.com from Users collection, with only specific feilds")
    print("########################################################################################")
    print("\n")

    spec = {"_id": 0, "name": 1, "email": 1, "role": 1}
    user_doc = find_single(users_collection, key, spec)
    print(user_doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve the NON-EXISTENT document with email ID xyz@mymail.com from Users collection")
    print("########################################################################################")
    print("\n")

    key = {"email": "xyz@mymail.com"}
    user_doc = find_single(users_collection, key)
    print(user_doc)

    
    # Simple read queries with orders

    print("\n")
    print("########################################################################################")
    print("Retrieve all the documents for orders placed by user with email ID sudha.nat@yourmail.com from Orders collection")
    print("########################################################################################")
    print("\n")

    key = {"user_email": "sudha.nat@yourmail.com"}
    cursor = find_multiple(orders_collection, key)
    for doc in cursor:
        print(doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve all the documents for orders placed by user with email ID sudha.nat@yourmail.com from Orders collection, with only specific fields")
    print("########################################################################################")
    print("\n")

    spec = {"_id": 0, "user_email": 1, "items": 1, "net_price": 1}
    cursor = find_multiple(orders_collection, key, spec)
    for doc in cursor:
        print(doc)

    print("\n")
    print("########################################################################################")
    print("Retrieve all the NON-EXISTENT documents for orders placed by user with email ID albertz@yourmail.com from Orders collection")
    print("########################################################################################")
    print("\n")

    key = {"user_email": "albertz@yourmail.com"}
    cursor = find_multiple(orders_collection, key)
    for doc in cursor:
        print(doc)

    ########################################################################################
    # More Read Queries
    ########################################################################################

    # Find all product SKUs that have price not less than 100000

    print("\n")
    print("########################################################################################")
    print("Find all product SKUs that have price not less than 100000")
    print("########################################################################################")
    print("\n")

    key = {"price": {"$gte": 100000}}
    spec = {"_id": 0, "product_sku": 1, "brand": 1, "model": 1, "price": 1}
    cursor = find_multiple(products_collection, key, spec)
    for doc in cursor:
        print(doc)

    # Find all orders that include a purchase of the product SKUs among "SMG-21001" and "SNY-11001"

    print("\n")
    print("########################################################################################")
    print("Find all orders that include a purchase of the product SKUs among SMG-21001 and SNY-11001")
    print("########################################################################################")
    print("\n")

    key = {
        "items.product_sku": {
            "$in": ["SMG-21001", "SNY-11001"]
        }
    }
    spec = {"user_email": 1, "items.product_sku": 1}
    cursor = find_multiple(orders_collection, key, spec)
    for doc in cursor:
        print(doc)

    # Find all orders that include the Product SKU "SMG-21001" and that are also with status code 2

    print("\n")
    print("########################################################################################")
    print("Find all orders that include the Product SKU SMG-21001 and that are also with status code 2")
    print("########################################################################################")
    print("\n")

    key = {"items.product_sku": "SMG-21001", "status": 2}
    spec = {"_id": 0, "user_email": 1, "items_product_sku": 1, "status": 1, "last_updated": 1}
    cursor = find_multiple(orders_collection, key, spec)
    for doc in cursor:
        print(doc)

    ########################################################################################
    # Aggregation Queries
    ########################################################################################

    # Find the average cost of an order placed by any user 

    print("\n")
    print("########################################################################################")
    print("Find the average cost of an order placed by any user")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
            "$group": {
                "_id": "avg_order_cost",
                "avg_order_cost": {
                    "$avg": "$net_price"
                }
            }
        }
    ]

    cursor = aggregate(orders_collection, pipeline)

    for doc in cursor:
        print(doc)

    # Find the average cost of an order placed by users, categorized by user

    print("\n")
    print("########################################################################################")
    print("Find the average cost of an order placed by users, categorized by user")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
            "$group": {
                "_id": "$user_email",
                "avg_order_cost": {
                    "$avg": "$net_price"
                }
            }
        }
    ]
    
    cursor = aggregate(orders_collection, pipeline)

    for doc in cursor:
        print(doc)

    # # List the count of product SKUs available across Product brands, grouped by brand

    print("\n")
    print("########################################################################################")
    print("List the count of product SKUs available across Product brands, grouped by brand")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
            "$group": {
                "_id": "$brand",
                "count": {"$sum": 1}
            }
        },
    ]

    cursor = aggregate(products_collection, pipeline)
    
    for doc in cursor:
        print(doc)

    # Return the 3 product items with the least quantity in the inventory

    print("\n")
    print("########################################################################################")
    print("Return the 3 product items with the least quantity in the inventory")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
            "$sort": {
                "quantity": 1
            }
        },
        {
            "$limit": 3
        },
        {
            "$project": {
                "_id": 0,
                "sku": 1,
                "quantity": 1
            }
        }
    ]

    cursor = aggregate(inventory_collection, pipeline)

    for doc in cursor:
        print(doc)

    # Return all the product items in the inventory that have less than 150 units each

    print("\n")
    print("########################################################################################")
    print("Return all the product items in the inventory that have less than 150 units each, sorted lowest first")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
            "$match": {
                "quantity": {
                    "$lt": 150
                }
            }
        },
        {
        	"$sort": {
        		"quantity": 1
        	}
        },
        {
            "$project": {
                "_id": 0,
                "sku": 1,
                "quantity": 1
            }
        }
    ]

    cursor = aggregate(inventory_collection, pipeline)

    for doc in cursor:
        print(doc)

    # Find out the highest-priced item purchased by a particular user, among all the 
    # purchases he/she has made at the eCommerce site

    print("\n")
    print("########################################################################################")
    print("Find out the highest-priced item purchased by a particular user, among all the purchases he/she has made at the eCommerce site")
    print("########################################################################################")
    print("\n")

    pipeline = [
    	{
            "$match": {
                "user_email": {
                    "$eq": "nisha.arora@evermail.com"
                }
            }
        },
        {
    		"$unwind": "$items"
    	},
    	{
        	"$project": {
                "_id": 0,
                "user_email": 1,
                "items.product_sku": 1,
                "items.unit_price": 1

        	}
        },
        {
            "$sort": {
                "items.unit_price": -1
            }
        },
        {
        	"$limit": 1
        }
    ]

    cursor = aggregate(orders_collection, pipeline)

    for doc in cursor:
        print(doc)

    # Find out the Product SKU that has been the highest selling item by count

    print("\n")
    print("########################################################################################")
    print("Find out the Product SKU that has been the highest selling item by count")
    print("########################################################################################")
    print("\n")

    pipeline = [
        {
    		"$unwind": "$items"
    	},
    	{
            "$group": {
                "_id": "$items.product_sku",
                "count": {"$sum": 1}
            }
        },
        {
            "$sort": {
                "count": -1
            }
        },
        {
        	"$limit": 1
        }
    ]

    cursor = aggregate(orders_collection, pipeline)

    for doc in cursor:
        print(doc)

    ########################################################################################
    # Indexing
    ########################################################################################

    # Find all product SKUs that have price not less than 100000

    print("\n")
    print("########################################################################################")
    print("Find all product SKUs that have price not less than 100000")
    print("########################################################################################")
    print("\n")

    print("WITHOUT INDEXING")
    print("########################################################################################")

    key = {"price": {"$gte": 100000}}
    stats = find_multiple(products_collection, key).explain()
    print(stats['executionStats'])

    products_collection.create_index("price", name="price_index")
    products_collection.index_information()

    print("########################################################################################")
    print("WITH INDEXING")
    print("########################################################################################")

    stats = find_multiple(products_collection, key).explain()
    print(stats['executionStats'])

    products_collection.drop_index("price_index")
    products_collection.index_information()

    # Find all orders that include a purchase of the product SKUs among "SMG-21001" and "SNY-11001"

    print("\n")
    print("########################################################################################")
    print("Find all orders that include a purchase of the product SKUs among SMG-21001 and SNY-11001")
    print("########################################################################################")
    print("\n")

    print("WITHOUT INDEXING")
    print("########################################################################################")

    key = {
        "items.product_sku": {
            "$in": ["SMG-21001", "SNY-11001"]
        }
    }
    spec = {"user_email": 1, "items.product_sku": 1}
    stats = find_multiple(orders_collection, key, spec).explain()
    print(stats['executionStats'])

    orders_collection.create_index("items.product_sku", name="sku_index")
    orders_collection.index_information()

    print("########################################################################################")
    print("WITH INDEXING")
    print("########################################################################################")

    stats = find_multiple(orders_collection, key, spec).explain()
    print(stats['executionStats'])

    orders_collection.drop_index("sku_index")
    orders_collection.index_information()


    # Find out the highest-priced item purchased by a particular user, among all the 
    # purchases he/she has made at the eCommerce site

    print("\n")
    print("########################################################################################")
    print("Find out the highest-priced item purchased by a particular user, among all the purchases he/she has made at the eCommerce site")
    print("########################################################################################")
    print("\n")

    print("WITHOUT INDEXING")
    print("########################################################################################")

    pipeline = [
    	{
            "$match": {
                "user_email": {
                    "$eq": "nisha.arora@evermail.com"
                }
            }
        },
        {
    		"$unwind": "$items"
    	},
    	{
        	"$project": {
                "_id": 0,
                "user_email": 1,
                "items.product_sku": 1,
                "items.unit_price": 1

        	}
        },
        {
            "$sort": {
                "items.unit_price": -1
            }
        },
        {
        	"$limit": 1
        }
    ]

    

    stats = product_order_db.command('aggregate', 'orders', pipeline=pipeline, explain=True)
    
    print(stats)

    orders_collection.create_index("user_email", name="email_index")
    orders_collection.index_information()

    print("########################################################################################")
    print("WITH INDEXING")
    print("########################################################################################")

    stats = product_order_db.command('aggregate', 'orders', pipeline=pipeline, explain=True)
    
    print(stats)

    orders_collection.drop_index("email_index")
    orders_collection.index_information()

    ########################################################################################
    # Update and Delete Queries
    ########################################################################################

    # Update the email address of the user, who originally had the email ID "nisha.arora@evermail.com", 
    # to "arora.nisha@origmail.net"

    print("\n")
    print("########################################################################################")
    print("Update the email address of the user, who originally had the email ID nisha.arora@evermail.com, to arora.nisha@origmail.net")
    print("########################################################################################")
    print("\n")

    key = {"email": "nisha.arora@evermail.com"}
    spec = {
        "$set": {
            "email": "arora.nisha@origmail.net"
        }
    }

    user_doc = find_single(users_collection, key)
    print(user_doc)


    print("########################################################################################")
    print("AFTER UPDATE")
    print("########################################################################################")

    update(users_collection, key, spec)    

    key = {"email": "arora.nisha@origmail.net"}
    user_doc = find_single(users_collection, key)
    print(user_doc)
    
    # Increment the quantity of the Product SKU "APL-01001" in the inventory, by 20

    print("\n")
    print("########################################################################################")
    print("Increment the quantity of the Product SKU APL-01001 in the inventory, by 20")
    print("########################################################################################")
    print("\n")

    key = {"sku": "APL-01001"}
    spec = {
        "$inc": {
            "quantity": 20
        }
    }

    inv_doc = find_single(inventory_collection, key)
    print(inv_doc)


    print("########################################################################################")
    print("AFTER UPDATE")
    print("########################################################################################")

    update(inventory_collection, key, spec)

    inv_doc = find_single(inventory_collection, key)
    print(inv_doc)

    # Remove the warranty information from the Product with SKU "PNS-18001"

    print("\n")
    print("########################################################################################")
    print("Remove the warranty information from the Product with SKU PNS-18001")
    print("########################################################################################")
    print("\n")

    key = {"sku": "PNS-18001"}
    spec = {"$unset": {"warranty": 1}}

    product_doc = find_single(products_collection, key)
    print(product_doc)


    print("########################################################################################")
    print("AFTER UPDATE")
    print("########################################################################################")

    update(products_collection, key, spec)

    product_doc = find_single(products_collection, key)
    print(product_doc)


    # Delete entries from the Orders collection, originally placed by the user with email ID "anjali.gupta@zestmail.com"

    print("\n")
    print("########################################################################################")
    print("Delete entries from the Orders collection, originally placed by the user with email ID anjali.gupta@zestmail.com")
    print("########################################################################################")
    print("\n")

    key = {"user_email": "anjali.gupta@zestmail.com"}

    order_docs = find_multiple(orders_collection, key)
    for order_doc in order_docs:
        print(order_doc)


    print("########################################################################################")
    print("AFTER DELETE")
    print("########################################################################################")

    delete_multiple(orders_collection, key)

    order_docs = find_multiple(orders_collection, key)
    for order_doc in order_docs:
        print(order_doc)
