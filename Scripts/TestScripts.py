
import pytest
from RuleConfigurationPage import RuleConfigurationPage

# Existing test code...

@pytest.mark.security
def test_sql_injection_in_rule_name(driver):
    page = RuleConfigurationPage(driver)
    malicious_rule_name = "test'; DROP TABLE rules;--"
    page.open_rule_creation()
    page.set_rule_name(malicious_rule_name)
    page.set_description('Safe description')
    page.add_trigger('Login')
    page.add_condition('UserRole', 'admin')
    page.add_action('Alert')
    page.submit_rule()
    assert page.is_error_displayed(), 'SQL injection payload should not be accepted'
    assert not page.is_rule_created(malicious_rule_name)
    log_entries = page.get_audit_log_entries(malicious_rule_name)
    assert any('blocked' in entry.lower() for entry in log_entries), 'Audit log should record blocked SQL injection'

@pytest.mark.security
def test_xss_in_description(driver):
    page = RuleConfigurationPage(driver)
    rule_name = 'XSS_Test'
    xss_payload = "<script>alert('XSS')</script>"
    page.open_rule_creation()
    page.set_rule_name(rule_name)
    page.set_description(xss_payload)
    page.add_trigger('Login')
    page.add_condition('UserRole', 'admin')
    page.add_action('Alert')
    page.submit_rule()
    assert page.is_error_displayed(), 'XSS payload should not be accepted'
    assert not page.is_rule_created(rule_name)
    log_entries = page.get_audit_log_entries(rule_name)
    assert any('blocked' in entry.lower() for entry in log_entries), 'Audit log should record blocked XSS'

@pytest.mark.security
def test_command_injection_in_condition_value(driver):
    page = RuleConfigurationPage(driver)
    rule_name = 'CmdInj_Test'
    cmd_inj_payload = "admin; rm -rf / --"
    page.open_rule_creation()
    page.set_rule_name(rule_name)
    page.set_description('Safe description')
    page.add_trigger('Login')
    page.add_condition('UserRole', cmd_inj_payload)
    page.add_action('Alert')
    page.submit_rule()
    assert page.is_error_displayed(), 'Command injection payload should not be accepted'
    assert not page.is_rule_created(rule_name)
    log_entries = page.get_audit_log_entries(rule_name)
    assert any('blocked' in entry.lower() for entry in log_entries), 'Audit log should record blocked command injection'

@pytest.mark.security
def test_audit_log_for_security_events(driver):
    page = RuleConfigurationPage(driver)
    # Attempt SQL injection
    page.open_rule_creation()
    page.set_rule_name("test'; DROP TABLE rules;--")
    page.set_description('Safe')
    page.add_trigger('Login')
    page.add_condition('UserRole', 'admin')
    page.add_action('Alert')
    page.submit_rule()
    # Attempt XSS
    page.open_rule_creation()
    page.set_rule_name('XSS_Test')
    page.set_description("<script>alert('XSS')</script>")
    page.add_trigger('Login')
    page.add_condition('UserRole', 'admin')
    page.add_action('Alert')
    page.submit_rule()
    # Attempt command injection
    page.open_rule_creation()
    page.set_rule_name('CmdInj_Test')
    page.set_description('Safe')
    page.add_trigger('Login')
    page.add_condition('UserRole', "admin; rm -rf / --")
    page.add_action('Alert')
    page.submit_rule()
    # Check audit log
    audit_log = page.get_audit_log()
    assert any('SQL injection' in entry for entry in audit_log)
    assert any('XSS' in entry for entry in audit_log)
    assert any('command injection' in entry for entry in audit_log)

@pytest.mark.limit
def test_max_triggers_conditions_actions(driver):
    page = RuleConfigurationPage(driver)
    rule_name = 'MaxTest'
    page.open_rule_creation()
    page.set_rule_name(rule_name)
    page.set_description('Testing max triggers/conditions/actions')
    # Add maximum allowed triggers
    for i in range(page.max_triggers):
        page.add_trigger(f'Trigger_{i}')
    assert page.triggers_count() == page.max_triggers
    # Add maximum allowed conditions
    for i in range(page.max_conditions):
        page.add_condition(f'Condition_{i}', 'value')
    assert page.conditions_count() == page.max_conditions
    # Add maximum allowed actions
    for i in range(page.max_actions):
        page.add_action(f'Action_{i}')
    assert page.actions_count() == page.max_actions
    page.submit_rule()
    assert page.is_rule_created(rule_name)
    log_entries = page.get_audit_log_entries(rule_name)
    assert any('created' in entry.lower() for entry in log_entries), 'Audit log should record rule creation'

@pytest.mark.limit
def test_exceeding_triggers_conditions_actions(driver):
    page = RuleConfigurationPage(driver)
    rule_name = 'ExceedTest'
    page.open_rule_creation()
    page.set_rule_name(rule_name)
    page.set_description('Testing exceeding triggers/conditions/actions')
    # Add triggers up to max + 1
    for i in range(page.max_triggers + 1):
        page.add_trigger(f'Trigger_{i}')
    assert page.triggers_count() == page.max_triggers
    assert page.is_error_displayed(), 'Should display error when exceeding max triggers'
    # Add conditions up to max + 1
    for i in range(page.max_conditions + 1):
        page.add_condition(f'Condition_{i}', 'value')
    assert page.conditions_count() == page.max_conditions
    assert page.is_error_displayed(), 'Should display error when exceeding max conditions'
    # Add actions up to max + 1
    for i in range(page.max_actions + 1):
        page.add_action(f'Action_{i}')
    assert page.actions_count() == page.max_actions
    assert page.is_error_displayed(), 'Should display error when exceeding max actions'
    page.submit_rule()
    assert not page.is_rule_created(rule_name)
    log_entries = page.get_audit_log_entries(rule_name)
    assert any('failed' in entry.lower() for entry in log_entries), 'Audit log should record failed creation'

@pytest.mark.performance
def test_rule_creation_performance(driver):
    page = RuleConfigurationPage(driver)
    rule_name = 'PerfTest'
    page.open_rule_creation()
    page.set_rule_name(rule_name)
    page.set_description('Performance test')
    page.add_trigger('Login')
    page.add_condition('UserRole', 'admin')
    page.add_action('Alert')
    page.start_performance_timer()
    page.submit_rule()
    elapsed = page.stop_performance_timer()
    assert elapsed < page.performance_threshold, f'Rule creation exceeded performance threshold: {elapsed}s'
    log_entries = page.get_audit_log_entries(rule_name)
    assert any('created' in entry.lower() for entry in log_entries), 'Audit log should record rule creation'