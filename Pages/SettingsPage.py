"""
Page Object for Settings Page.
Provides method for opening the settings menu.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

class SettingsPage:
    """
    Page Object representing the Settings Page.
    Implements method for opening settings menu.
    """
    settings_menu_locator = (By.CSS_SELECTOR, "#settings-menu")

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_settings(self) -> None:
        menu = self.driver.find_element(*self.settings_menu_locator)
        menu.click()
