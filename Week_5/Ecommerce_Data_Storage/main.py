import database as db
import setup as stp
# Driver code
if __name__ == "__main__":
    """
    Please enter the necessary information related to the DB at this place. 
    Please change PW and ROOT based on the configuration of your own system. 
    """
    PW = "Goksenin7!"  # IMPORTANT! Put your MySQL Terminal password here.
    ROOT = "root"
    DB = "ecommerce_record"  # This is the name of the database we will create in the next step - call it whatever
    # you like.
    LOCALHOST = "localhost"
    #Get DB Connection from database

    # Start implementing your task as mentioned in the problem statement
    # Implement all the test cases and test them by running this file

    #Get Connection from DB
    connection = db.create_db_connection(LOCALHOST, ROOT, PW, DB)

    #PROBLEM STATEMENT 2.B INSERT FIVE DIFFERENT ORDERS
    print("\n")

    Insert_five_different_orders_dif_customers = """
        INSERT INTO orders VALUES
        (101, 120000, 7, 100, 1,13),
        (102, 130000, 8, 200, 3,11),
        (103,14000, 9, 100,4, 6),
        (104, 15000, 10, 200,2, 8),
        (105, 16000, 11, 100,1, 9)        
        """
    db.create_insert_query(connection,Insert_five_different_orders_dif_customers)

    print("2.B INSERT FIVE DIFFERENT ORDERS DONE !\n")

    #PROBLEM STATEMENT 2.C FETCH ALL THE RECORDS AND PRINT DATA ON SCREEN

    print("2.C ROWS FIND FETCH ALL THE RECORDS OF THE ORDERS\n")
    Q1_Query_Select_All_Orders = """
        SELECT * from orders
        """
    Q1_DataSet=db.select_query(connection, Q1_Query_Select_All_Orders)
    for row in Q1_DataSet:
        print(row)

    print("\n")

    #PROBLEM STATEMENT 3.A FROM ORDERS TABLE WRITE A QUERY TO FIND MAXIMUM and MINIMUM ORDER VALUE
    print("3.A ROWS Find the maximum and minimum order value\n")
    Q2_Query_Select_MIN_MAX_Orders = """
        select MIN(total_value),MAX(total_value) from orders
        """
    Q2_DataSet=db.select_query(connection, Q2_Query_Select_MIN_MAX_Orders)
    print("MIN, MAX VALUES ARE ", Q2_DataSet)
    print("\n")

    #PROBLEM SATTEMENT 3.B Fetch and print the orders with value (total_value) greater than the average value (total_value) of all the orders in the orders table
    print("3.B ROWS value (total_value) greater than the average value (total_value)\n")
    Q3_Greater_AVG_Value= """
        select * from orders where total_value> (
            select avg(total_value) from orders);             
        """
    Q3_DataSet = db.select_query(connection, Q3_Greater_AVG_Value)
    for row in Q3_DataSet:
        print(row)
    print("\n")

    #PROBLEM SATTEMENT 3.C Insert one row for each registered customer who has made a purchase. And fill the (total_value) of this table, with the highest purchase value (total_value) of the orders table for a customer. In case a customer has not made any purchase, then do not add a record of the customer
    print("3.C Insert one row for each registered customer who has made a purchase. And fill the (total_value) of this table, with the highest purchase value (total_value) of the orders table for a customer. In case a customer has not made any purchase, then do not add a record of the customer.)\n")

    Q4_Highest_Purchase_Customer= """
    INSERT INTO customer_leaderboard (customer_id, total_value, customer_name, customer_email)
    SELECT o.customer_id, MAX(o.total_value) AS total_value, u.user_name, u.user_email
    FROM orders o
    JOIN users u ON o.customer_id = u.user_id
    GROUP BY o.customer_id
    HAVING total_value > 0;
    """
    Q4_DataSet = db.select_query(connection, Q4_Highest_Purchase_Customer)
    print("Data Inserted Successfully\n")
    print("Fetch Customer_LeaderBoard\n")

    Q5_Fetch_Customer_Leader_Board = """
           SELECT * from customer_leaderboard
           """
    Q5_DataSet = db.select_query(connection, Q5_Fetch_Customer_Leader_Board)
    for row in Q5_DataSet:
        print(row)

    print("\n")








