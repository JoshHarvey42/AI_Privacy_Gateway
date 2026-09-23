# Design

## 1. Requirements

### User

The user of the system is an IT help desk technician.

### AI-Assisted Task

The system will use an AI provider to summarize IT help desk tickets.

The AI should produce a short summary of the user's technical problem and identify any requested action.

### Goal

The goal is to allow an IT help desk technician to use AI to summarize support tickets without sending selected sensitive information to the external AI provider.

Sensitive values should remain on the local machine. The AI should receive placeholders instead of the original values.

### Sensitive Information

The gateway will initially support four categories of sensitive information:

1. Employee names
2. Employee IDs
3. Ticket numbers
4. IP addresses

Employee names, employee IDs, and ticket numbers will use a local synthetic term list for exact matching.

IP addresses will use a documented structured pattern.

### Expected Output

The final output should be a useful ticket summary with authorized sensitive values restored.

For example, the original input could be:

Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi.

The masked request would be:

[[r1:NAME:1]] ([[r1:EMPLOYEE_ID:1]]) submitted ticket [[r1:TICKET:1]]. Her laptop cannot connect to Wi-Fi.

The final output could be:

Sarah Johnson (EMP1042) reported that her laptop cannot connect to Wi-Fi.

### Non-Goals

The project will not:

* Connect to a real help desk system.
* Use real employee, customer, or company records.
* Use real private information.
* Use a paid AI API.
* Provide a graphical user interface.
* Support multi-turn conversations.
* Store mappings between separate requests.
* Detect every possible type of sensitive information.
* Perform actual IT troubleshooting.

The project will remain a small, single-turn command-line system.

## 2. M2 Scope

The M2 prototype will implement the complete basic pipeline:

Input → Detection → Masking → Offline Mock Provider → Response Validation → Restoration → Output

The M2 implementation will include:

* Detection of the selected sensitive categories.
* Exact matching from a local synthetic term list.
* One documented structured pattern.
* Local masking.
* Request-local placeholder mappings.
* Repeated-value handling.
* An offline deterministic mock provider.
* Response validation.
* Local restoration.
* Automated versions of the M1 test cases.
* Controlled errors for invalid placeholders.

Full category coverage, MASK/REMOVE policy behavior, cross-request isolation, and prompt comparison will be addressed during later refinement.

## 3. Language Choice

### Selected Language: Python

Python will be used for the project.

The main reason is that the project is primarily concerned with text processing, pattern matching, mappings, and JSON-style data. Python provides straightforward tools for these operations and allows the gateway to remain relatively small.

### Alternative: Java

Java is a realistic alternative because it provides static typing and strong compile-time checking.

However, Java would generally require more code for the same string-processing and data-handling operations.

### Trade-Offs

#### String Processing

Python provides concise string-processing operations and regular expressions. Java can also handle these operations, but the implementation would generally be more verbose.

#### Type System

Python uses dynamic typing, which makes prototyping simpler but provides less compile-time checking. Java uses static typing, which can catch certain type-related errors before the program runs.

For this project, the simpler text-processing syntax of Python is useful because most of the gateway's work involves strings and structured placeholders.

## 4. Architecture

### Data Flow

The system will follow this flow:

User Input
→ Sensitive Data Detection
→ Policy
→ Local Masking
→ Offline/AI Provider
→ Response Validation
→ Local Restoration
→ Final Output

### Local/External Boundary

The following information stays local:

* The original ticket
* Detected sensitive values
* Placeholder mappings
* Detection rules
* Restoration logic
* Response validation

Only the masked request is allowed to cross the external boundary.

For example:

Original local input:

Sarah Johnson (EMP1042) submitted ticket IT-5821.

Masked request:

[[r1:NAME:1]] ([[r1:EMPLOYEE_ID:1]]) submitted ticket [[r1:TICKET:1]].

The external provider should not receive the original name, employee ID, or ticket number.

### Main Components

#### Detector

Finds supported sensitive information in the input.

#### Policy

Determines how each sensitive category should be handled.

The project will support MASK and REMOVE behavior as required during refinement.

#### Mapping

Stores the relationship between placeholders and original values for the current request.

#### Masker

Replaces sensitive values with placeholders before the request is sent to the provider.

#### Provider

Provides the AI-assisted response. During development, this will be a deterministic offline mock provider.

#### Validator

Checks the provider response for valid structure and valid placeholders.

#### Restorer

Replaces authorized placeholders with the original values.

## 5. Placeholder Format

The project will use request-specific placeholders in the following format:

[[request:category:number]]

Examples:

[[r1:NAME:1]]
[[r1:EMPLOYEE_ID:1]]
[[r1:TICKET:1]]
[[r1:IP:1]]

The request identifier separates mappings belonging to different requests.

The category identifies the type of protected value.

The final number identifies the occurrence within that request.

Repeated values within one request should use the same placeholder.

For example:

Sarah Johnson reported ticket IT-5821. Sarah Johnson asked for an update on IT-5821.

could become:

[[r1:NAME:1]] reported ticket [[r1:TICKET:1]]. [[r1:NAME:1]] asked for an update on [[r1:TICKET:1]].

A placeholder from another request must not be restored.

For example, a request using r1 must not restore [[r2:NAME:1]].

## 6. Initial Prompt

The initial prompt for the AI provider will be:

You are an IT help desk ticket summarization assistant.

Summarize the user's technical problem in 1–3 sentences.

Identify the main issue and any requested action.

Do not invent information.

Preserve all placeholders exactly as they appear.

The masked ticket will then be included with the prompt.

Example:

You are an IT help desk ticket summarization assistant.

Summarize the user's technical problem in 1–3 sentences.

Identify the main issue and any requested action.

Do not invent information.

Preserve all placeholders exactly as they appear.

Ticket:

[[r1:NAME:1]] ([[r1:EMPLOYEE_ID:1]]) reported ticket [[r1:TICKET:1]]. The laptop cannot connect to Wi-Fi.

## 7. State and Mapping

The mapping between placeholders and original sensitive values will exist only for the current request.

For example:

[[r1:NAME:1]] → Sarah Johnson
[[r1:EMPLOYEE_ID:1]] → EMP1042
[[r1:TICKET:1]] → IT-5821

The mapping will be used after the provider response is validated.

The mapping should be released after the request is completed so that values from one request cannot be restored during another request.

## 8. Initial Design Decisions

The project will use synthetic data instead of real employee information.

The project will use an offline mock provider so that the gateway can be tested without requiring a paid or live AI service.

The project will use a command-line interface rather than a graphical interface to keep the scope focused.

The project will use request-specific placeholders so that responses cannot use mappings from another request.

## 9. M4 Paradigm Comparison

This section will be completed during M4.

The final project will compare two programming paradigms in depth for one component and briefly assess the other relevant paradigms as required by the project handbook.
