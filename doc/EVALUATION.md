# Evaluation

All results below come from the offline mock provider and synthetic fixtures. No real model was used.

## Planned acceptance cases

1. Ordinary input: "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."
2. Repeated values: "Sarah Johnson called. Michael Chen helped Sarah Johnson."
3. No sensitive data: "The printer is jammed."
4. Invalid placeholder response: case 1 input with the mock returning [[r1:NAME:99]]

## Executed tests (python -m unittest -v, 20 tests, all pass)

- test_ordinary: summary with original values restored
- test_outbound_masked: masked text exactly as expected, and Sarah, EMP1042, IT-5821 not present
- test_complete_outbound_request_has_no_protected_values: the request has exactly the fields prompt_version, prompt, and text, and none of Sarah, Johnson, EMP1042, or IT-5821 appears in any field
- test_ip_address: IP masked
- test_repeated_and_distinct: repeated name shares one placeholder, second name gets NAME:2
- test_no_sensitive_data: summary produced, nothing masked
- test_invalid_placeholder_response: controlled error raised
- test_malformed_placeholders_rejected: seven malformed responses each raise "malformed", including [[r1:NAME:]], [[r1:name:1]], and [[r1:NAME:1]
- test_malformed_placeholder_from_provider: full run with the mock returning a malformed placeholder raises "malformed"
- test_reserved_placeholder_input: controlled error raised
- test_default_policy_is_mask and test_remove_policy: default masking and explicit removal work
- test_invalid_policy_rejected and test_unknown_policy_category_rejected: invalid settings produce controlled errors
- test_overlapping_matches_choose_longest: overlap selection is deterministic
- test_independent_request_mappings: mappings remain separate between requests
- test_foreign_request_placeholder_rejected: a token from another request is rejected
- test_provider_failure_controlled and test_provider_failure_does_not_use_unmasked_fallback: provider failure is safe
- test_prompt_versions_are_available: both prompt versions can be selected
- test_default_policy_is_mask and test_remove_policy: default masking and explicit removal work
- test_invalid_policy_rejected and test_unknown_policy_category_rejected: invalid settings produce controlled errors
- test_overlapping_matches_choose_longest: overlap selection is deterministic
- test_independent_request_mappings: mappings remain separate between requests
- test_foreign_request_placeholder_rejected: a token from another request is rejected
- test_provider_failure_controlled and test_provider_failure_does_not_use_unmasked_fallback: provider failure is safe
- test_prompt_versions_are_available: both prompt versions can be selected

## Detection counts (labeled cases above)

The three synthetic cases used for the prompt comparison contain five protected-value occurrences: Sarah Johnson, EMP1042, and IT-5821 (3); Michael Chen and 192.168.1.25 (2); and a printer issue with no protected values (0).

- TP: 5
- FP: 0
- FN: 0
- Precision: 5 / (5 + 0) = 1.00
- Recall: 5 / (5 + 0) = 1.00
- Leaks in the outbound request: 0

These numbers are from three small synthetic cases and do not establish general detection accuracy. The name detector still depends on the configured name list.

## Invalid tokens and restoration

- Invalid placeholder in response: rejected before restoration, no output produced
- Malformed placeholder in response: rejected before restoration, no output produced
- Valid placeholders: restored correctly in cases 1, 2, and 5
- Valid `MASK` placeholders are restored correctly. Values selected for `REMOVE` are deleted before the provider receives the request.

## Usefulness of output

The mock builds the summary from a fixed template and the last sentence of the ticket, so it shows that placeholders survive the round trip. It does not show how useful a real AI summary would be. Prompt usefulness is compared through the prompt instructions, but the mock provider cannot measure real-model prompt quality.

## Limitations

- Names must be in the term list; an unlisted name is a false negative (not yet tested)
- IP pattern accepts numbers above 255
- The command-line program processes one ticket per run; request mappings are kept separate and are not shared between calls
- Provider failures are simulated, but real network timeouts are not tested
- The malformed check rejects leftover `[[` or `]]` syntax; it does not attempt to identify every possible stray single bracket
- Only exact-case matches: "sarah johnson" would not be found
