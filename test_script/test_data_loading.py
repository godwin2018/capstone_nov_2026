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
class TestDataloading:
    validation_utility = ValidationUtility()
    base_utility = BaseUtility()

    #@pytest.mark.skip
    def test_data_loading_for_monthly_sales_summary(self,connect_postgress_database):
      test_case_name = inspect.currentframe().f_code.co_name # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
      logger.info(f"Starting test: {test_case_name}")
      try:
          query_expected = """select product_id,sale_date,total_sales from monthly_sales_summary"""
          query_actual = """select product_id,sale_date,total_sales from monthly_sales_summary_source"""
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