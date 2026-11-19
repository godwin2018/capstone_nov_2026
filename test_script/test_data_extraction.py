import csv
import inspect
from common_utilities.utilities import ValidationUtility, BaseUtility
from test_configuration.etlconfig import *
import logging
import pytest
from _pytest.python import CallSpec2


# Logging functionality

logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\test_etlextraction.log',
    #filename='../logs/test_etlextraction.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    force=True,
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger = logging.getLogger(__name__)

# Create DB connection


sale_data_loc = 'C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\test_data\\sales_data.csv'
class TestDataExtraction:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    @pytest.mark.order(7)
    @pytest.mark.data_extraction
    @pytest.mark.regression
    @pytest.mark.skip
    def test_data_extraction_sales_file_stag(self,connect_postgress_database):
      test_case_name = inspect.currentframe().f_code.co_name # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
      logger.info(f"Starting test: {test_case_name}")
      try:
          query_actual = """select * from staging_sales"""
          self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                     test_case_name=test_case_name,
                                                     file_path="test_data/sales_data.csv",
                                                     file_type="csv",
                                                     query_actual=query_actual,
                                                     dbconn_actual=connect_postgress_database)
          logger.info(f"successfully competed test: {test_case_name}")
      except Exception as e:
          logger.error(f"test case failed {test_case_name}:{e}")
          pytest.fail()

    @pytest.mark.order(6)
    @pytest.mark.data_extraction
    @pytest.mark.regression
    @pytest.mark.skip
    def test_data_extraction_sales_s3_file_stag(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from staging_sales"""
            self.validation_utility.execute_validation(validation_type="S3_TO_DB",
                                                       test_case_name=test_case_name,
                                                       bucket_name=BUCKET_NAME,
                                                       file_path=FILE_KEY,
                                                       #file_type="csv",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    @pytest.mark.data_extraction
    @pytest.mark.smoke
    @pytest.mark.skip
    def test_data_extraction_inventory_file_stag(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from stag_inventory"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/inventory_data.xml",
                                                       file_type="xml",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    @pytest.mark.data_extraction
    @pytest.mark.regression
    @pytest.mark.smoke
    def test_data_extraction_product_file_stag(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from stag_product"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/product_data.csv",
                                                       file_type="csv",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    @pytest.mark.data_extraction
    @pytest.mark.regression
    @pytest.mark.smoke
    @pytest.mark.skip
    def test_data_extraction_product_linux_file_stag(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        self.base_utility.linux_utility_download_file_from_linux_server()
        # ABSTRACTION
        # download_file_from_linux_server()
        # Internal SSH/SFTP implementation
        # is hidden from test case
        try:
            query_actual = """select * from stag_product"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path=LOCAL_FILE_PATH,
                                                       file_type="csv",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    @pytest.mark.data_extraction
    @pytest.mark.regression
    #@pytest.mark.skip
    def test_data_extraction_supplier_file_stag(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_actual = """select * from stag_supplier"""
            self.validation_utility.execute_validation(validation_type="FILE_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/supplier_data.json",
                                                       file_type="json",
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"succesfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    @pytest.mark.data_extraction
    @pytest.mark.regression
    #@pytest.mark.skip
    def test_data_extraction_stores_db_stag(self, connect_postgress_database, connect_oracle_database):
        test_case_name = inspect.currentframe().f_code.co_name
        logger.info(f"Starting test: {test_case_name}")
        try:
            query_expected = """select * from stores"""
            query_actual = """select * from staging_stores"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       file_path="test_data/inventory_data.xml",
                                                       file_type="xml",
                                                       query_expected= query_expected,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database,
                                                       dbconn_expected=connect_oracle_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()



