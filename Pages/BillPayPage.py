from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver):
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

    def fill_payee_details(self, payee_info):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.payee_name)).send_keys(payee_info["name"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.address)).send_keys(payee_info["address"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.city)).send_keys(payee_info["city"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.state)).send_keys(payee_info["state"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.zip_code)).send_keys(payee_info["zip"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.phone_number)).send_keys(payee_info["phone"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.account_number)).send_keys(payee_info["account"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.verify_account_number)).send_keys(payee_info["verify_account"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.amount)).send_keys(payee_info["amount"])
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.from_account_id)).send_keys(payee_info["from_account"])

    def submit_payment(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(self.send_payment_button)).click()

    def verify_confirmation(self, expected_payee, expected_amount, expected_account):
        success = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.success_message)).is_displayed()
        payee = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.conf_payee_name)).text
        amount = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.conf_amount)).text
        account = WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.conf_from_account)).text
        return success and payee == expected_payee and amount == expected_amount and account == expected_account
