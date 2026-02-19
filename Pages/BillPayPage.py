# imports
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class BillPayPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Form locators
        self.payee_name = (By.NAME, "payee.name")
        self.address = (By.NAME, "payee.address.street")
        self.city = (By.NAME, "payee.address.city")
        self.state = (By.NAME, "payee.address.state")
        self.zip_code = (By.NAME, "payee.address.zipCode")
        self.phone_number = (By.NAME, "payee.phoneNumber")
        self.account_number = (By.NAME, "payee.accountNumber")
        self.verify_account_number = (By.NAME, "verifyAccount")
        self.amount = (By.NAME, "amount")
        self.from_account_id = (By.NAME, "fromAccountId")
        self.send_payment_button = (By.CSS_SELECTOR, "input[value='Send Payment']")
        # Confirmation locators
        self.success_message = (By.ID, "billpayResult")
        self.conf_payee_name = (By.ID, "payeeName")
        self.conf_amount = (By.ID, "amount")
        self.conf_from_account = (By.ID, "fromAccountId")

    def fill_payee_details(self, details: dict):
        self.driver.find_element(*self.payee_name).clear()
        self.driver.find_element(*self.payee_name).send_keys(details["payee_name"])
        self.driver.find_element(*self.address).clear()
        self.driver.find_element(*self.address).send_keys(details["address"])
        self.driver.find_element(*self.city).clear()
        self.driver.find_element(*self.city).send_keys(details["city"])
        self.driver.find_element(*self.state).clear()
        self.driver.find_element(*self.state).send_keys(details["state"])
        self.driver.find_element(*self.zip_code).clear()
        self.driver.find_element(*self.zip_code).send_keys(details["zip_code"])
        self.driver.find_element(*self.phone_number).clear()
        self.driver.find_element(*self.phone_number).send_keys(details["phone_number"])
        self.driver.find_element(*self.account_number).clear()
        self.driver.find_element(*self.account_number).send_keys(details["account_number"])
        self.driver.find_element(*self.verify_account_number).clear()
        self.driver.find_element(*self.verify_account_number).send_keys(details["verify_account_number"])
        self.driver.find_element(*self.amount).clear()
        self.driver.find_element(*self.amount).send_keys(str(details["amount"]))
        self.driver.find_element(*self.from_account_id).clear()
        self.driver.find_element(*self.from_account_id).send_keys(str(details["from_account_id"]))

    def submit_payment(self):
        self.driver.find_element(*self.send_payment_button).click()

    def get_success_message(self):
        return self.driver.find_element(*self.success_message).text

    def get_confirmation_details(self):
        return {
            "payee_name": self.driver.find_element(*self.conf_payee_name).text,
            "amount": self.driver.find_element(*self.conf_amount).text,
            "from_account": self.driver.find_element(*self.conf_from_account).text
        }

    def pay_bill(self, details: dict):
        self.fill_payee_details(details)
        self.submit_payment()
        return self.get_confirmation_details()
