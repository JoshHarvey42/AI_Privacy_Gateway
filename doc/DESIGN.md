# Design

## User

- IT help desk technician.

## Task

- Summarize IT help desk tickets using AI.

## Goal

- Protect private information while allowing AI to produce a useful ticket summary.

## Sensitive Information

- Employee names
- Employee IDs
- Ticket numbers
- IP addresses

## Expected Output

- A short summary of the technical problem and any requested action.

## Language Comparison

Python was chosen for this project. Java was considered as an alternative.

- Text processing: Python has simple tools for finding and replacing text. Java can do this too, but usually requires more code. Python is a good fit because this project mainly works with text.
- Error handling: Python uses exceptions to handle problems, while Java also supports exceptions and has stricter type checking. Java's type checking can catch some mistakes before the program runs, but Python is simpler for building this small prototype.
- Testing: Python has a built-in testing option that is easy to use for automated tests. Java also supports automated testing, but commonly uses additional testing tools.

Python was selected because it allows the project to focus on the privacy process without requiring as much supporting code.

## How It Works

- The user enters a ticket.
- The program finds supported private information.
- Private information is replaced with placeholders.
- The masked ticket goes to an offline mock provider.
- The response is checked for invalid placeholders.
- Valid placeholders are replaced with their original values.
- The final summary is displayed.

## Local and External Boundary

The original ticket, private information, placeholder mappings, detection, validation, and restoration stay local.

The mock provider receives only the masked ticket. The prototype does not send information to a real AI service.

## Components

- Detector: Finds supported private information.
- Masker: Replaces private information with placeholders.
- Mapping: Keeps track of the original values for the current request.
- Mock provider: Produces a predictable summary without using an online AI service.
- Validator: Checks that the response does not contain invalid placeholders.
- Restorer: Replaces valid placeholders with their original values.

## Placeholder Format

- [[r1:NAME:1]]
- [[r1:EMPLOYEE_ID:1]]
- [[r1:TICKET:1]]
- [[r1:IP:1]]

Repeated values should use the same placeholder within a request. Different values should have separate placeholders.

## Initial Prompt

You are an IT help desk ticket summarization assistant.

Summarize the technical problem in 1–3 sentences. Identify the main issue and requested action. Do not invent information. Preserve all placeholders exactly as they appear.
