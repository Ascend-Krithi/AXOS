from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Form Locators
    PAYEE_NAME = (By.NAME, "payee.name")
    ADDRESS = (By.NAME, "payee.address.street")
    CITY = (By.NAME, "payee.address.city")
    STATE = (By.NAME, "payee.address.state")
    ZIP_CODE = (By.NAME, "payee.address.zipCode")
    PHONE_NUMBER = (By.NAME, "payee.phoneNumber")
    ACCOUNT_NUMBER = (By.NAME, "payee.accountNumber")
    VERIFY_ACCOUNT_NUMBER = (By.NAME, "verifyAccount")
    AMOUNT = (By.NAME, "amount")
    FROM_ACCOUNT_ID = (By.NAME, "fromAccountId")
    SEND_PAYMENT_BUTTON = (By.CSS_SELECTOR, "input[value='Send Payment']")

    # Confirmation Locators
    SUCCESS_MESSAGE = (By.ID, "billpayResult")
    CONF_PAYEE_NAME = (By.ID, "payeeName")
    CONF_AMOUNT = (By.ID, "amount")
    CONF_FROM_ACCOUNT = (By.ID, "fromAccountId")

    def fill_payee_info(self, name: str, address: str, city: str, state: str, zip_code: str, phone: str, account: str, verify_account: str):
        self.wait.until(EC.visibility_of_element_located(self.PAYEE_NAME)).clear()
        self.driver.find_element(*self.PAYEE_NAME).send_keys(name)

        self.wait.until(EC.visibility_of_element_located(self.ADDRESS)).clear()
        self.driver.find_element(*self.ADDRESS).send_keys(address)

        self.wait.until(EC.visibility_of_element_located(self.CITY)).clear()
        self.driver.find_element(*self.CITY).send_keys(city)

        self.wait.until(EC.visibility_of_element_located(self.STATE)).clear()
        self.driver.find_element(*self.STATE).send_keys(state)

        self.wait.until(EC.visibility_of_element_located(self.ZIP_CODE)).clear()
        self.driver.find_element(*self.ZIP_CODE).send_keys(zip_code)

        self.wait.until(EC.visibility_of_element_located(self.PHONE_NUMBER)).clear()
        self.driver.find_element(*self.PHONE_NUMBER).send_keys(phone)

        self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_NUMBER)).clear()
        self.driver.find_element(*self.ACCOUNT_NUMBER).send_keys(account)

        self.wait.until(EC.visibility_of_element_located(self.VERIFY_ACCOUNT_NUMBER)).clear()
        self.driver.find_element(*self.VERIFY_ACCOUNT_NUMBER).send_keys(verify_account)

    def select_from_account(self, account_id: str):
        from_account_dropdown = self.wait.until(EC.visibility_of_element_located(self.FROM_ACCOUNT_ID))
        from_account_dropdown.clear()
        from_account_dropdown.send_keys(account_id)

    def enter_amount(self, amount: str):
        amount_field = self.wait.until(EC.visibility_of_element_located(self.AMOUNT))
        amount_field.clear()
        amount_field.send_keys(amount)

    def send_payment(self):
        send_btn = self.wait.until(EC.element_to_be_clickable(self.SEND_PAYMENT_BUTTON))
        send_btn.click()

    def get_confirmation_details(self):
        self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE))
        payee_name = self.driver.find_element(*self.CONF_PAYEE_NAME).text
        amount = self.driver.find_element(*self.CONF_AMOUNT).text
        from_account = self.driver.find_element(*self.CONF_FROM_ACCOUNT).text
        return {
            "payee_name": payee_name,
            "amount": amount,
            "from_account": from_account
        }

    def is_success_message_displayed(self):
        return self.wait.until(EC.visibility_of_element_located(self.SUCCESS_MESSAGE)).is_displayed()
