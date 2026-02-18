# BillPayPage.py
"""
PageClass for Bill Pay Page.
QA Notes:
- Locators are grouped (form, confirmation).
- Methods are granular for each form field.
- Confirmation methods validate details.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class BillPayPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        # Form fields
        self.payee_name = driver.find_element(By.NAME, "payee.name")
        self.address = driver.find_element(By.NAME, "payee.address.street")
        self.city = driver.find_element(By.NAME, "payee.address.city")
        self.state = driver.find_element(By.NAME, "payee.address.state")
        self.zip_code = driver.find_element(By.NAME, "payee.zipCode")
        self.phone_number = driver.find_element(By.NAME, "payee.phoneNumber")
        self.account_number = driver.find_element(By.NAME, "payee.accountNumber")
        self.verify_account_number = driver.find_element(By.NAME, "verifyAccount")
        self.amount = driver.find_element(By.NAME, "amount")
        self.from_account_id = driver.find_element(By.NAME, "fromAccountId")
        self.send_payment_button = driver.find_element(By.CSS_SELECTOR, "input[value='Send Payment']")
        # Confirmation
        self.success_message = driver.find_element(By.ID, "billpayResult")
        self.conf_payee_name = driver.find_element(By.ID, "payeeName")
        self.conf_amount = driver.find_element(By.ID, "amount")
        self.conf_from_account = driver.find_element(By.ID, "fromAccountId")

    def fill_payee_details(self, name, address, city, state, zip_code, phone, account_number, verify_account):
        self.payee_name.clear(); self.payee_name.send_keys(name)
        self.address.clear(); self.address.send_keys(address)
        self.city.clear(); self.city.send_keys(city)
        self.state.clear(); self.state.send_keys(state)
        self.zip_code.clear(); self.zip_code.send_keys(zip_code)
        self.phone_number.clear(); self.phone_number.send_keys(phone)
        self.account_number.clear(); self.account_number.send_keys(account_number)
        self.verify_account_number.clear(); self.verify_account_number.send_keys(verify_account)

    def enter_amount(self, amount):
        self.amount.clear(); self.amount.send_keys(str(amount))

    def select_from_account(self, account_id):
        self.from_account_id.send_keys(account_id)

    def click_send_payment(self):
        self.send_payment_button.click()

    def is_success_message_displayed(self):
        return self.success_message.is_displayed()

    def get_confirmation_details(self):
        return {
            "payee_name": self.conf_payee_name.text,
            "amount": self.conf_amount.text,
            "from_account": self.conf_from_account.text
        }
