# Evaluation

All results below come from the offline mock provider and synthetic fixtures. No real model was used.

## Planned acceptance cases (M1)

1. Ordinary input: "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."
2. Repeated values: "Sarah Johnson called. Michael Chen helped Sarah Johnson."
3. No sensitive data: "The printer is jammed."
4. Invalid placeholder response: case 1 input with the mock returning [[r1:NAME:99]]

Extra case added in M2: "Device 192.168.1.25 is offline." (IP address)

## Executed tests (python -m unittest -v, 7 tests, all pass)

- test_ordinary: summary with original values restored
- test_outbound_masked: masked text exactly as expected, and Sarah, EMP1042, IT-5821 not present
- test_ip_address: IP masked
- test_repeated_and_distinct: repeated name shares one placeholder, second name gets NAME:2
- test_no_sensitive_data: summary produced, nothing masked
- test_invalid_placeholder_response: controlled error raised
- test_reserved_placeholder_input: controlled error raised

## Detection counts (labeled cases above)

Protected-value occurrences: ordinary 3, repeated 3, none 0, invalid-placeholder case 3, IP 1.

- TP: 10
- FP: 0
- FN: 0
- Precision: 10/10 = 1.00
- Recall: 10/10 = 1.00
- Leaks in outbound text: 0

These numbers are on five small hand-made cases, so they show the rules work on those cases, not that detection is reliable in general.

## Invalid tokens and restoration

- Invalid placeholder in response: rejected before restoration, no output produced
- Valid placeholders: restored correctly in cases 1, 2, and 5
- REMOVE is not implemented yet

## Usefulness of output

The mock builds the summary from a fixed template and the last sentence of the ticket, so it shows that placeholders survive the round trip. It does not show how useful a real AI summary would be. Prompt usefulness is not evaluated yet

## Limitations

- Names must be in the term list; an unlisted name is a false negative (not yet tested)
- IP pattern accepts numbers above 255
- Only one request is run at a time; cross-request isolation is not tested yet
- No provider timeout or malformed-response tests yet
- Only exact-case matches: "sarah johnson" would not be found
