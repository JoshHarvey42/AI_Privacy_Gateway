# Assistance

Each entry: what was suggested, what I decided, and how I checked it.

## 1. Planning: pipeline and placeholder form (M1)

- Suggestion: build the pipeline as detect, mask, mock provider, validate, restore, and use placeholders like [[r1:NAME:1]] with the request id inside.
- Decision: accepted.
- Check: traced the handbook example by hand, then ran the example ticket and compared the masked text and final output with my expected values.

## 2. Code: first version of main.py (M2)

- Suggestion: a single-file program using regular expressions and a term list, with the mapping kept as a local variable in run().
- Decision: accepted, after simplifying it (removed JSON input/output, extra error codes, and command-line options other than --bad-provider) because the course has no shared JSON contract.
- Check: ran the program on the example ticket, and ran the 7 unit tests.

## 3. Tests (M2)

- Suggestion: tests for the four M1 cases plus an IP case, an exact check of the masked text, and a reserved-placeholder input case.
- Decision: accepted.
- Check: all 7 tests pass; confirmed manually that the masked text contains no protected values.

## 4. Documentation (M2)

- Suggestion: README and the four docs files drafted from the handbook requirements.
- Decision: accepted with edits to match the real program (names list, exact output text).
- Check: ran every command in the README and compared the output to the text written there.

## Tech Spike (M1)

- Runtime: Python 3.15.1
- Command: echo "Sarah Johnson (EMP1042) submitted ticket IT-5821." | python -c "import sys; print(sys.stdin.read().strip())"
- Input: Sarah Johnson (EMP1042) submitted ticket IT-5821.
- Observed output: Sarah Johnson (EMP1042) submitted ticket IT-5821.

## Other sources

- Python standard library documentation (re, unittest, sys)
