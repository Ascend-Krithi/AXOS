# TC-FT-008: SQL Injection Rejection

## Steps
1. Attempt to upload a rule containing SQL injection.
2. Verify that the rule is rejected and error message is displayed.
3. Attempt batch upload with SQL injection rules.
4. Verify that all SQL injection rules are rejected.

## Expected Results
- SQL injection rules are not accepted.
- Error message is displayed for each rejection.
