from selenium.webdriver.common.by import By

class Navigation:
    def __init__(self, driver):
        self.driver = driver
        self.bill_pay_link = driver.find_element(By.LINK_TEXT, 'Bill Pay')
        self.account_overview_link = driver.find_element(By.LINK_TEXT, 'Accounts Overview')

    def go_to_bill_pay(self):
        self.bill_pay_link.click()

    def go_to_account_overview(self):
        self.account_overview_link.click()
