from Create_tables import check_creation
from Query import sql_to_df

password = input('Enter password for database connection')
database = input('Enter SQL database name')

# Function used to check if tables where uploaded to database, and create them otherwise
check_creation()

# Function used to check if sql files where turned to dataframe, and turn them otherwise
sql_to_df()
