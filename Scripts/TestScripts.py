import pytest
from Pages.LoginPage import LoginPage
from Pages.DashboardPage import DashboardPage

@pytest.mark.usefixtures("setup")
class TestLogin:

    def test_TC_LOGIN_001_valid_login(self):
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("validPass")
        login_page.click_login()
        assert dashboard_page.is_loaded(), "Dashboard did not load after valid login"

    def test_TC_LOGIN_002_invalid_password(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("wrongPass")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for invalid password"

    def test_TC_LOGIN_003_blank_username(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("")
        login_page.enter_password("somePass")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for blank username"

    def test_TC_LOGIN_004_blank_password(self):
        login_page = LoginPage(self.driver)
        login_page.enter_username("validUser")
        login_page.enter_password("")
        login_page.click_login()
        assert login_page.is_error_displayed(), "Error message not displayed for blank password"

    # TC_LOGIN_005: Login with special characters in username and password
    def test_TC_LOGIN_005_special_characters_credentials(self):
        login_page = LoginPage(self.driver)
        special_username = "!@#$%^&*()_+{}|:\"<>?~"
        special_password = "`-=[]\\;',./"
        login_page.enter_username(special_username)
        login_page.enter_password(special_password)
        login_page.click_login()
        # Assuming the system should not allow login with special characters and should display an error
        assert login_page.is_error_displayed(), "Error message not displayed for special character credentials"

    # TC_LOGIN_006: 'Remember Me' session persistence
    def test_TC_LOGIN_006_remember_me_session_persistence(self):
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        username = "validUser"
        password = "validPass"

        login_page.enter_username(username)
        login_page.enter_password(password)
        login_page.select_remember_me()
        login_page.click_login()
        assert dashboard_page.is_loaded(), "Dashboard did not load after login with 'Remember Me'"

        # Simulate browser close and reopen
        self.driver.quit()
        self.setup_method()  # Assuming this reinitializes self.driver and fixture

        dashboard_page = DashboardPage(self.driver)
        assert dashboard_page.is_loaded(), "'Remember Me' did not persist session after browser restart"
