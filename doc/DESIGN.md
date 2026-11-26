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

- No protected value appears anywhere in the complete outbound request (prompt included)
- Repeated values get the same placeholder; different values get different placeholders
- Valid placeholders in the response are restored correctly
- Invalid, malformed, or reserved placeholders produce a controlled error, not a crash or a wrong restore

## Non-goals

- No graphical interface, real customer data, or paid AI access
- No multi-turn conversations
- No universal detector (unlisted names are not found)

## Scope by milestone

- M2: the initial full pipeline, four categories, request-local mappings, controlled errors, and automated tests
- M3: MASK/REMOVE policy, deterministic overlap handling, independent request mappings, provider-failure handling, expanded tests, and prompt comparison

## Language choice: Python

Python was compared with Java.

* String processing: Python was chosen because the main purpose of the project is to identify and replace sensitive information in help desk tickets. Python provides simple string methods and the built-in re library, which makes it easy to detect patterns such as IPv4 addresses and replace sensitive values with placeholders. Java can accomplish the same tasks, but Python requires less code to implement them.
* Error handling: Python was chosen because its exceptions make it simple to handle errors during input processing and response validation. For example, mask() rejects input that already contains placeholder syntax, and validate() rejects invalid, unknown, or malformed placeholders in the provider response. Both raise GatewayError, and the main block catches it, prints an ERROR line, and exits with code 1, so the program fails in a controlled way instead of crashing. Java also provides strong error handling through exceptions, but its checked exceptions must be declared and handled in each method, so Python requires less code to implement these checks.

## Data flow and boundary

    LOCAL                                          EXTERNAL (mock)
    input text
      -> detect sensitive values
      -> apply MASK/REMOVE policy
      -> mask (placeholders + local mapping)
      -> [ prompt + masked text ] ----------------> mock provider
                                    <---------------- response
      -> validate placeholders
      -> restore from local mapping
      -> final output

Stays local: original text, the mapping from placeholder to real value, the final output. The mapping and repeated-value lookup are created for one request only and are released when `run` returns or raises an error. 
May be sent: the complete outbound request only, which has three fields: prompt_version, prompt (the versioned prompt), and text (the masked text). Run with --show-request to print it.
Checked before restoring: every placeholder in the response must be well formed, belong to this request, and exist in the mapping. Invalid, unknown, malformed, and foreign-request placeholders are rejected. Provider failures return a controlled error and never trigger an unmasked retry.

## Components (all in main.py)

- detect(): finds sensitive values and returns their start, end, category, and value
- resolve_overlaps(): selects non-overlapping matches in a consistent order, preferring the longest match at the same starting position
- apply_policies(): validates category policies and applies `MASK` by default or `REMOVE` when selected
- build_mapping(): replaces selected values and builds the request-local placeholder mapping
- mask(): coordinates detection, overlap resolution, policy application, and mapping; rejects input that already contains placeholder syntax
- prepare_request(): builds the complete outbound request (prompt_version, prompt, and masked text)
- mock_provider(): offline, deterministic stand-in for the AI
- validate(): rejects invalid, malformed, unknown, and foreign-request placeholders in the response
- run(): connects the steps; the mapping is a local variable, so it is released when the function returns
- main block: reads the command line and policy flags, prints output or a controlled error

The implementation uses strings for ticket text and provider responses, tuples `(start, end, category, value)` for detected spans, and dictionaries for policies, outbound requests, and placeholder mappings. The outbound request has `prompt_version`, `prompt`, and `text` fields. `prepare_request()` returns that request together with the mapping; `run()` passes the request to the provider and passes the mapping only to validation and restoration. The mapping is local state and is not shared between calls.

## Placeholder form

[[r1:NAME:1]]: request id, category, number within that category and request. The same value in one request always gets the same placeholder. The request id lets the validator reject placeholders from another request. Each request has its own mapping; repeated occurrences of the same category and value reuse a placeholder within that request.

A response is also rejected as malformed if, after all valid placeholders are removed, [[ or ]] is still left (for example [[r1:NAME:]] or [[r1:NAME:1]).

## Prompt
    You summarize IT help desk tickets in one or two sentences.
    Keep every [[...]] placeholder exactly as written. Do not invent facts.

    You summarize an IT help desk ticket for a technician. Return a Summary and Details section. Include the reported issue and relevant device or ticket details when present. Keep every [[...]] placeholder exactly as written. Do not invent facts.

The prompt is stored as `PROMPT_V1` in main.py (version v1) and is part of the complete outbound request. `PROMPT_V2` gives more specific instructions about the technician audience, the information to include, the Summary and Details format, and preserving placeholders. The same three synthetic cases were run with both versions. The offline mock ignores prompt wording, so identical mock outputs do not establish real-model prompt quality.

## Design decisions

- Mapping is local to one function call: simplest way to guarantee no state is shared between requests.
- Overlapping matches: sort by start position and then longest match first; skip any match that overlaps an already selected match. Simple and deterministic.
- Policies: use `MASK` by default for NAME, EMPID, TICKET, and IP. A category can use `REMOVE`; invalid policy values and unknown categories raise `GatewayError`.
- Provider boundary: `mock_provider()` receives only the prepared request, not the original ticket or mapping. Provider failures become controlled errors, with no unmasked fallback.
- Input containing placeholder-like text is rejected, so a user cannot forge a placeholder the gateway would later restore.
- Malformed placeholders in the response are rejected instead of left in the output.
- The outbound request is built in one function (prepare_request) and can be printed with --show-request.
- Errors use one exception class (GatewayError) and exit code 1.
