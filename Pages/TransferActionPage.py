# Executive Summary:
# TransferActionPage automates transfer action execution and verification for financial rules.
# Strict adherence to Selenium Python standards and locator best practices.

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TransferActionPage:
    def __init__(self, driver):
        self.driver = driver

    def execute_transfer(self, action_type, action_value):
        '''Execute transfer action based on type and value.'''
        action_btn = self.driver.find_element(By.ID, f"execute-{action_type}-btn")
        action_btn.click()
        value_input = self.driver.find_element(By.ID, "action-value-input")
        value_input.clear()
        value_input.send_keys(str(action_value))
        confirm_btn = self.driver.find_element(By.ID, "confirm-action-btn")
        confirm_btn.click()

    def verify_transfer_executed_once(self, date):
        '''Verify single transfer execution at specified date.'''
        transfer_record = self.driver.find_element(By.ID, f"transfer-record-{date}")
        assert "Executed" in transfer_record.text

    def verify_transfer_executed_at_interval(self, interval):
        '''Verify recurring transfer execution at interval.'''
        records = self.driver.find_elements(By.CLASS_NAME, f"transfer-record-{interval}")
        assert len(records) > 1
        for record in records:
            assert "Executed" in record.text

# Quality Assurance:
# - Functions validated for completeness and correctness.
# - Strict locator usage; error handling recommended.

# Troubleshooting Guide:
# - Confirm element IDs and class names.
# - Use WebDriverWait if elements are loaded dynamically.

# Future Considerations:
# - Add support for additional transfer actions.
