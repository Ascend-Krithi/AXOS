from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class RuleConfigurationPage:
    """
    Page Object for Rule Configuration Page.
    Handles rule creation, trigger setup (specific_date and recurring),
    action setup (fixed_amount and percentage_of_deposit), conditions, and validation.
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

        # Locators (example structure, replace with actual from Locators.json)
        self.locators = {
            "rule_form": (By.ID, "ruleForm"),
            "trigger_type_dropdown": (By.ID, "triggerType"),
            "trigger_date_input": (By.ID, "triggerDate"),
            "trigger_interval_dropdown": (By.ID, "triggerInterval"),
            "action_type_dropdown": (By.ID, "actionType"),
            "fixed_amount_input": (By.ID, "fixedAmount"),
            "percentage_input": (By.ID, "percentageOfDeposit"),
            "add_condition_btn": (By.ID, "addCondition"),
            "condition_field": (By.CLASS_NAME, "conditionField"),
            "submit_btn": (By.ID, "submitRule"),
            "validation_message": (By.ID, "validationMessage"),
            "rule_list": (By.ID, "ruleList"),
        }

    def open_rule_form(self):
        self.wait.until(EC.visibility_of_element_located(self.locators["rule_form"]))

    def select_trigger_type(self, trigger_type):
        trigger_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["trigger_type_dropdown"]))
        trigger_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='triggerType']/option[@value='{trigger_type}']")
        option.click()

    def set_specific_date_trigger(self, date_str):
        self.select_trigger_type("specific_date")
        date_input = self.wait.until(EC.visibility_of_element_located(self.locators["trigger_date_input"]))
        date_input.clear()
        date_input.send_keys(date_str)

    def set_recurring_trigger(self, interval):
        self.select_trigger_type("recurring")
        interval_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["trigger_interval_dropdown"]))
        interval_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='triggerInterval']/option[@value='{interval}']")
        option.click()

    def select_action_type(self, action_type):
        action_dropdown = self.wait.until(EC.element_to_be_clickable(self.locators["action_type_dropdown"]))
        action_dropdown.click()
        option = self.driver.find_element(By.XPATH, f"//select[@id='actionType']/option[@value='{action_type}']")
        option.click()

    def set_fixed_amount_action(self, amount):
        self.select_action_type("fixed_amount")
        amount_input = self.wait.until(EC.visibility_of_element_located(self.locators["fixed_amount_input"]))
        amount_input.clear()
        amount_input.send_keys(str(amount))

    def set_percentage_of_deposit_action(self, percentage):
        self.select_action_type("percentage_of_deposit")
        percentage_input = self.wait.until(EC.visibility_of_element_located(self.locators["percentage_input"]))
        percentage_input.clear()
        percentage_input.send_keys(str(percentage))

    def add_condition(self, condition_text):
        add_btn = self.wait.until(EC.element_to_be_clickable(self.locators["add_condition_btn"]))
        add_btn.click()
        condition_field = self.wait.until(EC.visibility_of_element_located(self.locators["condition_field"]))
        condition_field.send_keys(condition_text)

    def submit_rule(self):
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.locators["submit_btn"]))
        submit_btn.click()

    def get_validation_message(self):
        msg_elem = self.wait.until(EC.visibility_of_element_located(self.locators["validation_message"]))
        return msg_elem.text

    def rule_exists_in_list(self, rule_desc):
        rule_list = self.wait.until(EC.visibility_of_element_located(self.locators["rule_list"]))
        return rule_desc in rule_list.text

    def create_rule(self, rule_json):
        """
        Orchestrates rule creation from JSON:
        {
            "trigger": {"type": "specific_date", "date": "2024-07-01T10:00:00Z"}
            "action": {"type": "fixed_amount", "amount": 100}
            "conditions": []
        }
        """
        self.open_rule_form()
        trigger = rule_json.get("trigger", {})
        action = rule_json.get("action", {})
        conditions = rule_json.get("conditions", [])

        # Trigger setup
        if trigger.get("type") == "specific_date":
            self.set_specific_date_trigger(trigger.get("date", ""))
        elif trigger.get("type") == "recurring":
            self.set_recurring_trigger(trigger.get("interval", ""))

        # Action setup
        if action.get("type") == "fixed_amount":
            self.set_fixed_amount_action(action.get("amount", ""))
        elif action.get("type") == "percentage_of_deposit":
            self.set_percentage_of_deposit_action(action.get("percentage", ""))

        # Conditions
        for cond in conditions:
            self.add_condition(cond)

        self.submit_rule()
        return self.get_validation_message()

    def validate_rule_execution(self, rule_desc, expected=True):
        """
        Validates if a rule exists in the rule list.
        """
        exists = self.rule_exists_in_list(rule_desc)
        if expected:
            assert exists, f"Rule '{rule_desc}' not found in list."
        else:
            assert not exists, f"Rule '{rule_desc}' should not exist in list."
