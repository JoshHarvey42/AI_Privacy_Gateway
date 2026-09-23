# Design

## User

IT help desk technician.

## Task

Use AI to summarize an IT help desk ticket.

## Goal

Keep sensitive information local while still allowing AI to produce a useful ticket summary.

## Sensitive Information

* Employee names
* Employee IDs
* Ticket numbers
* IP addresses

## Expected Output

A short summary of the IT problem and any requested action.

## Non-Goals

* No real employee data
* No real help desk system
* No graphical interface
* No multi-turn conversations
* No live AI service

## M2 Scope

The system will:

1. Read a ticket.
2. Detect sensitive information.
3. Replace sensitive information with placeholders.
4. Send the masked ticket to a mock AI provider.
5. Check the response.
6. Restore the original values.

## Language

Python will be used.

Java is the alternative.

Python makes string processing and pattern matching simpler. Java provides stronger static type checking but generally requires more code.

## Data Flow

```text
Input
  ↓
Detect
  ↓
Mask
  ↓
AI Provider
  ↓
Validate
  ↓
Restore
  ↓
Output
```

The original sensitive information and mappings stay local. Only the masked request is sent to the provider.

## Components

* Detector
* Masker
* Mapping
* Mock Provider
* Validator
* Restorer

## Placeholder Format

```text
[[r1:NAME:1]]
[[r1:EMPLOYEE_ID:1]]
[[r1:TICKET:1]]
[[r1:IP:1]]
```

The request ID keeps mappings separate between requests.

## Initial Prompt

You are an IT help desk ticket summarization assistant.

Summarize the technical problem in 1–3 sentences. Identify the main issue and requested action. Do not invent information. Preserve all placeholders exactly as they appear.
