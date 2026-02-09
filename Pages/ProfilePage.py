"""
Page Object for Profile Page.
Provides method for clicking on user profile icon.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class ProfilePage:
    """
    Page Object representing the Profile Page.
    Implements method for clicking user profile icon.
    """
    user_profile_icon_locator = (By.CSS_SELECTOR, "#profile-icon")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click_profile(self) -> None:
        icon = self.driver.find_element(*self.user_profile_icon_locator)
        icon.click()
