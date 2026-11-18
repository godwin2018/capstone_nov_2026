import inspect

import oracledb
import  pandas as pd
from test_configuration.etlconfig import *
from sqlalchemy import create_engine,text
import logging
import pytest



logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\conftest.log',
    #filename='/logs/conftest.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

@pytest.fixture()
def connect_postgress_database():
    logger.info("postgress databse connection is being established..")
    pggress_conn = create_engine(
        f'postgresql+psycopg://{PGRESS_USER}:{PGRESS_PASSWORD}@{PGRESS_HOST}:{PGRESS_PORT}/{PGRESS_DATABASE}')
    logger.info(pggress_conn)
    yield pggress_conn
    #pggress_conn.close()
    logger.info("postgress databse connection is been terminated..")


@pytest.fixture()
def connect_oracle_database():
    logger.info("oracle databse connection is being established..")
    oracle_conn = create_engine(
        f'oracle+oracledb://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE}')
    oracledb.init_oracle_client(lib_dir='C:\\Users\\USER\\Downloads\\instantclient-basic\\instantclient_23_26')
    logger.info(oracle_conn)
    yield oracle_conn
    logger.info("oracle databse connection is been terminated..")

