# Navigation.py
"""
PageClass for Navigation elements (menu links).
QA Notes:
- Only navigation locators from Locators.json are used.
- Methods are strictly for navigation actions.
- No state mutation.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class Navigation:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.bill_pay_link = driver.find_element(By.LINK_TEXT, "Bill Pay")
        self.account_overview_link = driver.find_element(By.LINK_TEXT, "Accounts Overview")

    def click_bill_pay(self):
        self.bill_pay_link.click()

    def click_account_overview(self):
        self.account_overview_link.click()
