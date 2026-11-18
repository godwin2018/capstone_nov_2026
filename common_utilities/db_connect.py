from sqlalchemy import create_engine
import oracledb
from test_configuration.etlconfig import *
import logging


logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\dbconnection.log',
    #filename='../logs/dbconnection.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)



def connect_to_oracle(self):
    oracle_conn = create_engine(f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}')
    oracledb.init_oracle_client(lib_dir='C:\\Users\\USER\\Downloads\\instantclient-basic\\instantclient_23_26')
    logger.info(oracle_conn)

def connect_to_postgress(self):
    pggress_conn = create_engine(f'postgresql+psycopg://{PGRESS_USER}:{PGRESS_PASSWORD}@{PGRESS_HOST}:{PGRESS_PORT}/{PGRESS_DATABASE}')
    logger.info(pggress_conn)



''''class DatabaseConnection:
    #def __init__(self):
    def connect_to_oracle(self):
        oracle_conn = create_engine(f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}')
        oracledb.init_oracle_client(lib_dir='C:\\Users\\USER\\Downloads\\instantclient-basic\\instantclient_23_26')
        print(oracle_conn)

    def connect_to_postgress(self):
        pggress_conn = create_engine(f'postgresql+psycopg://{PGRESS_USER}:{PGRESS_PASSWORD}@{PGRESS_HOST}:{PGRESS_PORT}/{PGRESS_DATABASE}')
        print(pggress_conn)'''