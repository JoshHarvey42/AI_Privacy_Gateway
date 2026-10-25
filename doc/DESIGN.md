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

- String processing: Python has built-in regular expressions and simple string handling, so detection and replacement take few lines. Java needs more code for the same work.
- Type system: Java checks types at compile time and would catch some mistakes earlier. Python is dynamically typed, so errors such as passing the wrong type appear only when the code runs. I accept this because the program is small and unit tests cover the main paths.
- Error handling: Python exceptions (GatewayError) make controlled errors short to write. Java would work equally well but needs more setup.
- Deployment: Python runs directly with one command and no build step.

Choice: Python, because string processing and quick testing matter most for this task.

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
