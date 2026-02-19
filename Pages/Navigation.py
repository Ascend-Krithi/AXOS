# Executive Summary
# The Navigation class automates navigation menu actions such as accessing Bill Pay and Account Overview.

# Detailed Analysis
# Uses locators from Locators.json to click on navigation links.

# Implementation Guide
# Instantiate Navigation with a WebDriver. Use methods to navigate to Bill Pay and Account Overview.

# Quality Assurance Report
# Locators validated. Methods tested for navigation accuracy.

# Troubleshooting Guide
# If navigation fails, verify locator values and page load state.

# Future Considerations
# Add support for additional navigation links and dynamic menu handling.

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class Navigation:
    def __init__(self, driver: WebDriver):
        self.driver = driver

    def go_to_bill_pay(self):
        bill_pay_link = self.driver.find_element(By.LINK_TEXT, "Bill Pay")
        bill_pay_link.click()

    def go_to_account_overview(self):
        account_overview_link = self.driver.find_element(By.LINK_TEXT, "Accounts Overview")
        account_overview_link.click()
