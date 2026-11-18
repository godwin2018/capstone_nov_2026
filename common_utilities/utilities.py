from io import StringIO

import boto3
import pandas as pd
import paramiko
import os

import pytest
from sqlalchemy.testing.suite import test_results

from  common_utilities.db_connect import *
#from core_scripts.etl_extraction import *
from common_utilities.db_connect import *
import logging

from conftest import connect_postgress_database
from test_configuration.etlconfig import *

logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\utilities.log',
    #filename='../logs/utilities.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)


class BaseUtility:
    # encapsulation is used here
    def __read_file(self, file_path,file_type):
        if file_type == 'csv':
            df = pd.read_csv(file_path)
            logger.info(f'CSV read from file: {file_path}')
        elif file_type == 'json':
            df = pd.read_json(file_path)
            logger.info(f'JSON read from file: {file_path}')
        elif file_type == 'xml':
            df = pd.read_xml(file_path, xpath='.//item')
            logger.info(f'xml read from file: {file_path}')
        else:
            raise ValueError(f'unsupported file type passed: {file_type}')
            logger.info(f'Failed to read from file: {file_path}')
        return df

    # Abstraction is used here
    def read_file(self,file_path, file_type):
        return self.__read_file(file_path, file_type)

    def read_file_from_s3(self, bucket_name, file_key):
        try:
            logger.info("Reading file from S3 bucket")
            s3 = boto3.client('s3')
            response = s3.get_object(Bucket=bucket_name, Key=file_key)
            csv_content = response['Body'].read().decode('utf-8')
            data = StringIO(csv_content)
            df = pd.read_csv(data)
            logger.info(f"S3 data is {df}")
            return df
        except Exception as e:
            logger.error(f"S3 file read failed{e}")

    def linux_utility_download_file_from_linux_server(selfslf):
        try:
            logger.info("File download from linux server has started....")
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            ssh_client.connect(LINUX_HOSTNAME, username=LINUX_USERNAME, password=LINUX_PASSWORD)
            sftp = ssh_client.open_sftp()
            sftp.get(REMOTE_FILE_PATH, LOCAL_FILE_PATH)
            sftp.close()
            logger.info("File download from linux server has completed....")

        except Exception as e:
            logger.error(f'test file download failed from Linux')
            pytest.fail()

# we are using inheritance here
class ValidationUtility(BaseUtility):

    def execute_validation(self, validation_type=None, test_case_name=None, file_path=None, file_type=None, query_actual=None,dbconn_actual=None,query_expected=None,dbconn_expected=None,bucket_name=None, file_key=None):

            if validation_type == 'FILE_TO_DB':
                self.file_db(test_case_name,file_path,file_type,query_actual,dbconn_actual)
            elif validation_type == "DB_TO_DB":
                self.db_to_db(test_case_name, query_expected, dbconn_expected, query_actual, dbconn_actual)
            elif validation_type == "S3_TO_DB":
                self.s3_to_db(test_case_name, bucket_name, file_key, query_actual, dbconn_actual)


    def file_db(self,test_case_name,file_path,file_type,query_actual,dbconn_actual):
        try:
            df_expected = self.read_file(file_path, file_type)
            logger.info(f'expected data: {df_expected}')
            df_actual = pd.read_sql(query_actual,dbconn_actual)
            logger.info(f'actual data: {df_actual}')
            # expected minus actual
            df_extra_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences/", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(f"differences_extra_in_expected_{test_case_name}.csv", index=False)

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(f"differences_extra_in_actual_{test_case_name}.csv", index=False)
            # Assertion
            assert df_actual.equals(df_expected), f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")

        except Exception as e:
            logger.error(f"{test_case_name} validation failed {e}")
            pytest.fail()

    def db_to_db(self,test_case_name, query_expected, dbconn_expected, query_actual, dbconn_actual):
        try:
            df_expected = pd.read_sql(query_expected, dbconn_expected)
            logger.info(f"expected data :{df_expected}")
            df_actual = pd.read_sql(query_actual, dbconn_actual)
            logger.info(f'actual data: {df_actual}')
            # expected minus actual
            df_extra_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(f"differences_extra_in_expected_{test_case_name}.csv", index=False)

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(f"differences_extra_in_actual_{test_case_name}.csv", index=False)
            # Assertion
            assert df_actual.equals(df_expected), f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")

        except Exception as e:
            logger.error(f"{test_case_name} validation failed {e}")
            pytest.fail()


    def s3_to_db(self, test_case_name, bucket_name, file_key, query_actual, dbconn_actual):
        try:
            df_expected = self.read_file_from_s3(bucket_name, file_key)
            logger.info(f"expected data :{df_expected}")
            df_actual = pd.read_sql(query_actual, dbconn_actual)
            logger.info(f"actual data :{df_actual}")
            # expected minus actual
            df_extra_expected = df_expected[~df_expected.apply(tuple, axis=1).isin(df_actual.apply(tuple, axis=1))]

            # actual minus expected
            df_extra_actual = df_actual[~df_actual.apply(tuple, axis=1).isin(df_expected.apply(tuple, axis=1))]

            if not df_extra_expected.empty or not df_extra_actual.empty:
                os.makedirs("differences", exist_ok=True)

                if not df_extra_expected.empty:
                    df_extra_expected.to_csv(f"differences_{test_case_name}.csv", index=False)

                if not df_extra_actual.empty:
                    df_extra_actual.to_csv(f"differences_{test_case_name}.csv", index=False)
            # Assertion
            assert df_actual.equals(df_expected), f"{test_case_name} failed"
            logger.info(f"{test_case_name} passed")

        except Exception as e:
            logger.error(f"{test_case_name} validation failed {e}")
            pytest.fail()


class FileUtility(BaseUtility):
    def check_file_exists(self,file_path):
        try:
            return os.path.isfile(file_path)
        except Exception as e:
            logger.info(f'{file_path}, does not exist - file existence failed {e}')

    def check_file_size(self,file_path):
        try:
            return os.path.getsize(file_path)>0
        except Exception as e:
            logger.info(f'{file_path}, size is zero - This is a zero file size {e}')

class DataQuality(BaseUtility):
    # Check duplicate functions
    def check_duplicate_in_file(self,file_path, file_type):
        try:
            df = self.read_file(file_path, file_type)
            if df.duplicated().any():
                return False
            return True
        except Exception as e:
            logger.info(f'Duplicate check failed {e}')


    def check_duplicate_in_database(self,query, db_conn):
        try:
            #db_conn = connect_postgress_database()
            logger.info(f"checking duplicat in DB started")
            df = pd.read_sql(query, db_conn)
            if df.duplicated().any():
                return False
            return True
        except Exception as e:
            logger.info(f'Duplicate check failed {e}')


    def check_duplicate_for_specific_column_in_file(self, file_path, file_type, column_name):
                try:
                    df = self.read_file(file_path, file_type)
                    if df[column_name].duplicated().any():
                        return False
                    return True
                except Exception as e:
                    logger.error(f"Duplicate check for column {column_name}failed {e}")

    def check_duplicate_for_specific_column_in_database(self, query, db_conn, column_name):
        try:
            df = pd.read_sql(query, db_conn)
            if df[column_name].duplicated().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Duplicate check for column {column_name}failed {e}")


    # Null checks functions
    def check_null_value_in_file(self, file_path, file_type):
        try:
            df = self.read_file(file_path, file_type)
            if df.isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Null check failed {e}")

    def check_null_value_for_a_specific_column_in_file(self, file_path, file_type, column_name):
        try:
            df = self.read_file(file_path, file_type)
            if df[column_name].isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Null check failed {e}")


    def check_null_value_in_database(self, query, db_conn):
        try:
            df = pd.read_sql(query, db_conn)
            if df.isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Null check failed {e}")


    def check_null_value_for_a_specific_colum_in_database(self, query, db_conn, column_name):
        try:
            df = pd.read_sql(query, db_conn)
            if df[column_name].isnull().values().any():
                return False
            return True
        except Exception as e:
            logger.error(f"Null check failed {e}")


class SchemaValidationUtility(BaseUtility):
    def validate_column_names(self,db_conn,table_name,expected_column_names):
        query = f"select * from {table_name} where {expected_column_names}"
        df = pd.read_sql(query, db_conn)
        actual_column_name = list(df.columns)
        assert actual_column_name == expected_column_names, (f"{table_name} validation failed "
                                                            f"\n on {expected_column_names} column mismatch")

    def validate_column_datatypes(self,db_conn,table_name,expected_datatypes_dict):
        query = f"select * from {table_name}"
        df = pd.read_sql(query, db_conn)
        for column_name,expected_datatype in expected_datatypes_dict.items():
            actual_data_type = df[column_name].dtypes
            assert actual_data_type in expected_datatype, (f" data type mismatch in {table_name} "
                                                           f"\n for ismatch in column {column_name}"
                                                           f"\n expect column is {expected_datatypes_dict}"
                                                           f"\n actual column is {actual_data_type}")

    def validate_referential_interity_check(self, primary_db_conn, foreign_db_conn, primary_query, foreign_query,
                                            key_column_name, cv_path):
        foreign_df = pd.read_sql(foreign_query, foreign_db_conn)
        primary_df = pd.read_sql(primary_query, primary_db_conn)
        df_not_matched = foreign_df[~foreign_df[key_column_name].isin(primary_df[key_column_name])]
        if not df_not_matched.empty:
            df_not_matched.to_csv(cv_path, index=False)
        return df_not_matched