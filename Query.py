from sqlalchemy import create_engine
import pandas as pd
import os.path


def sql_to_df():
    # Checking if pkl file in directory
    pkl_filepath = input('Enter filepath for pkl')
    if os.path.isfile(pkl_filepath):
        pass
    else:
        # Function to facilitate neatness of creating query
        def sql_cols(columns, separator, last_separator):
            concatenator = ""
            for value in columns:
                if columns[columns.index(value)] != columns[-1]:
                    concatenator = concatenator + value + separator
                if columns[columns.index(value)] == columns[-1]:
                    concatenator = concatenator + value + last_separator
            return concatenator

        # Creating query

        subquery_a = f"Select ep.index, f.Ticker, f.AvgVol  " \
                     "FROM (SELECT ep.fund_symbol as 'Ticker' , AVG(ep.volume) As 'AvgVol' " \
                     "FROM `ETF prices` AS ep " \
                     "GROUP BY ep.fund_symbol " \
                     "HAVING AVG(ep.volume) > 10000) AS f " \
                     "JOIN `ETF prices` ep ON ep.fund_symbol = f.Ticker "

        cols = "ep.index, ep.open, ep.fund_symbol, ep.volume, e.fund_alpha_3years, e.fund_beta_3years, " \
               "e.fund_r_squared_3years, e.fund_stdev_3years, e.fund_sharpe_ratio_3years, " \
               "e.fund_treynor_ratio_3years"

        subquery_b = f"SELECT {cols} " \
                     f"FROM ETFs AS e " \
                     f"JOIN `ETF prices` AS ep " \
                     f"ON ep.fund_symbol = e.fund_symbol " \
                     f"WHERE {sql_cols(cols.split(','), ' IS NOT NULL AND', ' IS NOT NULL')}"

        query = F"SELECT b.*, a.AvgVol " \
                F"FROM ({subquery_a}) as a " \
                F"JOIN ({subquery_b}) as b " \
                F"ON a.index = b.index"

        # Connecting to database
        engine = create_engine(f'mysql://root:{password}@127.0.0.1:3306/{database}')
        connection = engine.connect()
        # Converting SQL to dataframe
        df_sql = pd.read_sql(query, connection)
        connection.close()
        # Converting dataframe to pkl
        df_sql.to_pickle(f'{pkl_filepath}')
        # pkl facilitates accessing dataframes in the future very quickly
