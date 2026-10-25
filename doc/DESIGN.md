# Design

## User and Task

The user is an IT help desk technician who needs short summaries of support tickets.

## Goal

Protect private information while allowing an AI-style provider to summarize a ticket.

## Sensitive Information

- Employee names, employee IDs, and ticket numbers are detected using a local list of synthetic examples.
- IP addresses are detected using a regular expression.

## Language Choice

Python was chosen over Java because it requires less code for text processing and is straightforward to test. Java offers stricter type checking, which can catch some mistakes earlier, but requires more structure. Python is a better fit for this small text-processing project.

## How It Works

- Read the ticket and detect supported private information.
- Replace detected values with placeholders.
- Save the original values in a mapping for the current request.
- Send the masked ticket to the offline mock provider.
- Validate the response.
- Restore valid placeholders and display the result.

## Local and External Boundary

The original ticket, sensitive values, placeholder mappings, detection, validation, and restoration stay local. The mock provider receives only the masked ticket. No real AI service is used.

## Components

- Detector: Finds supported private information.
- Masker: Replaces detected values with placeholders.
- Mapping: Keeps track of original values for the request.
- Mock provider: Produces a predictable response without an online service.
- Validator: Checks for invalid placeholders.
- Restorer: Replaces valid placeholders with their original values.

## Placeholders

Examples: `[[r1:NAME:1]]`, `[[r1:EMPLOYEE_ID:1]]`, `[[r1:TICKET:1]]`, and `[[r1:IP:1]]`.

Repeated values use the same placeholder within a request. Different values receive different placeholders.

## Initial Prompt

You are an IT help desk ticket summarization assistant. Summarize the technical problem in 1–3 sentences, identify the main issue and requested action, do not invent information, and preserve all placeholders exactly.

## M2 Scope

The prototype implements the full input, detection, masking, mock provider, validation, restoration, and output process. It includes repeated values, multiple sensitive values in one request, and controlled errors for invalid placeholders.

MASK/REMOVE policies, real AI services, a graphical interface, and multi-turn conversations are outside the M2 scope.
