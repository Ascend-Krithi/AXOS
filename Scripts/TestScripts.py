# Existing imports and code remain unchanged
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Pages.BillPayPage import BillPayPage
from Pages.NavigationPage import NavigationPage

# ... (existing test methods remain unchanged)

def test_billpay_extremely_large_amount(driver):
    """
    TC-SCRUM-15483-007: Enter valid payee details and an extremely large amount, submit, and verify outcome.
    Steps:
    1. Navigate to Bill Pay page.
    2. Enter valid payee details (name, address, phone, account).
    3. Enter extremely large amount (e.g., 9999999999).
    4. Select valid account.
    5. Submit payment.
    6. Verify for success message or appropriate error message.
    """
    nav_page = NavigationPage(driver)
    billpay_page = BillPayPage(driver)

    nav_page.go_to_billpay()
    
    # Wait for Bill Pay page to load
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, billpay_page.payee_name_id))
    )

    # Enter payee details
    billpay_page.enter_payee_name("Test Automation Payee")
    billpay_page.enter_address("1234 Test Lane")
    billpay_page.enter_city("Testville")
    billpay_page.enter_state("TS")
    billpay_page.enter_zip_code("12345")
    billpay_page.enter_phone("555-123-4567")
    billpay_page.enter_account("123456789")
    
    # Enter extremely large amount
    large_amount = "9999999999"
    billpay_page.enter_amount(large_amount)

    # Select valid account
    billpay_page.select_from_account("54321")

    # Submit payment
    billpay_page.submit_payment()

    # Handle possible outcomes: success or error
    try:
        # Wait for either success or error message
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.visibility_of_element_located((By.ID, billpay_page.success_message_id)),
                EC.visibility_of_element_located((By.ID, billpay_page.error_message_id))
            )
        )
        if billpay_page.is_payment_successful():
            assert True, "Payment succeeded with extremely large amount."
        else:
            error_text = billpay_page.get_error_message()
            assert "amount" in error_text.lower() or "limit" in error_text.lower(), \
                f"Unexpected error message: {error_text}"
    except Exception as e:
        pytest.fail(f"Neither success nor error message appeared: {e}")

def test_billpay_session_timeout(driver):
    """
    TC-SCRUM-15483-008: Enter valid payee/payment details, simulate session timeout, and verify session expiry behavior.
    Steps:
    1. Navigate to Bill Pay page.
    2. Enter valid payee details and amount.
    3. Simulate session timeout (e.g., wait for session expiry or delete session cookie).
    4. Attempt to submit payment.
    5. Verify session expired message or redirect to login.
    """
    import time

    nav_page = NavigationPage(driver)
    billpay_page = BillPayPage(driver)

    nav_page.go_to_billpay()
    
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, billpay_page.payee_name_id))
    )

    # Enter payee details
    billpay_page.enter_payee_name("Timeout Payee")
    billpay_page.enter_address("5678 Timeout Blvd")
    billpay_page.enter_city("Expiretown")
    billpay_page.enter_state("EX")
    billpay_page.enter_zip_code("98765")
    billpay_page.enter_phone("555-987-6543")
    billpay_page.enter_account("987654321")
    billpay_page.enter_amount("100.00")
    billpay_page.select_from_account("12345")

    # Simulate session timeout
    driver.delete_all_cookies()  # This simulates session expiry
    time.sleep(1)  # Ensure cookies are cleared

    # Attempt to submit payment
    billpay_page.submit_payment()

    # Verify session expired handling
    try:
        # Wait for redirect to login or session expired message
        WebDriverWait(driver, 10).until(
            EC.any_of(
                EC.url_contains("login"),
                EC.visibility_of_element_located((By.ID, getattr(billpay_page, 'session_expired_id', 'sessionExpiredMessage')))
            )
        )
        current_url = driver.current_url
        if "login" in current_url.lower():
            assert True, "Redirected to login page after session timeout."
        elif hasattr(billpay_page, "is_session_expired") and billpay_page.is_session_expired():
            assert True, "Session expired message displayed."
        else:
            # Try to get session expired message
            try:
                msg = driver.find_element(By.ID, getattr(billpay_page, 'session_expired_id', 'sessionExpiredMessage')).text
                assert "session expired" in msg.lower() or "login" in msg.lower(), f"Unexpected session message: {msg}"
            except Exception:
                pytest.fail("No session expired indication after timeout.")
    except Exception as e:
        pytest.fail(f"Session timeout handling failed: {e}")

# End of file
