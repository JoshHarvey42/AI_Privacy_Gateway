# IT Help Desk Privacy Gateway

Milestone M2 (working prototype).

The program helps an IT help desk technician summarize a support ticket with an AI tool without sending private values. It finds sensitive values, replaces them with placeholders locally, sends only the masked text to an offline mock provider, checks the response, and puts the original values back locally.

## Scope

- User: IT help desk technician
- Task: summarize one support ticket
- Sensitive categories: employee names, employee IDs, ticket numbers, IP addresses
- Detection: term list for names, patterns for IDs, tickets, and IPs
- Single request at a time, command line only, synthetic data only
- Offline mock provider (no real AI, no network, no API keys)

Pipeline: input -> detect -> mask -> mock provider -> validate -> restore -> output

Placeholder form: [[r1:NAME:1]] (request id, category, number). The mapping from placeholder to real value exists only inside one request.

## Setup

Python 3.15.1

## Run

Run all commands from the project folder (the folder that contains main.py).

    python main.py "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

Expected output:

    Summary: Sarah Johnson (EMP1042) reported an issue in ticket IT-5821. Details: Her laptop cannot connect to Wi-Fi.

Show the complete outbound request (everything the provider receives):

    python main.py --show-request "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

Expected output:

    OUTBOUND REQUEST:
      prompt_version: v1
      prompt: You summarize IT help desk tickets in one or two sentences. Keep every [[...]] placeholder exactly as written. Do not invent facts.
      text: [[r1:NAME:1]] ([[r1:EMPID:1]]) submitted ticket [[r1:TICKET:1]]. Her laptop cannot connect to Wi-Fi.
    Summary: Sarah Johnson (EMP1042) reported an issue in ticket IT-5821. Details: Her laptop cannot connect to Wi-Fi.

Invalid placeholder from the provider (the mock is told to misbehave):

    python main.py --bad-provider "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

Expected output (exit code 1):

    ERROR: invalid placeholder in response: [[r1:NAME:99]]

Malformed placeholder from the provider (the mock returns [[r1:NAME:1] with a missing bracket):

    python main.py --malformed-provider "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

Expected output (exit code 1):

    ERROR: malformed placeholder in response

## Test

    python -m unittest -v

Expected: Ran 10 tests ... OK

## Files

- main.py: the gateway
- test_main.py: automated tests
- tech_spike.py: M1 Tech Spike (reads and echoes text)
- docs/DESIGN.md: requirements, language choice, architecture, prompt, decisions
- docs/USER_GUIDE.md: how to run, formats, warnings, troubleshooting
- docs/EVALUATION.md: planned and executed cases, results, limitations
- docs/ASSISTANCE.md: AI help and how it was checked

## Data

Synthetic data only. Do not enter real employee or ticket information.
