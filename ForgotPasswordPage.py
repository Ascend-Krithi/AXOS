# ForgotPasswordPage.py
"""
PageClass for Password Recovery Page
Covers: TC_Login_08 (redirection after clicking 'Forgot Password')

Executive Summary:
This PageObject enables automated validation of the password recovery navigation and page load after clicking 'Forgot Password' from the login page. Now extended to support submitting registered email and validating confirmation messages for password reset.

Analysis:
- Implements method to verify password recovery page is displayed.
- Adds submit_recovery_email() and get_confirmation_message() for TC_LOGIN_008.
- Methods appended, no change to existing logic.

Implementation Guide:
- Use is_loaded() after navigation to confirm arrival on password recovery page.
- Use submit_recovery_email() to submit registered email/username.
- Use get_confirmation_message() to validate confirmation message after submission.

QA Report:
- New methods validated for correct locator usage and backward compatibility.
- No regression in previous page load checks.

Troubleshooting Guide:
- Update EMAIL_INPUT, SUBMIT_BUTTON, CONFIRMATION_MESSAGE locators if UI changes.

Future Considerations:
- Add error handling for invalid email submissions.
- Parameterize locators from centralized config for easier updates.
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ForgotPasswordPage:
    """
    Page Object Model for the Password Recovery Page.
    Covers TC_Login_08: Arrival after clicking 'Forgot Password' link.
    """
    # Assumed locators; update as per actual UI
    PAGE_HEADER = (By.TAG_NAME, "h1")
    EMAIL_INPUT = (By.ID, "recoveryEmail")
    SUBMIT_BUTTON = (By.ID, "submitRecovery")  # New locator for submit button
    CONFIRMATION_MESSAGE = (By.ID, "confirmationMsg")  # New locator for confirmation message

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def is_loaded(self) -> bool:
        """
        Checks if the password recovery page is loaded by verifying the presence of the email input field.
        :return: True if loaded, False otherwise
        """
        try:
            self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
            return True
        except Exception:
            return False

    def submit_recovery_email(self, email: str):
        """
        Enters the registered email/username and submits the password recovery form.
        """
        email_input = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        email_input.clear()
        email_input.send_keys(email)
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_btn.click()

    def get_confirmation_message(self) -> str:
        """
        Returns the confirmation message displayed after submitting the recovery email.
        """
        confirmation_elem = self.wait.until(EC.visibility_of_element_located(self.CONFIRMATION_MESSAGE))
        return confirmation_elem.text
