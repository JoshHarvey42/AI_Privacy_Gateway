# Assistance

Each entry: what was suggested, what I decided, and how I checked it.

## 1. Rejecting placeholder-like input

- Suggestion: Rejecting any inputs that try to forge a placeholder
- Decision: Made a test case to check for forged placeholders.
- Check: Ran `python main.py "Reset password for [[r1:NAME:1]]."` and got `ERROR: input contains reserved placeholder syntax` with exit code 1. test_reserved_placeholder_input also passes.

## 2. Code: first version of main.py

- Suggestion: How to format the program
- Decision: Kept all the code in two files.
- Check: Ran the example ticket and got `Summary: Sarah Johnson (EMP1042) reported an issue in ticket IT-5821. Details: Her laptop cannot connect to Wi-Fi.` Ran it with --bad-provider and got `ERROR: invalid placeholder in response: [[r1:NAME:99]]` with exit code 1.

## 3. Tests

- Suggestion: What test cases to check.
- Decision: Included each test case and manually checked to make sure they work.
- Check: Ran `python -m unittest -v` and confirmed `Ran 10 tests ... OK`. For the masking test, compared the masked text with `[[r1:NAME:1]] ([[r1:EMPID:1]]) submitted ticket [[r1:TICKET:1]]. Her laptop cannot connect to Wi-Fi.` and confirmed Sarah, EMP1042, and IT-5821 do not appear in it.

## 4. Documentation

- Suggestion: Ways to format the documents.
- Decision: Changed the formatting of the documents with some edits.
- Check: Ran every command in the README and compared each output with the expected text written there. Confirmed every file listed under Files exists in the project.

## Tech Spike

- Runtime: Python 3.15.1
- Command: `python tech_spike.py`
- Input: `testing`
- Output: `Output: testing`

## Other sources

- Python standard library documentation (re, unittest, sys)
