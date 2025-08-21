import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import glob
import os
from src.logger import logging
logging.info('Initaiting the engin t oconnect to our database')
engine = create_engine('mysql+mysqlconnector://root:korty@127.0.0.1:3306/DATA_Korty')


def data_ingestion(df, table_name, engine):
    try:
        logging.info('Data Ingestion Script')
        logging.info('Adding to database')
        df.to_sql(table_name, engine , if_exists= 'replace', index= False)
    except Exception as e:
        print(e)
for file in os.listdir('../Data/fixed_data/'):
    logging.info('Check for all files with .csv extention')
    if '.csv' in file:
        try:
            logging.info('Loading the dataset from the directory')
            df = pd.read_csv('../Data/fixed_data/'+file)
            print(df.shape)
            data_ingestion(df, file[:-4], engine)
            print(f'Ingestion Completed of file {file}')
        except Exception as e:
            print(e)