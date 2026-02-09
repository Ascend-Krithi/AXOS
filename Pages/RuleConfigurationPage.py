"""
RuleConfigurationPage
----------------------
Selenium PageClass for Rule Configuration page automation.

This class provides structured methods to interact with rule creation, schema validation, metadata handling, and error validation as described in test cases TC_SCRUM158_03 and TC_SCRUM158_04.

Locators are strictly sourced from Locators.json, and methods are designed for async Selenium workflows (Playwright-style).

Sections:
- Rule Form: Fill rule details (ID, Name, Save)
- Triggers: Set trigger types, intervals, toggles
- Conditions: Add conditions, select types, set thresholds
- Actions: Choose action types, set amounts/accounts
- Validation: Edit JSON schema, validate, check success/error messages

Best Practices:
- All locators are initialized in __init__
- Methods are atomic and descriptive
- No existing logic is altered; new code is appended only
- Comprehensive docstrings for downstream automation

Usage Example:
    page = browser.new_page()
    rule_page = RuleConfigurationPage(page)
    await rule_page.fill_rule_form('R123', 'Transfer Rule')
    await rule_page.set_metadata({'description': 'Transfer rule', 'tags': ['finance', 'auto']})
    await rule_page.submit_schema()
    await rule_page.validate_schema()
    await rule_page.check_metadata('Transfer rule', ['finance', 'auto'])

"""

from typing import Any, Dict, List

class RuleConfigurationPage:
    def __init__(self, page):
        """
        Initialize RuleConfigurationPage with all locators.
        Args:
            page: Selenium/Playwright Page object
        """
        self.page = page
        # Rule Form
        self.rule_id_input = page.locator('id=rule-id-field')
        self.rule_name_input = page.locator('name=rule-name')
        self.save_rule_button = page.locator("button[data-testid='save-rule-btn']")
        # Triggers
        self.trigger_type_dropdown = page.locator('id=trigger-type-select')
        self.date_picker = page.locator("input[type='date']")
        self.recurring_interval_input = page.locator('id=interval-value')
        self.after_deposit_toggle = page.locator('id=trigger-after-deposit')
        # Conditions
        self.add_condition_btn = page.locator('id=add-condition-link')
        self.condition_type_dropdown = page.locator('select.condition-type')
        self.balance_threshold_input = page.locator("input[name='balance-limit']")
        self.transaction_source_dropdown = page.locator('id=source-provider-select')
        self.operator_dropdown = page.locator('css=.condition-operator-select')
        # Actions
        self.action_type_dropdown = page.locator('id=action-type-select')
        self.transfer_amount_input = page.locator('name=fixed-amount')
        self.percentage_input = page.locator('id=deposit-percentage')
        self.destination_account_input = page.locator('id=target-account-id')
        # Validation
        self.json_schema_editor = page.locator('css=.monaco-editor')
        self.validate_schema_btn = page.locator('id=btn-verify-json')
        self.success_message = page.locator('.alert-success')
        self.schema_error_message = page.locator("[data-testid='error-feedback-text']")

    async def fill_rule_form(self, rule_id: str, rule_name: str):
        """
        Fill rule ID and rule name fields and click Save.
        """
        await self.rule_id_input.fill(rule_id)
        await self.rule_name_input.fill(rule_name)
        await self.save_rule_button.click()

    async def set_trigger(self, trigger_type: str, date: str = None, interval: int = None, after_deposit: bool = False):
        """
        Set trigger type and related fields.
        """
        await self.trigger_type_dropdown.select_option(trigger_type)
        if date:
            await self.date_picker.fill(date)
        if interval:
            await self.recurring_interval_input.fill(str(interval))
        if after_deposit:
            await self.after_deposit_toggle.check()

    async def add_condition(self, condition_type: str, balance_threshold: float = None, source: str = None, operator: str = None):
        """
        Add a new condition with specified details.
        """
        await self.add_condition_btn.click()
        await self.condition_type_dropdown.select_option(condition_type)
        if balance_threshold is not None:
            await self.balance_threshold_input.fill(str(balance_threshold))
        if source:
            await self.transaction_source_dropdown.select_option(source)
        if operator:
            await self.operator_dropdown.select_option(operator)

    async def set_action(self, action_type: str, amount: float = None, percentage: float = None, dest_account: str = None):
        """
        Set action details.
        """
        await self.action_type_dropdown.select_option(action_type)
        if amount is not None:
            await self.transfer_amount_input.fill(str(amount))
        if percentage is not None:
            await self.percentage_input.fill(str(percentage))
        if dest_account:
            await self.destination_account_input.fill(dest_account)

    async def set_metadata(self, metadata: Dict[str, Any]):
        """
        Set metadata fields in JSON schema editor.
        """
        import json
        schema_text = await self.json_schema_editor.inner_text()
        schema = json.loads(schema_text)
        schema['metadata'] = metadata
        await self.json_schema_editor.fill(json.dumps(schema, indent=2))

    async def submit_schema(self):
        """
        Submit the schema by clicking Save Rule button.
        """
        await self.save_rule_button.click()

    async def validate_schema(self):
        """
        Validate the schema using the Validate Schema button.
        """
        await self.validate_schema_btn.click()

    async def get_success_message(self) -> str:
        """
        Retrieve success message after schema validation.
        """
        return await self.success_message.inner_text()

    async def get_schema_error_message(self) -> str:
        """
        Retrieve error message after schema validation failure.
        """
        return await self.schema_error_message.inner_text()

    async def check_metadata(self, expected_description: str, expected_tags: List[str]) -> bool:
        """
        Retrieve schema from editor and check if metadata matches expected.
        """
        import json
        schema_text = await self.json_schema_editor.inner_text()
        schema = json.loads(schema_text)
        metadata = schema.get('metadata', {})
        return (
            metadata.get('description') == expected_description and
            metadata.get('tags') == expected_tags
        )

    # ------------------
    # TC_SCRUM158_07 (testCaseId: 1353)
    # ------------------
    async def create_rule_with_max_conditions_and_actions(self, rule_id: str, rule_name: str, conditions: list, actions: list) -> bool:
        """
        Creates a rule with the maximum supported number of conditions and actions.
        Steps:
        1. Fill rule form.
        2. Add all conditions (up to max supported).
        3. Add all actions (up to max supported).
        4. Validate the JSON schema.
        5. Submit the schema.
        6. Retrieve and validate all conditions/actions are persisted.
        Args:
            rule_id (str): Rule ID value
            rule_name (str): Rule Name value
            conditions (list): List of condition dicts
            actions (list): List of action dicts
        Returns:
            bool: True if all conditions/actions are persisted, False otherwise
        """
        import json
        # Step 1: Fill the rule form
        await self.fill_rule_form(rule_id, rule_name)
        # Step 2: Add all conditions
        for condition in conditions:
            await self.add_condition(**condition)
        # Step 3: Add all actions
        for action in actions:
            await self.set_action(**action)
        # Step 4: Validate JSON schema
        await self.validate_schema()
        success_msg = await self.get_success_message()
        if 'valid' not in success_msg.lower():
            return False
        # Step 5: Submit the schema
        await self.submit_schema()
        # Step 6: Retrieve and validate persistence
        schema_text = await self.json_schema_editor.inner_text()
        schema = json.loads(schema_text)
        persisted_conditions = schema.get('conditions', [])
        persisted_actions = schema.get('actions', [])
        return len(persisted_conditions) == len(conditions) and len(persisted_actions) == len(actions)

    # ------------------
    # TC_SCRUM158_08 (testCaseId: 1354)
    # ------------------
    async def create_rule_with_empty_conditions_and_actions(self, rule_id: str, rule_name: str) -> str:
        """
        Creates a rule with empty 'conditions' and 'actions' arrays and validates the schema.
        Steps:
        1. Fill rule form.
        2. Set empty conditions/actions in JSON schema editor.
        3. Validate the JSON schema.
        4. Submit the schema.
        5. Return API/validation response.
        Args:
            rule_id (str): Rule ID value
            rule_name (str): Rule Name value
        Returns:
            str: Validation result message (success or error)
        """
        import json
        # Step 1: Fill the rule form
        await self.fill_rule_form(rule_id, rule_name)
        # Step 2: Set empty arrays in JSON schema editor
        schema_text = await self.json_schema_editor.inner_text()
        schema = json.loads(schema_text)
        schema['conditions'] = []
        schema['actions'] = []
        await self.json_schema_editor.fill(json.dumps(schema, indent=2))
        # Step 3: Validate schema
        await self.validate_schema()
        # Step 4: Submit schema
        await self.submit_schema()
        # Step 5: Return validation message
        try:
            return await self.get_success_message()
        except Exception:
            return await self.get_schema_error_message()
