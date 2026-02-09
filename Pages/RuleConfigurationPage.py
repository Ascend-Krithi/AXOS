# RuleConfigurationPage.py
"""
Selenium Page Object for Rule Configuration Page.
Generated for test cases TC_SCRUM158_01 and TC_SCRUM158_02.
Adheres to AXOS coding standards and Selenium Python best practices.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        # Example locators from Locators.json
        # Replace '...' with actual locator values
        self.rule_name_input = driver.find_element(By.ID, 'rule-name-input')
        self.save_button = driver.find_element(By.XPATH, '//button[@id="save-rule"]')
        self.cancel_button = driver.find_element(By.XPATH, '//button[@id="cancel-rule"]')
        # Add more locators as per Locators.json

    def enter_rule_name(self, rule_name):
        """Enter rule name in the input field."""
        self.rule_name_input.clear()
        self.rule_name_input.send_keys(rule_name)

    def click_save(self):
        """Click the save button to save the rule configuration."""
        self.save_button.click()

    def click_cancel(self):
        """Click the cancel button to discard changes."""
        self.cancel_button.click()

    def wait_for_rule_configuration_page(self, timeout=10):
        """Wait for Rule Configuration Page to load."""
        WebDriverWait(self.driver, timeout).until(
            EC.visibility_of(self.rule_name_input)
        )

    # Add more methods based on test steps and Locators.json
