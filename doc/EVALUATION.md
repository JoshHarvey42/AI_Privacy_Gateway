# Evaluation

## Test 1: Normal Input

Input:

Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi.

Expected:

- Private information is replaced with placeholders.
- The mock provider summarizes the ticket.
- Valid placeholders are restored.

## Test 2: Repeated Information

Input:

Sarah Johnson submitted ticket IT-5821. Sarah Johnson wants an update on IT-5821.

Expected:

- Repeated values use the same placeholders.
- The original values are restored correctly.

## Test 3: No Private Information

Input:

The laptop cannot connect to Wi-Fi.

Expected:

- No information is masked.
- The ticket is summarized normally.

## Test 4: Invalid Placeholder

Example invalid placeholder:

[[r1:EMPLOYEE_ID:999]]

Expected:

- The validator detects that the placeholder was not issued for the request.
- The program returns a controlled error.
- The invalid placeholder is not restored.

## Results

Results will be recorded after running the automated tests.

## Limitations

- The program only detects the supported types of private information.
- The mock provider does not use a real AI service.
