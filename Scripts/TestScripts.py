
import unittest
from Pages.FinancialTransferPage import FinancialTransferPage

class TestFinancialTransfer(unittest.TestCase):

    def setUp(self):
        self.page = FinancialTransferPage()

    # Existing test methods...

    def test_TC_158_07_bulk_transfer_performance(self):
        """TC-158-07: Bulk Transfer Performance Validation
        - Prepare 10,000 unique transfer payloads.
        - Submit all payloads rapidly.
        - Log and validate response times and throughput.
        - Assert all transfers processed within <1s per transfer.
        """
        import time
        payloads = []
        for i in range(10000):
            payload = {
                "transfer_id": f"T{i:05d}",
                "amount": 100 + i,
                "currency": "USD",
                "recipient": f"recipient_{i}@example.com"
            }
            payloads.append(payload)
        
        start_time = time.time()
        responses = self.page.submit_bulk_transfers(payloads)
        perf_metrics = self.page.monitor_api_performance(responses)
        
        # Validate number of responses
        self.assertEqual(len(responses), 10000, "Not all transfers returned responses.")
        
        # Validate performance thresholds
        for idx, metric in enumerate(perf_metrics):
            self.assertLessEqual(
                metric['response_time'],
                1.0,
                f"Transfer {idx} exceeded 1s: {metric['response_time']}"
            )
        total_time = time.time() - start_time
        throughput = 10000 / total_time
        print(f"Total time: {total_time:.2f}s, Throughput: {throughput:.2f} transfers/sec")
        self.assertGreaterEqual(throughput, 10000, "Throughput below expected threshold.")

    def test_TC_158_08_invalid_token_authentication_error(self):
        """TC-158-08: Invalid Token Authentication Error
        - Prepare a valid JSON payload.
        - Submit with invalid token.
        - Assert error message 'Invalid authentication token' is shown.
        """
        payload = {
            "transfer_id": "T99999",
            "amount": 500,
            "currency": "USD",
            "recipient": "recipient_invalid@example.com"
        }
        invalid_token = "invalid_token_123"
        response = self.page.submit_transfer_with_invalid_token(payload, invalid_token)
        error_valid = self.page.validate_authentication_error(response, expected_message="Invalid authentication token")
        self.assertTrue(error_valid, "Authentication error message not shown or incorrect.")

if __name__ == '__main__':
    unittest.main()
