import unittest
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage
from Pages.FinancialTransferAPIPage import FinancialTransferAPIPage

class TestScripts(unittest.TestCase):

    def setUp(self):
        self.login_page = LoginPage()
        self.dashboard_page = DashboardPage()
        self.financial_transfer_api_page = FinancialTransferAPIPage()

    def test_login_valid(self):
        # Existing login test
        self.login_page.open()
        self.login_page.enter_credentials('valid_user', 'valid_password')
        self.login_page.submit()
        self.assertTrue(self.login_page.is_logged_in())

    def test_dashboard_load(self):
        # Existing dashboard test
        self.dashboard_page.open()
        self.assertTrue(self.dashboard_page.is_dashboard_loaded())

    # --- New Test Cases for Financial Transfer API ---

    def test_TC_158_01_valid_transfer(self):
        """
        TC-158-01: Submit valid payload, expect confirmation.
        Steps:
        - Prepare a valid payload
        - Submit it
        - Assert successful transfer
        """
        payload = self.financial_transfer_api_page.prepare_valid_payload()
        response = self.financial_transfer_api_page.send_transfer_payload(payload)
        self.financial_transfer_api_page.validate_successful_transfer(response)
        # Optionally, assert response structure if needed
        self.assertTrue(response.get('status') == 'success')
        self.assertIn('confirmation', response)

    def test_TC_158_02_missing_destination(self):
        """
        TC-158-02: Submit payload missing 'destination', expect error for missing field.
        Steps:
        - Prepare a payload missing 'destination'
        - Submit it
        - Assert error for missing field
        """
        payload = self.financial_transfer_api_page.prepare_invalid_payload_missing_destination()
        response = self.financial_transfer_api_page.send_transfer_payload(payload)
        self.financial_transfer_api_page.validate_missing_field_error(response)
        # Optionally, assert error details if needed
        self.assertTrue(response.get('status') == 'error')
        self.assertIn('missing_field', response)
        self.assertEqual(response.get('missing_field'), 'destination')

if __name__ == "__main__":
    unittest.main()
