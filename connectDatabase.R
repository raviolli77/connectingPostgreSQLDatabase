require(dplyr)
require(DBI)
require(RPostgreSQL)
require(data.table)


databaseConnection <- readr::read_file('database.ini')
host <- strsplit(databaseConnection, '\r\n') # SPLIT THE ini FILE AT EVERY NEW LINE
# NOTE: THIS WORKS FOR WINDOWS MACHINES \n WILL BE APPLICABLE TO OTHER OS!
host <- unlist(host) # PRODUCE A VECTOR FROM THE PREVIOUS STRUCTURE
host <- gsub(".*: ", "", host) # REGULAR EXPRESSIONS TO GET RID OF STUFF THAT'S USEFUL IN PYTHON WHEN DOING ODBC

con <- dbConnect(RPostgres::Postgres(),
                 host = host[2],
                 dbname = host[3],
                 user = host[4],
                 port = host[5],
                 password = host[6])

# NOW THAT WE'RE CONNECTED LET'S DO A QUERY AND DO DATA ANALYSIS

rows = dbSendQuery(con, 'SELECT * FROM my_table WHERE some_requirement > 21')

dataTable <- data.table(rows)

# USE THIS COMMAND IF YOU WANT TO CREATE A NEW QUERY USING THE SAME NAME 
dbClearResult(rows)

# CLOSE CONNECTION
dbDisconnect(con)
