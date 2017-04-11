#!/usr/bin/python3 
import psycopg2 # PACKAGE TO DO ODBC TO POSTGRESQL
import sys
import pandas as pd # DATAFRAMES
from configparser import ConfigParser # PARSE THROUGH INI FILE

# READ .ini FILE AND PARSE THROUGH TO GET ALL RELEVANT TO CONNECT TO ODBC
config = ConfigParser()
config.read('database.ini')
print(config.sections())

def ConfigSectionMap(section):
    dict1 = {}
    options = config.options(section)
    for option in options:
        try:
            dict1[option] = config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

host = ConfigSectionMap("PostgreSQL")['host']
database = ConfigSectionMap("PostgreSQL")['database']
user = ConfigSectionMap("PostgreSQL")['user']

port = ConfigSectionMap("PostgreSQL")['port']
password = ConfigSectionMap("PostgreSQL")['password']


def main():
	# Let's define our connection string
	conn_string = "host={0} dbname = {1} user = {2} port = {3} password = {4}".format(host, database, user, port, password)

	# print the connection string we will use to connect
	print("Connecting to database\n ->")

	# get a connection, if a connect cannot be made an exception will be raised here
	conn = psycopg2.connect(conn_string)
	print("Connected!\n") 
	# conn.cursor will return a cursor object, you can use this cursor to perform queries
	cursor = conn.cursor()
	cursor.execute("""
        SELECT *
        FROM my_table
        WHERE some_requirement > 21
        """)

    # CONVERT QUERY INTO DATAFRAME FOR PYTHON ANALYSIS!
    rows = cursor.fetchall()
    
    dataFrmae = pd.DataFrame(rows, columns = list(zip(*cursor.description))[0])
    ######################
    # ANALYSIS GOES HERE #
    # OR YOU CAN CREATE  #
    # ANOTHER FUNCTION   #
    # TO DO WHATEVER     #
    # ANALYSIS MAKES     #
    # YOUR HEART HAPPY   #
    ######################
    
if __name__ == "__main__":
    main()