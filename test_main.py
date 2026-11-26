import unittest
from main import (
    GatewayError, NAMES, detect, resolve_overlaps, mask, prepare_request,
    mock_provider, validate, run,
)

TICKET = ("Sarah Johnson (EMP1042) submitted ticket IT-5821. "
          "Her laptop cannot connect to Wi-Fi.")


class Tests(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual(run(TICKET),
            "Summary: Sarah Johnson (EMP1042) reported an issue in ticket "
            "IT-5821. Details: Her laptop cannot connect to Wi-Fi.")

    def test_outbound_masked(self):
        masked, _ = mask(TICKET, "r1")
        self.assertEqual(masked,
            "[[r1:NAME:1]] ([[r1:EMPID:1]]) submitted ticket [[r1:TICKET:1]]. "
            "Her laptop cannot connect to Wi-Fi.")
        for secret in ("Sarah", "EMP1042", "IT-5821"):
            self.assertNotIn(secret, masked)

    def test_complete_outbound_request_has_no_protected_values(self):
        request, _ = prepare_request(TICKET, "r1")
        for field, value in request.items():
            for secret in ("Sarah", "Johnson", "EMP1042", "IT-5821"):
                self.assertNotIn(secret, value, f"{secret} leaked in {field}")

    def test_ip_address(self):
        masked, mapping = mask("Device 192.168.1.25 is offline.", "r1")
        self.assertEqual(masked, "Device [[r1:IP:1]] is offline.")
        self.assertEqual(mapping["[[r1:IP:1]]"], "192.168.1.25")

    def test_repeated_and_distinct(self):
        masked, mapping = mask(
            "Sarah Johnson called. Michael Chen helped Sarah Johnson.", "r1")
        self.assertEqual(masked,
            "[[r1:NAME:1]] called. [[r1:NAME:2]] helped [[r1:NAME:1]].")
        self.assertEqual(len(mapping), 2)

    def test_no_sensitive_data(self):
        self.assertEqual(run("The printer is jammed."),
            "Summary: A user reported an issue. Details: The printer is jammed.")

    def test_invalid_placeholder_response(self):
        with self.assertRaisesRegex(GatewayError, "invalid placeholder"):
            run(TICKET, provider_mode="invalid")

    def test_malformed_placeholders_rejected(self):
        mapping = {"[[r1:NAME:1]]": "Sarah Johnson"}
        for bad in ["Hi [[r1:NAME:]]", "Hi [[r1:name:1]]", "Hi [[r1:NAME:1]",
                    "Hi [[r1:NAME]]", "Hi [[NAME:1]]", "Hi r1:NAME:1]]",
                    "Hi [[r1:NAME:1]] and [[r1:NAME:x]]"]:
            with self.subTest(response=bad):
                with self.assertRaisesRegex(GatewayError, "malformed"):
                    validate(bad, "r1", mapping)

    def test_malformed_placeholder_from_provider(self):
        with self.assertRaisesRegex(GatewayError, "malformed"):
            run(TICKET, provider_mode="malformed")

    def test_reserved_placeholder_input(self):
        with self.assertRaisesRegex(GatewayError, "reserved"):
            run("Reset password for [[r1:NAME:1]].")

    def test_default_policy_is_mask(self):
        masked, mapping = mask(TICKET, "r1")
        self.assertIn("[[r1:NAME:1]]", masked)
        self.assertIn("Sarah Johnson", mapping.values())

    def test_remove_policy(self):
        masked, mapping = mask(
            "Sarah Johnson submitted ticket IT-5821.",
            "r1", {"NAME": "REMOVE"}
        )
        self.assertNotIn("Sarah Johnson", masked)
        self.assertNotIn("Sarah Johnson", mapping.values())
        self.assertIn("[[r1:TICKET:1]]", masked)

    def test_invalid_policy_rejected(self):
        with self.assertRaisesRegex(GatewayError, "invalid policy"):
            mask("Sarah Johnson called.", "r1", {"NAME": "KEEP"})

    def test_unknown_policy_category_rejected(self):
        with self.assertRaisesRegex(GatewayError, "invalid policy category"):
            mask("The printer is jammed.", "r1", {"UNKNOWN": "MASK"})

    def test_overlapping_matches_choose_longest(self):
        NAMES.append("Sarah Johnson EMP1042")
        try:
            matches = detect("Sarah Johnson EMP1042")
            chosen = resolve_overlaps(matches)
            self.assertEqual(len(chosen), 1)
            self.assertEqual(chosen[0][3], "Sarah Johnson EMP1042")
        finally:
            NAMES.pop()

    def test_independent_request_mappings(self):
        masked1, mapping1 = mask("Sarah Johnson called.", "r1")
        masked2, mapping2 = mask("Michael Chen called.", "r2")
        self.assertIn("[[r1:NAME:1]]", mapping1)
        self.assertIn("[[r2:NAME:1]]", mapping2)
        self.assertNotIn("[[r1:NAME:1]]", mapping2)
        self.assertNotEqual(masked1, masked2)

    def test_foreign_request_placeholder_rejected(self):
        mapping = {"[[r1:NAME:1]]": "Sarah Johnson"}
        with self.assertRaisesRegex(GatewayError, "invalid placeholder"):
            validate("Hi [[r2:NAME:1]]", "r1", mapping)

    def test_provider_failure_controlled(self):
        with self.assertRaisesRegex(GatewayError, "provider failure"):
            run(TICKET, provider_mode="failure")

    def test_provider_failure_does_not_use_unmasked_fallback(self):
        request, _ = prepare_request(TICKET, "r1")
        self.assertNotIn("Sarah Johnson", request["text"])
        self.assertNotIn("EMP1042", request["text"])
        with self.assertRaises(GatewayError):
            run(TICKET, provider_mode="failure")

    def test_prompt_versions_are_available(self):
        request1, _ = prepare_request(TICKET, "r1", prompt_version="v1")
        request2, _ = prepare_request(TICKET, "r2", prompt_version="v2")
        self.assertEqual(request1["prompt_version"], "v1")
        self.assertEqual(request2["prompt_version"], "v2")
        self.assertNotEqual(request1["prompt"], request2["prompt"])


if __name__ == "__main__":
    unittest.main()
