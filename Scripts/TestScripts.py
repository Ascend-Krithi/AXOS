
{Import necessary modules}

class TestLoginFunctionality:
    def __init__(self, page):
        self.page = page
        self.login_page = LoginPage(page)

    async def test_empty_fields_validation(self):
        await self.login_page.navigate()
        await self.login_page.submit_login('', '')
        assert await self.login_page.get_error_message() == 'Mandatory fields are required'

    async def test_remember_me_functionality(self):
        await self.login_page.navigate()
        await self.login_page.fill_email('

class TestRuleConfiguration:
    def __init__(self, page):
        self.page = page
        self.rule_page = RuleConfigurationPage(page)

    async def test_TC_SCRUM158_01_create_rule_with_all_types(self):
        # Step 1: Prepare a JSON rule schema with all supported trigger, condition, and action types populated.
        rule_schema = {
            "name": "AllTypesRule",
            "triggers": [
                {"type": "onCreate", "params": {}},
                {"type": "onUpdate", "params": {}},
                {"type": "onDelete", "params": {}}
            ],
            "conditions": [
                {"type": "fieldEquals", "field": "status", "value": "active"},
                {"type": "fieldContains", "field": "description", "value": "urgent"},
                {"type": "fieldGreaterThan", "field": "priority", "value": 5}
            ],
            "actions": [
                {"type": "sendEmail", "recipients": ["admin@example.com"], "subject": "Rule Triggered"},
                {"type": "createTask", "taskType": "followup", "assignee": "user1"},
                {"type": "logEvent", "message": "Rule executed successfully"}
            ]
        }

        # Step 2: Submit the rule schema to the API endpoint for rule creation.
        response = await self.rule_page.submit_rule_schema_api(rule_schema)
        assert response.status_code == 201, f"Rule creation failed: {response.text}"

        rule_id = response.json().get("id")
        assert rule_id is not None, "Rule ID not returned after creation"

        # Step 3: Retrieve the created rule from the database.
        created_rule = await self.rule_page.get_rule_from_db(rule_id)
        assert created_rule is not None, "Rule not found in database"
        assert created_rule["name"] == rule_schema["name"]
        assert len(created_rule["triggers"]) == len(rule_schema["triggers"])
        assert len(created_rule["conditions"]) == len(rule_schema["conditions"])
        assert len(created_rule["actions"]) == len(rule_schema["actions"])

    async def test_TC_SCRUM158_02_create_rule_with_two_conditions_and_actions(self):
        # Step 1: Prepare a rule schema with two conditions and two actions.
        rule_schema = {
            "name": "TwoCondTwoActRule",
            "triggers": [
                {"type": "onUpdate", "params": {}}
            ],
            "conditions": [
                {"type": "fieldEquals", "field": "priority", "value": "high"},
                {"type": "fieldContains", "field": "description", "value": "escalate"}
            ],
            "actions": [
                {"type": "sendEmail", "recipients": ["support@example.com"], "subject": "Priority Escalated"},
                {"type": "createTask", "taskType": "escalation", "assignee": "team_lead"}
            ]
        }

        # Step 2: Submit the schema to the API endpoint.
        response = await self.rule_page.submit_rule_schema_api(rule_schema)
        assert response.status_code == 201, f"Rule creation failed: {response.text}"
        rule_id = response.json().get("id")
        assert rule_id is not None, "Rule ID not returned after creation"

        # Step 3: Verify rule logic via simulation.
        simulation_payload = {
            "rule_id": rule_id,
            "test_data": {
                "priority": "high",
                "description": "Please escalate this issue."
            }
        }
        simulation_result = await self.rule_page.simulate_rule_logic(simulation_payload)
        assert simulation_result["actions_executed"] == ["sendEmail", "createTask"], f"Unexpected actions executed: {simulation_result['actions_executed']}"
        assert simulation_result["conditions_met"] == True, "Conditions not met during simulation"