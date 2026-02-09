import unittest
from Pages.TransferAPIPage import TransferAPIPage

class TestTransferAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api_page = TransferAPIPage()

    # Existing test methods...

    def test_TC_158_09_valid_transfer_and_log_entry(self):
        """TC-158-09: Submit valid transfer payload and verify log entry."""
        payload = {
            'amount': 200.00,
            'currency': 'USD',
            'source': 'ACC123',
            'destination': 'ACC456',
            'timestamp': '2024-06-01T10:00:00Z'
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.api_page.validate_transfer_success(response)
        log_entry = self.api_page.query_backend_log_entry(payload['timestamp'], payload['source'], payload['destination'])
        self.assertIsNotNone(log_entry, "Log entry should exist for valid transfer.")
        self.assertEqual(log_entry['amount'], payload['amount'])
        self.assertEqual(log_entry['currency'], payload['currency'])
        self.assertEqual(log_entry['source'], payload['source'])
        self.assertEqual(log_entry['destination'], payload['destination'])
        self.assertEqual(log_entry['timestamp'], payload['timestamp'])

    def test_TC_158_10_unsupported_currency_rejection(self):
        """TC-158-10: Submit transfer with unsupported currency and verify rejection."""
        payload = {
            'amount': 100.00,
            'currency': 'XYZ',
            'source': 'ACC123',
            'destination': 'ACC456',
            'timestamp': '2024-06-01T11:00:00Z'
        }
        response = self.api_page.submit_transfer_payload(payload)
        self.api_page.validate_transfer_rejection(response, expected_error='Unsupported currency')

if __name__ == '__main__':
    unittest.main()
