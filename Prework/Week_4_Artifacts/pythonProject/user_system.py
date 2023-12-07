# Driver code
from db_utils import create_server_connection, create_db_connection, create_insert_query, \
    create_user_system_database


def create_user_db_tables(connection):
    print("Creating users Table")
    create_insert_query(connection, create_user_table())  # Execute our defined query
    print("Done")
    print("Creating user access control Table")
    create_insert_query(connection, create_user_access_control_table())  # Execute our defined query
    print("Done")


def create_user_table():
    # creating the users table to hold the user basic information
    return """
    	CREATE TABLE users (
    	  user_id varchar(20) PRIMARY KEY,
    	  user_name varchar(45) NOT NULL,
    	  email varchar(45) NOT NULL,
    	  phone_no varchar(45) NOT NULL,
    	  address varchar(160) NOT NULL
    	)
    	"""


def create_user_access_control_table():
    # creating a table to map the access control of each type od entity
    # location, device, area in a single table
    # this reduces the need to introdice foreign key concept in this table
    return """
    	CREATE TABLE user_access_control (
    	  id int NOT NULL PRIMARY KEY,
    	  user_id varchar(45) NOT NULL,
    	  access_entity_type varchar(45) NOT NULL,
    	  entity_id varchar(45) NOT NULL,
    	  access_type varchar(20) NOT NULL,
    	  CONSTRAINT `fk_user_id_access` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
    	)
    	"""


if __name__ == "__main__":
    """
    Please enter the necessary information related to the DB at this place. 
    Please change PW and ROOT based on the configuration of your own system. 
    """
    PW = "Goksenin7!"  # IMPORTANT! Put your MySQL Terminal password here.
    ROOT = "root"
    DB = "Users_Database"  # This is the name of the database we will create in the next step - call it whatever you like.
    LOCALHOST = "localhost"
    connection = create_server_connection(LOCALHOST, ROOT, PW)

    # creating the schema in the DB
    create_user_system_database(connection, DB, DB)

    connection = create_db_connection(LOCALHOST, ROOT, PW, DB)  # Connect to the Database

    create_user_db_tables(connection)

    insert_user = """
    INSERT INTO users VALUES
    ('user101',  'John Doe', 'john@example.com', '665-877-8852', '790 Kozey Meadow Apt. 175 Kozeyside, WA 99871-1865'),
    ('user102',  'Alice cooper', 'alice@example.com', '134-345-5430', '8589 Miller Centers Leannonmouth, OR 18781-6843'),
    ('user103',  'Bob Willis', 'bob@example.com', '300-052-5450', '958 Gerry Estate New Eudora, MT 89349-0462')
    """
    create_insert_query(connection, insert_user)

    user_access_control_table = """
    INSERT INTO user_access_control VALUES
    (1, 'user101', 'location', 'PSBG101', 'Normal'),
    (2, 'user101', 'location', 'PSFG102', 'Admin'),
    (3, 'user102', 'location', 'CIHG101', 'Admin'),
    (4, 'user101', 'device', 'device101', 'Normal'),
    (5, 'user101', 'device', 'device102', 'Admin'),
    (6, 'user102', 'area', 'area101', 'Admin')
    """
    create_insert_query(connection, user_access_control_table)
