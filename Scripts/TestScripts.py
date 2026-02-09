# Scripts/TestScripts.py
import unittest
from selenium import webdriver
from Pages.FinancialTransferPage import FinancialTransferPage
from Pages.TransferPage import TransferPage

class TestLogin(unittest.TestCase):
    # Existing login-related test methods...
    pass

class TestFinancialTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        self.page = FinancialTransferPage(self.driver)

    def test_TC_158_01_valid_financial_transfer(self):
        """
        TC-158-01: Valid financial transfer
        """
        confirmation = self.page.submit_transfer_payload(
            amount=100.00,
            currency='USD',
            source='ACC123',
            destination='ACC456',
            timestamp='2024-06-01T10:00:00Z'
        )
        confirmation_message = self.page.get_confirmation_message()
        self.assertIsInstance(confirmation_message, str)
        self.assertTrue(len(confirmation_message) > 0, "Confirmation message should not be empty.")

    def test_TC_158_02_invalid_transfer_missing_destination(self):
        """
        TC-158-02: Invalid transfer missing 'destination' field
        """
        self.page.submit_invalid_payload(
            amount=50.00,
            currency='USD',
            source='ACC123',
            timestamp='2024-06-01T10:00:00Z'
        )
        error_message = self.page.get_error_message()
        self.assertIsInstance(error_message, str)
        self.assertIn('destination', error_message.lower(), "Error message should mention missing 'destination'.")

class TestTransfer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)
        cls.transfer_page = TransferPage(cls.driver)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def setUp(self):
        # Navigate to transfer page before each test
        base_url = "http://localhost:8000"  # Replace with actual base URL as needed
        self.transfer_page.navigate_to_transfer(base_url)

    def test_TC_158_03_minimum_allowed_transfer(self):
        """
        TC-158-03: Submit transfer with minimum allowed amount (0.01 USD)
        Steps:
        1. Prepare a JSON payload with amount set to minimum allowed (0.01).
        2. Submit the payload to the transfer endpoint.
        Expected:
        - Payload is accepted and processed successfully.
        - Transfer is completed and confirmation response is returned.
        """
        self.transfer_page.submit_minimum_amount_transfer()
        success = self.transfer_page.validate_transfer_success()
        self.assertTrue(success, "Minimum allowed transfer should be processed successfully.")

    def test_TC_158_04_exceeding_maximum_allowed_transfer(self):
        """
        TC-158-04: Submit transfer with amount exceeding maximum allowed (1,000,000.00 USD)
        Steps:
        1. Prepare a JSON payload with amount exceeding the maximum allowed (1,000,000.00).
        2. Submit the payload to the transfer endpoint.
        Expected:
        - Payload is rejected with appropriate error message.
        - API returns error: 'Amount exceeds maximum limit'.
        """
        self.transfer_page.submit_exceeding_maximum_amount_transfer()
        error_valid = self.transfer_page.validate_transfer_error("Amount exceeds maximum limit")
        self.assertTrue(error_valid, "Transfer exceeding maximum limit should return correct error message.")

if __name__ == "__main__":
    unittest.main()
