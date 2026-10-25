# IT Help Desk Privacy Gateway

This project helps IT help desk technicians summarize support tickets while protecting private information. The program replaces sensitive values before sending text to an offline mock provider, checks the response, and restores valid values locally.

## Requirements

- Python 3

## Run

- Run the program with `python main.py`.
- Run the tests with `python -m unittest`.

These commands assume the program and tests use these entry points.

## Example

Input:

Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi.

Expected output:

A short summary of the Wi-Fi problem with the original information restored.

## Supported Information

- Employee names
- Employee IDs
- Ticket numbers
- IP addresses

## Testing

The tests cover normal input, repeated values, input without sensitive information, and invalid placeholders.

Use synthetic data only. The prototype does not use a real AI service.
