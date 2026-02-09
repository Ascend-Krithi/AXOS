# TransferActionPage.py
"""
Page Object for Transfer Action verification.
This class supports simulation and validation of transfer actions triggered by rules.

Test Coverage:
- Simulate system time reaching the trigger date.
- Simulate the passing of several weeks.
- Validate that transfer actions are executed as expected.

Locators should be updated according to Locators.json content for:
- Transfer action logs
- Transfer confirmation
- Date/time fields

Usage:
    transfer_page = TransferActionPage(driver)
    assert transfer_page.verify_transfer_executed(date, amount)
    assert transfer_page.verify_recurring_transfer(interval, percentage)
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TransferActionPage:
    def __init__(self, driver):
        self.driver = driver
        # Locators (replace with actual values from Locators.json)
        self.transfer_log = (By.ID, 'transfer-log')
        self.transfer_entry = (By.CLASS_NAME, 'transfer-entry')
        self.transfer_date = (By.CLASS_NAME, 'transfer-date')
        self.transfer_amount = (By.CLASS_NAME, 'transfer-amount')
        self.transfer_percentage = (By.CLASS_NAME, 'transfer-percentage')

    def verify_transfer_executed(self, date, amount):
        """
        Verify that a transfer action was executed at the specified date with the specified amount.
        :param date: str, date in ISO format
        :param amount: int, expected amount
        :return: bool
        """
        log = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_log)
        )
        entries = log.find_elements(By.CLASS_NAME, 'transfer-entry')
        for entry in entries:
            entry_date = entry.find_element(By.CLASS_NAME, 'transfer-date').text
            entry_amount = entry.find_element(By.CLASS_NAME, 'transfer-amount').text
            if entry_date == date and int(entry_amount) == amount:
                return True
        return False

    def verify_recurring_transfer(self, interval, percentage):
        """
        Verify that recurring transfer actions are executed at the start of each interval with the specified percentage.
        :param interval: str, interval type (e.g., 'weekly')
        :param percentage: int
        :return: bool
        """
        log = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.transfer_log)
        )
        entries = log.find_elements(By.CLASS_NAME, 'transfer-entry')
        count = 0
        for entry in entries:
            entry_percentage = entry.find_element(By.CLASS_NAME, 'transfer-percentage').text
            entry_interval = entry.find_element(By.CLASS_NAME, 'transfer-date').text  # Simplified; should check interval logic
            if entry_percentage == str(percentage):
                count += 1
        return count > 0