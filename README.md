# IT Help Desk Privacy Gateway

This project helps IT help desk technicians summarize support tickets while protecting private information. The program replaces sensitive values locally before sending text to an offline mock provider, checks the provider's response, and restores valid values locally.

**Milestone:** M2 (working prototype). Single-turn, command-line, synthetic data only.

## Requirements

- Python 3.8 or newer
- No third-party packages and no network access

## How It Works

```
ticket text -> detect -> mask -> offline mock provider -> validate -> restore -> summary
```

1. **Detect** sensitive values using an exact-match term list (employee names) and documented patterns (employee IDs, ticket numbers, IP addresses).
2. **Mask** each value with a request-local placeholder of the form `[[<request_id>:<CATEGORY>:<n>]]`, for example `[[r1:NAME:1]]`. The mapping from placeholder to original value stays in memory for that request only.
3. **Mock provider** receives only the masked text and returns a deterministic summary. It makes no network calls.
4. **Validate** that every placeholder in the response was issued for this request.
5. **Restore** the original values locally and print the final summary.

Repeated values reuse the same placeholder. Different values in the same category get different numbers (`NAME:1`, `NAME:2`).

## Run

- Run the program: `python main.py "<ticket text>"`
- Run the tests: `python -m unittest -v`

## Example

Command:

```
python main.py "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."
```

Text sent to the mock provider (masked):

```
[[r1:NAME:1]] ([[r1:EMPID:1]]) submitted ticket [[r1:TICKET:1]]. Her laptop cannot connect to Wi-Fi.
```

Expected output (original values restored locally):

```
Summary: Sarah Johnson (EMP1042) reported ticket IT-5821: laptop cannot connect to Wi-Fi.
```

The wording comes from the deterministic mock provider; the original name, ID, and ticket number appear only in the final output.

### Error example

If the provider returns a placeholder that was not issued for this request, the program prints a controlled error and exits with code 1 instead of restoring anything:

```
ERROR: invalid placeholder in response: [[r1:NAME:99]]
```

Input that already contains reserved placeholder syntax (such as `[[r1:NAME:1]]`) is also rejected with an error.

## Supported Information

| Category | Placeholder | Detection method |
|---|---|---|
| Employee names | `NAME` | Exact match from a local synthetic term list |
| Employee IDs | `EMPID` | Pattern: `EMP` followed by digits (e.g., `EMP1042`) |
| Ticket numbers | `TICKET` | Pattern: `IT-` followed by digits (e.g., `IT-5821`) |
| IP addresses | `IP` | Pattern: four dot-separated numbers (e.g., `192.168.1.25`) |

## Testing

The automated tests cover:

- Normal input with several sensitive values
- Repeated values (same placeholder) and different values (different placeholders)
- Input with no sensitive information
- An invalid placeholder in the provider response
- Input containing reserved placeholder syntax

Tests use the offline mock provider only, so they report gateway behavior, not real-model quality.

## Limitations (M2)

- Names are only detected if they appear in the local term list; unlisted names are not masked.
- The IP pattern is simple and does not check that each number is 0-255.
- One request at a time; no conversation history.
- Not yet implemented (planned for M3): MASK/REMOVE policy, cross-request isolation tests, provider timeout simulation, and prompt comparison.

## Data

Use synthetic data only. Do not enter real employee or ticket information. The prototype does not use a real AI service or API keys.
