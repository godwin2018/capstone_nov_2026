import csv
import inspect
from common_utilities.utilities import ValidationUtility, BaseUtility, FileUtility, DataQuality
from test_configuration.etlconfig import *
import logging
import pytest


# Logging functionality

logging.basicConfig(
    filename='C:\\etlAutomation\\Capstone_Aug2026_Test_Automation\\logs\\test_etldata_quality.log',
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
class TestDataQuality:
    file_utility = FileUtility()
    data_quality_utility = DataQuality()

    logger.info('FILE EXISTENCE CHECK STARTS')

    @pytest.mark.data_quality
    def test_data_quality_file_existence_of_inventory_data_xml(self):

        try:
            logger.info(f'Inventory Data Quality Test Started')
            file_loc = 'test_data/inventory_data.xml'
            file_status = self.file_utility.check_file_exists(file_loc)
            assert file_status is True, f'Inventory data file doe not exist at {file_loc}'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_existence_for_product_data_csv(self):

        try:
            logger.info(f'Product File Existence Check Test Started')
            file_status = self.file_utility.check_file_exists('test_data/product_data.csv')
            assert file_status is True, 'Product data file does not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_existence_for_sales_data_csv(self):

        try:
            logger.info(f'Sales File Existence Check Test Started')
            file_status = self.file_utility.check_file_exists('test_data/sales_data.csv')
            assert file_status is True, 'Sales data bfile doe not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_existence_for_stores_data_csv(self):

        try:
            logger.info(f'Stores File Existence Check Test Started')
            file_status = self.file_utility.check_file_exists('test_data/stores.csv')
            assert file_status is True, 'Sales data bfile doe not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_existence_for_supplier_data_json(self):

        try:
            logger.info(f'Supplier File Existence CheckTest Started')
            file_status = self.file_utility.check_file_exists('test_data/supplier_data.json')
            assert file_status is True, 'Supplier data file does not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()
        logger.info('FILE EXISTENCE CHECK ENDS')
        logger.info('========file existence stopping and file size starting==================')

    @pytest.mark.data_quality
    def test_data_quality_file_size_for_inventory_data_xml(self):

        logger.info('FILE SIZE CHECK STARTS')
        try:
            logger.info(f'Inventory Data file size Test Started')
            file_status = self.file_utility.check_file_size('test_data/inventory_data.xml')
            #file_status = self.file_utility.check_file_size('test_data/test_file')
            assert file_status is True, 'Inventory data file size is empty'
        except Exception as e:
            logger.error(f"test case failed {e} because file size is empty!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_size_for_product_data_csv(self):

        try:
            logger.info(f'Product Data file size Test Started')
            file_status = self.file_utility.check_file_size('test_data/inventory_data.xml')
            assert file_status is True, 'Product data file is empty'
        except Exception as e:
            logger.error(f"test case failed {e} because file is empty!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_size_for_sales_data_csv(self):

        try:
            logger.info(f'Sales Data file size Test Started')
            file_status = self.file_utility.check_file_size('test_data/sales_data.csv')
            assert file_status is True, 'Sales data file does not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.data_quality
    def test_data_quality_file_size_for_stores_data_csv(self):

        try:
            logger.info(f'Stores Data file size Test Started')
            file_status = self.file_utility.check_file_size('test_data/stores.csv')
            assert file_status is True, 'Stores data bfile doe not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    @pytest.mark.order(4)
    @pytest.mark.data_quality
    def test_data_quality_file_size_for_supplier_data_json(self):

        try:
            logger.info(f'Supplier Data file size Test Started')
            file_status = self.file_utility.check_file_size('test_data/supplier_data.json')
            assert file_status is True, 'Supplier data bfile doe not exist'
        except Exception as e:
            logger.error(f"test case failed {e} because file does not exist!!!!")
            pytest.fail()

    logger.info('FILE SIZE CHECK ENDS')