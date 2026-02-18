from selenium.webdriver.common.by import By

class BillPayPage:
    def __init__(self, driver):
        self.driver = driver
        self.payee_name = driver.find_element(By.NAME, 'payee.name')
        self.address = driver.find_element(By.NAME, 'payee.address.street')
        self.city = driver.find_element(By.NAME, 'payee.address.city')
        self.state = driver.find_element(By.NAME, 'payee.address.state')
        self.zip_code = driver.find_element(By.NAME, 'payee.address.zipCode')
        self.phone_number = driver.find_element(By.NAME, 'payee.phoneNumber')
        self.account_number = driver.find_element(By.NAME, 'payee.accountNumber')
        self.verify_account_number = driver.find_element(By.NAME, 'verifyAccount')
        self.amount = driver.find_element(By.NAME, 'amount')
        self.from_account_id = driver.find_element(By.NAME, 'fromAccountId')
        self.send_payment_button = driver.find_element(By.CSS_SELECTOR, "input[value='Send Payment']")
        self.success_message = driver.find_element(By.ID, 'billpayResult')
        self.conf_payee_name = driver.find_element(By.ID, 'payeeName')
        self.conf_amount = driver.find_element(By.ID, 'amount')
        self.conf_from_account = driver.find_element(By.ID, 'fromAccountId')

    def enter_payee_details(self, name, address, city, state, zip, phone, account, verify_account):
        self.payee_name.clear()
        self.payee_name.send_keys(name)
        self.address.clear()
        self.address.send_keys(address)
        self.city.clear()
        self.city.send_keys(city)
        self.state.clear()
        self.state.send_keys(state)
        self.zip_code.clear()
        self.zip_code.send_keys(zip)
        self.phone_number.clear()
        self.phone_number.send_keys(phone)
        self.account_number.clear()
        self.account_number.send_keys(account)
        self.verify_account_number.clear()
        self.verify_account_number.send_keys(verify_account)

    def enter_amount(self, amount):
        self.amount.clear()
        self.amount.send_keys(str(amount))

    def select_from_account(self, account_id):
        self.from_account_id.send_keys(account_id)

    def click_send_payment(self):
        self.send_payment_button.click()

    def get_success_message(self):
        return self.success_message.text

    def get_confirmation_details(self):
        return {
            'payee_name': self.conf_payee_name.text,
            'amount': self.conf_amount.text,
            'from_account': self.conf_from_account.text
        }
