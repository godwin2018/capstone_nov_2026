import csv
import inspect
from common_utilities.utilities import ValidationUtility, BaseUtility, SchemaValidationUtility
from test_configuration.etlconfig import *
import logging
import pytest


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
class TestSchemaValidation:
    validation_utility = ValidationUtility()
    schema_validation = SchemaValidationUtility()

    #@pytest.mark.skip
    def test_schema_validation_for_fact_table_column_names_check(self,connect_postgress_database):
      test_case_name = inspect.currentframe().f_code.co_name # this code get the name of the current test case i.e. test_data_extraction_sales_file_stag
      logger.info(f"Starting test: {test_case_name}")
      try:
          expected_column_names = ['sale_id','product_id','store_id','quantity','total_sales','sale_date']


          logger.info(f"successfully competed test: {test_case_name}")
      except Exception as e:
          logger.error(f"test case failed {test_case_name}:{e}")
          pytest.fail()


    def test_schema_validation_for_inventory_level_by_(self,connect_postgress_database):


    def test_