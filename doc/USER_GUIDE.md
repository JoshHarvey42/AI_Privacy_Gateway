# User Guide

## Requirements

Python 3 is required. Use synthetic data only.

## Running the Program

- Start the program with the documented run command.
- Enter an IT help desk ticket.
- The program masks supported private information, processes the masked ticket with the offline mock provider, checks the response, and restores valid values.

## Example Input

Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi at 192.168.1.25.

## Supported Information

- Employee names
- Employee IDs
- Ticket numbers
- IP addresses

Names, IDs, and ticket numbers must match the local synthetic term list. IP addresses are detected by a pattern.

## Output and Errors

The program displays a short ticket summary with valid placeholders restored. If the response contains an invalid or unknown placeholder, the program returns a controlled error instead of restoring it.

## JSON Input and Output

The program follows the shared course JSON I/O contract. Document the required input fields, output fields, and error format here using the exact contract supplied for the project.
