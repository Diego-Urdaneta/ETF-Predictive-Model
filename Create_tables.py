from sqlalchemy import create_engine, text
import pandas as pd
import os


def check_creation():
    csv_dir = input('Input CSV file location')
    # Connecting to database
    engine = create_engine(f'mysql://root:{password}@127.0.0.1:3306/{database}')
    connection = engine.connect()
    for filename in os.listdir(csv_dir):
        # Checking if tables exist
        print(f'{filename}...')
        cursor = connection.execute(text("SELECT COUNT(*) FROM information_schema.tables WHERE "
                                         f"table_schema = '{database}' AND table_name = '{filename[0:-4]}';"))
        existence_val = cursor.first()[0]
        if existence_val == 0:
            # Converting CSV to dataframe
            tables_df = pd.read_csv(f"{csv_dir}{filename}")
            # Converting dataframe to SQL
            tables_df.to_sql(name=filename[0:-4], con=engine)
        if existence_val == 1:
            print(f'{filename} does exist')
            return
