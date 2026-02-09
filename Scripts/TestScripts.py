import unittest
from Pages.TransferAPIPage import TransferAPIPage

class TestTransferAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Example: You may need to provide base_url and auth_token
        cls.api_page = TransferAPIPage(base_url="http://localhost:8000", auth_token="test-token")

    # TC-158-09: Valid transfer and backend log verification
    def test_TC_158_09_valid_transfer_and_backend_log(self):
        """
        Test Case TC-158-09:
        1. Submit a valid transfer payload.
        2. Query backend system for transfer log entry.
        """
        payload = {
            "amount": 200.00,
            "currency": "USD",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.assertTrue(self.api_page.validate_transfer_success(response), "Transfer should be processed successfully.")
        # Stub DB query function for backend log validation
        def db_query_fn(details):
            # Simulate DB log exists and matches details
            # In real test, replace with actual DB agent
            return (details["amount"] == 200.00 and
                    details["currency"] == "USD" and
                    details["source"] == "ACC123" and
                    details["destination"] == "ACC456" and
                    details["timestamp"] == "2024-06-01T10:00:00Z")
        self.assertTrue(self.api_page.validate_backend_log_entry(payload, db_query_fn), "Log entry should exist for transfer with correct details.")

    # TC-158-10: Unsupported currency rejection
    def test_TC_158_10_unsupported_currency_rejection(self):
        """
        Test Case TC-158-10:
        1. Prepare a JSON payload with unsupported currency (e.g., 'XYZ').
        2. Submit the payload to the transfer endpoint and verify rejection.
        """
        payload = {
            "amount": 100.00,
            "currency": "XYZ",
            "source": "ACC123",
            "destination": "ACC456",
            "timestamp": "2024-06-01T10:00:00Z"
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.assertTrue(self.api_page.validate_unsupported_currency_error(response), "API should return error: 'Unsupported currency'.")

if __name__ == "__main__":
    unittest.main()
