from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

        # Locators from Locators.json
        self.locators = {
            "payeeName": (By.NAME, "payee.name"),
            "address": (By.NAME, "payee.address.street"),
            "city": (By.NAME, "payee.address.city"),
            "state": (By.NAME, "payee.address.state"),
            "zipCode": (By.NAME, "payee.address.zipCode"),
            "phoneNumber": (By.NAME, "payee.phoneNumber"),
            "accountNumber": (By.NAME, "payee.accountNumber"),
            "verifyAccountNumber": (By.NAME, "verifyAccount"),
            "amount": (By.NAME, "amount"),
            "fromAccountId": (By.NAME, "fromAccountId"),
            "sendPaymentButton": (By.CSS_SELECTOR, "input[value='Send Payment']"),
            "successMessage": (By.ID, "billpayResult"),
            "confPayeeName": (By.ID, "payeeName"),
            "confAmount": (By.ID, "amount"),
            "confFromAccount": (By.ID, "fromAccountId"),
            # Navigation
            "billPayLink": (By.LINK_TEXT, "Bill Pay")
        }

    def navigate_to_bill_pay(self):
        """Navigate to the Bill Pay page via navigation link."""
        bill_pay_link = WebDriverWait(self.driver, self.timeout).until(
            EC.element_to_be_clickable(self.locators["billPayLink"])
        )
        bill_pay_link.click()
        # Wait for the Bill Pay form to be visible
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators["payeeName"])
        )

    def fill_payee_information(self, payee_name, address, city, state, zip_code, phone_number):
        """Fill out payee information fields."""
        self.driver.find_element(*self.locators["payeeName"]).clear()
        self.driver.find_element(*self.locators["payeeName"]).send_keys(payee_name)
        self.driver.find_element(*self.locators["address"]).clear()
        self.driver.find_element(*self.locators["address"]).send_keys(address)
        self.driver.find_element(*self.locators["city"]).clear()
        self.driver.find_element(*self.locators["city"]).send_keys(city)
        self.driver.find_element(*self.locators["state"]).clear()
        self.driver.find_element(*self.locators["state"]).send_keys(state)
        self.driver.find_element(*self.locators["zipCode"]).clear()
        self.driver.find_element(*self.locators["zipCode"]).send_keys(zip_code)
        self.driver.find_element(*self.locators["phoneNumber"]).clear()
        self.driver.find_element(*self.locators["phoneNumber"]).send_keys(phone_number)

    def fill_account_information(self, account_number, verify_account_number):
        """Fill out account number and verify account number fields."""
        self.driver.find_element(*self.locators["accountNumber"]).clear()
        self.driver.find_element(*self.locators["accountNumber"]).send_keys(account_number)
        self.driver.find_element(*self.locators["verifyAccountNumber"]).clear()
        self.driver.find_element(*self.locators["verifyAccountNumber"]).send_keys(verify_account_number)

    def fill_payment_amount(self, amount):
        """Fill out the payment amount field."""
        self.driver.find_element(*self.locators["amount"]).clear()
        self.driver.find_element(*self.locators["amount"]).send_keys(str(amount))

    def select_from_account(self, account_id):
        """Select the source account from the dropdown."""
        select_elem = Select(self.driver.find_element(*self.locators["fromAccountId"]))
        select_elem.select_by_value(str(account_id))

    def submit_payment(self):
        """Click the Send Payment button to submit the form."""
        self.driver.find_element(*self.locators["sendPaymentButton"]).click()

    def is_bill_pay_page_displayed(self):
        """Verify that the Bill Pay page is displayed with all required fields."""
        try:
            WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(self.locators["payeeName"])
            )
            # Optionally check all fields
            for key in ["address", "city", "state", "zipCode", "phoneNumber", "accountNumber", "verifyAccountNumber", "amount", "fromAccountId"]:
                self.driver.find_element(*self.locators[key])
            return True
        except Exception:
            return False

    def verify_confirmation(self, expected_payee_name, expected_amount, expected_from_account):
        """Verify the confirmation page displays correct details after payment."""
        WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(self.locators["successMessage"])
        )
        payee_name = self.driver.find_element(*self.locators["confPayeeName"]).text.strip()
        amount = self.driver.find_element(*self.locators["confAmount"]).text.strip()
        from_account = self.driver.find_element(*self.locators["confFromAccount"]).text.strip()
        return (payee_name == expected_payee_name and
                amount == str(expected_amount) and
                from_account == str(expected_from_account))

    def get_success_message(self):
        """Return the success message displayed after payment."""
        return self.driver.find_element(*self.locators["successMessage"]).text.strip()
