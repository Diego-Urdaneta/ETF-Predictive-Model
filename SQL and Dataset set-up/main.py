from Create_tables import check_creation
from Query import sql_to_df
import kaggle

#To download files
kaggle_filepath = input('Input filepath of kaggle files')
kaggle.api.authenticate()
kaggle.api.dataset_download_files('stefanoleone992/mutual-funds-and-etfs', path=f'{kaggle_filepath}, unzip=True)

#Information for accessing database                              
password = input('Enter password for database connection')
database = input('Enter SQL database name')

# Function used to check if tables where uploaded to database, and create them otherwise
check_creation()

# Function used to check if sql files where turned to dataframe, and turn them otherwise
sql_to_df()
