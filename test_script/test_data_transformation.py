import csv
import inspect
from common_utilities.utilities import ValidationUtility, BaseUtility
from test_configuration.etlconfig import *
import logging
import pytest


# Logging functionality

logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\test_etltransfomation.log',
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
class TestDatatransformation:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    #@pytest.mark.skip
    def test_data_transformation_filtered_sale_data(self,connect_postgress_database):
      test_case_name = inspect.currentframe().f_code.co_name # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
      logger.info(f"Starting test: {test_case_name}")
      try:
          #query_expected = """select * from staging_sales where sale_date > '2026-09-10'"""
          query_expected = """select sales_id,product_id,store_id,quantity,price,sale_date,region from staging_sales  where sale_date > '2026-09-10'"""
          query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from filtered_sale"""
          self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                     test_case_name=test_case_name,
                                                     query_expected=query_expected,
                                                     dbconn_expected=connect_postgress_database,
                                                     query_actual=query_actual,
                                                     dbconn_actual=connect_postgress_database)
          logger.info(f"successfully competed test: {test_case_name}")
      except Exception as e:
          logger.error(f"test case failed {test_case_name}:{e}")
          pytest.fail()

    #@pytest.mark.skip(reason="not needed at the moment")
    def test_data_transformation_for_router_high_sales_data(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:

            query_expected = """select * from filtered_sale where region = 'High'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from high_sale"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_postgress_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    #@pytest.mark.skip(reason="not needed at the moment")
    def test_data_transformation_for_router_low_sales_data(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:
            # query_expected = """select * from staging_sales where sale_date > '2026-09-10'"""
            query_expected = """select * from filtered_sale where region = 'Low'"""
            query_actual = """select sales_id,product_id,store_id,quantity,price,sale_date,region from low_sale"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_postgress_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    #@pytest.mark.skip(reason="not needed at the moment")
    def test_data_transformation_for_aggregator_sales(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:
            # query_expected = """select * from staging_sales where sale_date > '2026-09-10'"""
            query_expected = """select product_id, sale_date, sum(quantity*price) from filtered_sale group by product_id, sale_date"""
            query_actual = """select product_id,sale_date,sum from monthly_sales_summary_source"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_postgress_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    #@pytest.mark.skip(reason="not needed at the moment")
    def test_data_transformation_for_joiner(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:
            # query_expected = """select * from staging_sales where sale_date > '2026-09-10'"""
            query_expected = """select fs.sales_id,fs.product_id,fs.quantity, fs.price,fs.quantity*fs.price as sales_amount,fs.sale_date,p.product_name,s.store_id,s.store_name 
        from filtered_sale as fs inner join stag_product as p on fs.product_id=p.product_id inner join staging_stores as s on fs.store_id=s.store_id"""
            query_actual = """select sales_id,product_id,quantity,price,sales_amount,sale_date,product_name,store_id,store_name from sales_with_details"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_postgress_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()

    #@pytest.mark.skip(reason="not needed at the moment")
    def test_data_transformation_aggregator_inventory(self, connect_postgress_database):
        test_case_name = inspect.currentframe().f_code.co_name  # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
        logger.info(f"Starting test: {test_case_name}")
        try:
            # query_expected = """select * from staging_sales where sale_date > '2026-09-10'"""
            query_expected = """select store_id, sum(quantity_on_hand) as total_inventory from stag_inventory group by store_id"""
            query_actual = """select store_id,total_inventory from agg_inventory_level"""
            self.validation_utility.execute_validation(validation_type="DB_TO_DB",
                                                       test_case_name=test_case_name,
                                                       query_expected=query_expected,
                                                       dbconn_expected=connect_postgress_database,
                                                       query_actual=query_actual,
                                                       dbconn_actual=connect_postgress_database)
            logger.info(f"successfully competed test: {test_case_name}")
        except Exception as e:
            logger.error(f"test case failed {test_case_name}:{e}")
            pytest.fail()