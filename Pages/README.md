# Pages Directory Documentation

## Overview
This directory contains Page Object classes for Selenium-based UI automation of Example E-Commerce. Each class represents a distinct page and encapsulates UI elements and actions, mapped to locators from Locators.json.

## PageClasses
- LoginPage.py: Handles login operations and validations.
- ProfilePage.py: Handles user profile actions.
- SettingsPage.py: Handles settings menu interactions.
- RuleManagementPage.py: Handles rule creation, update, and validation for triggers/actions (specific_date, recurring, fixed_amount, percentage_of_deposit).
- TransactionPage.py: Handles transaction operations related to rules.

## Implementation Guide
1. **Add new PageClass**: Place new .py files in Pages directory. Ensure imports and methods match test case requirements.
2. **Update existing PageClass**: Append new methods, preserving existing logic and structure.
3. **Locators**: Map all UI elements to Locators.json. Update as needed for new triggers/actions.
4. **Code Integrity**: Strict adherence to method signatures, docstrings, and exception handling.

## QA Report
- All PageClasses validated for structure and locator mapping.
- Methods tested for trigger/action flows (specific_date, recurring, fixed_amount, percentage_of_deposit).
- Code reviewed for integrity, maintainability, and downstream compatibility.
- No breaking changes to existing logic.

## Troubleshooting
- If locators change, update Locators.json and PageClasses accordingly.
- For new triggers/actions, extend RuleManagementPage and TransactionPage.
- Ensure WebDriverWait and EC conditions match UI response times.

## Future Considerations
- Expand RuleManagementPage for additional triggers/actions.
- Add Transaction validation and reporting methods.
- Integrate with CI/CD for automated PageClass updates.
- Enhance documentation for new PageClasses.
