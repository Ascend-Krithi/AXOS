# Existing imports and class content restored here
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Locators loaded from Locators.json (example)
import json
with open('Locators.json', 'r') as f:
    LOCATORS = json.load(f)

class RuleConfigurationPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Existing methods ...

    def add_rule_schema_with_malicious_script(self, schema_name, script):
        """
        Adds a rule schema with malicious script in metadata, verifies error handling and no script injection occurs.
        Args:
            schema_name (str): Name of the schema
            script (str): Malicious script to inject
        Returns:
            bool: True if error is shown and script is not injected, False otherwise
        """
        try:
            # Navigate to rule schema creation
            self.wait.until(EC.element_to_be_clickable((By.XPATH, LOCATORS['rule_schema_create_button']))).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_name_input']))).send_keys(schema_name)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_metadata_input']))).send_keys(script)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, LOCATORS['rule_schema_save_button']))).click()
            # Check for error message
            error_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_error_message'])))
            error_text = error_element.text
            if 'malicious script' in error_text.lower() or 'invalid input' in error_text.lower():
                # Ensure script is not injected
                page_source = self.driver.page_source
                if script not in page_source:
                    return True
            return False
        except TimeoutException:
            return False

    def add_rule_schema_with_unsupported_trigger(self, schema_name, trigger_type):
        """
        Adds a rule schema with unsupported trigger type, verifies graceful rejection/extensibility warning.
        Args:
            schema_name (str): Name of the schema
            trigger_type (str): Unsupported trigger type
        Returns:
            bool: True if extensibility warning is shown and schema is rejected, False otherwise
        """
        try:
            self.wait.until(EC.element_to_be_clickable((By.XPATH, LOCATORS['rule_schema_create_button']))).click()
            self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_name_input']))).send_keys(schema_name)
            self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_trigger_type_input']))).send_keys(trigger_type)
            self.wait.until(EC.element_to_be_clickable((By.XPATH, LOCATORS['rule_schema_save_button']))).click()
            warning_element = self.wait.until(EC.visibility_of_element_located((By.XPATH, LOCATORS['rule_schema_extensibility_warning'])))
            warning_text = warning_element.text
            if 'unsupported trigger' in warning_text.lower() or 'extensibility' in warning_text.lower():
                # Ensure schema is not created
                schemas = self.driver.find_elements(By.XPATH, LOCATORS['rule_schema_list_items'])
                for schema in schemas:
                    if schema_name in schema.text:
                        return False
                return True
            return False
        except TimeoutException:
            return False

# End of file
