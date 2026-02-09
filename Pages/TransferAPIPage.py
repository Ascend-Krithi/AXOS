import requests
from typing import Dict, Any

class TransferAPIPage:
    """
    PageClass for handling /transfer endpoint API interactions for test automation.
    This class prepares JSON payloads, submits them to the /transfer endpoint, and validates responses.
    Strictly adheres to code integrity, input validation, and structured output for downstream automation.
    """

    def __init__(self, base_url: str, auth_token: str = None):
        """
        :param base_url: Base URL of the API (e.g., 'https://api.example.com')
        :param auth_token: Optional authentication token for API requests
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.auth_token:
            headers["Authorization"] = f"Bearer {self.auth_token}"
        return headers

    def submit_transfer(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submits a transfer request to the /transfer endpoint.
        Validates required fields and returns structured response.
        :param payload: JSON payload for transfer (must include 'amount')
        :return: Dict with keys: 'status_code', 'success', 'response_json', 'error_message'
        """
        # Validate fields
        if "amount" not in payload:
            return {
                "status_code": 400,
                "success": False,
                "response_json": {},
                "error_message": "Missing required field: amount"
            }
        try:
            resp = requests.post(
                f"{self.base_url}/transfer",
                json=payload,
                headers=self._headers()
            )
            resp_json = resp.json() if resp.content else {}
            # Determine success by status code and response
            success = resp.status_code == 200 and resp_json.get("result", "") == "success"
            error_message = resp_json.get("error", "") if not success else ""
            return {
                "status_code": resp.status_code,
                "success": success,
                "response_json": resp_json,
                "error_message": error_message
            }
        except Exception as e:
            return {
                "status_code": 500,
                "success": False,
                "response_json": {},
                "error_message": str(e)
            }

    def submit_minimum_amount_transfer(self) -> Dict[str, Any]:
        """
        TestCase TC-158-03: Prepare payload with minimum amount (0.01), submit, expect success.
        :return: Structured response dict
        """
        payload = {"amount": 0.01}
        result = self.submit_transfer(payload)
        # Validate result
        assert result["status_code"] == 200, f"Expected 200 OK, got {result['status_code']}"
        assert result["success"] is True, f"Expected success, got {result['error_message']}"
        return result

    def submit_exceed_maximum_amount_transfer(self) -> Dict[str, Any]:
        """
        TestCase TC-158-04: Prepare payload with amount exceeding maximum (1000000.00), submit, expect rejection with error message.
        :return: Structured response dict
        """
        payload = {"amount": 1000000.00}
        result = self.submit_transfer(payload)
        # Validate rejection
        assert result["success"] is False, "Expected rejection for exceeding maximum amount"
        assert result["error_message"], "Expected error message for rejection"
        return result