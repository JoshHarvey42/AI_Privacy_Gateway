import unittest
from main import run, mask, prepare_request, validate, GatewayError

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
        self.assertEqual(set(request), {"prompt_version", "prompt", "text"})
        for field, value in request.items():      # every field, prompt included
            for secret in ("Sarah", "Johnson", "EMP1042", "IT-5821"):
                self.assertNotIn(secret, value, f"{secret} leaked in {field}")

    def test_ip_address(self):
        masked, _ = mask("Device 192.168.1.25 is offline.", "r1")
        self.assertEqual(masked, "Device [[r1:IP:1]] is offline.")

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

if __name__ == "__main__":
    unittest.main()
