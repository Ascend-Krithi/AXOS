# BillPayPage.py
"""
BillPayPage - Selenium Page Object for Bill Pay functionality

Executive Summary:
This PageClass automates the end-to-end Bill Pay workflow in Online Banking, covering navigation, form entry, payment submission, and confirmation, as described in test cases TC-BP-001 and TC-BP-002. All locators are sourced from Locators.json. The class is designed for robust test automation, strict code integrity, and seamless integration with downstream pipelines.

Detailed Analysis:
- Navigates to Bill Pay section using Navigation['billPayLink']
- Fills Payee Name, Address, City, State, Zip, Phone, Account Number, Verify Account Number, Amount, and selects Source Account
- Submits payment and verifies confirmation, including success message and transaction details
- Handles minimum payment amount, account selection, and field validations

Implementation Guide:
- Requires Selenium WebDriver and Python 3.7+
- Instantiate BillPayPage with a Selenium driver
- Use provided methods for each test step: navigation, field input, submission, and confirmation
- Each method returns verification result or raises AssertionError if validation fails

Quality Assurance Report:
- All actions and verifications are mapped directly from test cases and locators
- Input validation, confirmation checks, and error handling included
- Structured for maintainability and extensibility

Troubleshooting Guide:
- Ensure locators match current UI (update Locators.json as needed)
- WebDriver must be initialized and logged in before using BillPayPage
- Use explicit waits for dynamic elements
- Review logs for assertion errors or locator mismatches

Future Considerations:
- Extend for negative test cases (invalid inputs, insufficient funds)
- Parameterize for data-driven testing
- Integrate with reporting frameworks for enhanced visibility

"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        # Navigation locators
        self.bill_pay_link = (By.LINK_TEXT, "Bill Pay")
        # Bill Pay form locators
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

    def navigate_to_bill_pay(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.bill_pay_link)
        ).click()
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.payee_name)
        )
        # Verify Bill Pay page loaded
        return self.driver.find_element(*self.payee_name).is_displayed()

    def fill_payee_details(self, payee_name, address, city, state, zip_code, phone_number):
        self.driver.find_element(*self.payee_name).clear()
        self.driver.find_element(*self.payee_name).send_keys(payee_name)
        self.driver.find_element(*self.address).clear()
        self.driver.find_element(*self.address).send_keys(address)
        self.driver.find_element(*self.city).clear()
        self.driver.find_element(*self.city).send_keys(city)
        self.driver.find_element(*self.state).clear()
        self.driver.find_element(*self.state).send_keys(state)
        self.driver.find_element(*self.zip_code).clear()
        self.driver.find_element(*self.zip_code).send_keys(zip_code)
        self.driver.find_element(*self.phone_number).clear()
        self.driver.find_element(*self.phone_number).send_keys(phone_number)
        # Validate fields
        assert self.driver.find_element(*self.payee_name).get_attribute("value") == payee_name, "Payee name not set correctly"
        assert self.driver.find_element(*self.address).get_attribute("value") == address, "Address not set correctly"
        assert self.driver.find_element(*self.city).get_attribute("value") == city, "City not set correctly"
        assert self.driver.find_element(*self.state).get_attribute("value") == state, "State not set correctly"
        assert self.driver.find_element(*self.zip_code).get_attribute("value") == zip_code, "Zip code not set correctly"
        assert self.driver.find_element(*self.phone_number).get_attribute("value") == phone_number, "Phone not set correctly"

    def fill_account_details(self, account_number, verify_account_number):
        self.driver.find_element(*self.account_number).clear()
        self.driver.find_element(*self.account_number).send_keys(account_number)
        self.driver.find_element(*self.verify_account_number).clear()
        self.driver.find_element(*self.verify_account_number).send_keys(verify_account_number)
        # Validation
        assert self.driver.find_element(*self.account_number).get_attribute("value") == account_number, "Account number not set correctly"
        assert self.driver.find_element(*self.verify_account_number).get_attribute("value") == verify_account_number, "Verify account not set correctly"
        assert account_number == verify_account_number, "Account numbers do not match"

    def enter_amount(self, amount):
        self.driver.find_element(*self.amount).clear()
        self.driver.find_element(*self.amount).send_keys(str(amount))
        # Validate minimum amount
        entered = float(self.driver.find_element(*self.amount).get_attribute("value"))
        assert entered >= 0.01, f"Amount {entered} is below minimum allowed"

    def select_source_account(self, account_id):
        dropdown = self.driver.find_element(*self.from_account_id)
        dropdown.click()
        for option in dropdown.find_elements_by_tag_name("option"):
            if option.get_attribute("value") == str(account_id):
                option.click()
                break
        # Validate selection
        selected = dropdown.get_attribute("value")
        assert selected == str(account_id), "Source account not selected correctly"

    def send_payment(self):
        self.driver.find_element(*self.send_payment_button).click()
        # Wait for confirmation
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(self.success_message)
        )

    def verify_confirmation(self, expected_payee, expected_amount, expected_account):
        success_text = self.driver.find_element(*self.success_message).text
        assert "Payment processed successfully" in success_text or "Confirmation" in success_text, "Success message not found"
        actual_payee = self.driver.find_element(*self.conf_payee_name).text
        actual_amount = self.driver.find_element(*self.conf_amount).text
        actual_account = self.driver.find_element(*self.conf_from_account).text
        assert actual_payee == expected_payee, f"Payee name mismatch: {actual_payee} != {expected_payee}"
        assert actual_amount == str(expected_amount), f"Amount mismatch: {actual_amount} != {expected_amount}"
        assert actual_account == str(expected_account), f"Account mismatch: {actual_account} != {expected_account}"

    # End-to-end workflow for Bill Pay
    def pay_bill(self, payee_details, account_details, amount, source_account):
        self.navigate_to_bill_pay()
        self.fill_payee_details(**payee_details)
        self.fill_account_details(**account_details)
        self.enter_amount(amount)
        self.select_source_account(source_account)
        self.send_payment()
        self.verify_confirmation(
            expected_payee=payee_details['payee_name'],
            expected_amount=amount,
            expected_account=source_account
        )
