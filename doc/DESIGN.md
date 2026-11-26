# Design

## Problem and motivation

IT help desk tickets contain employee names, employee IDs, ticket numbers, and IP addresses. A cloud AI can summarize a ticket, but it does not need those identifiers. The goal is to keep them on the local machine while still getting a useful summary.

## User and task

- User: an IT help desk technician
- Task: summarize one support ticket
- Useful output: a short summary that names the right person, ticket, and device, and describes the problem, without inventing facts

## Sensitive categories

- NAME: employee names (example: Sarah Johnson)
- EMPID: employee IDs (example: EMP1042)
- TICKET: ticket numbers (example: IT-5821)
- IP: IP addresses (example: 192.168.1.25)

## Success criteria

- No protected value appears in the text sent to the provider
- Repeated values get the same placeholder; different values get different placeholders
- Valid placeholders in the response are restored correctly
- Invalid or reserved placeholders produce a controlled error, not a crash or a wrong restore

## Non-goals

- No graphical interface, real customer data, or paid AI access
- No multi-turn conversations
- No universal detector (unlisted names are not found)

## Scope by milestone

- M2 (this version): the full pipeline, four categories, request-local mappings, controlled errors, automated tests
- M3 (later): MASK/REMOVE policy, cross-request isolation, timeout and malformed-response simulation, prompt comparison

## Language choice: Python

Python was compared with Java.

- String processing: Python was chosen because the main purpose of the project is to identify and replace sensitive information in help desk tickets. Python provides simple string methods and the built-in re library, which makes it easy to detect patterns such as IPv4 addresses and replace sensitive values with placeholders. Java can accomplish the same tasks, but Python requires less code to implement them.
- Error handling: * Error handling: Python was chosen because its exceptions make it simple to handle errors during input processing and response validation. For example, mask() rejects input that already contains placeholder syntax, and validate() rejects invalid, unknown, or malformed placeholders in the provider response. Both raise GatewayError, and the main block catches it, prints an ERROR line, and exits with code 1, so the program fails in a controlled way instead of crashing. Java also provides strong error handling through exceptions, but its checked exceptions must be declared and handled in each method, so Python requires less code to implement these checks.

## Data flow and boundary

    LOCAL                                          EXTERNAL (mock)
    input text
      -> detect sensitive values
      -> mask (placeholders + local mapping)
      -> [ prompt + masked text ] ----------------> mock provider
                                    <---------------- response
      -> validate placeholders
      -> restore from local mapping
      -> final output

Stays local: original text, the mapping from placeholder to real value, the final output.
May be sent: the versioned prompt and the masked text only.
Checked before restoring: every placeholder in the response must belong to this request and exist in the mapping.

## Components (all in main.py)

- mask(): finds sensitive values, builds placeholders and the local mapping, rejects input that already contains placeholder syntax
- mock_provider(): offline, deterministic stand-in for the AI
- validate(): checks response placeholders
- run(): connects the steps; the mapping is a local variable, so it is released when the function returns
- main block: reads the command line, prints output or an error

## Placeholder form

[[r1:NAME:1]]: request id, category, number within that category and request. The same value in one request always gets the same placeholder. The request id lets a later milestone reject placeholders from another request.

## Prompt

    You summarize IT help desk tickets in one or two sentences.
    Keep every [[...]] placeholder exactly as written. Do not invent facts.

The prompt is stored as PROMPT in main.py and passed to the provider with the masked text. The offline mock ignores the prompt text, so M2 tests check gateway behavior only, not prompt quality.

## Design decisions

- Mapping is local to one function call: simplest way to guarantee no state is shared between requests.
- Overlapping matches: sort by start position and skip any match that begins inside an earlier one. Simple and deterministic.
- Input containing placeholder-like text is rejected, so a user cannot forge a placeholder the gateway would later restore.
- Plain text input and output: there is no shared JSON contract, so the simplest interface was chosen.
- Errors use one exception class (GatewayError) and exit code 1.
