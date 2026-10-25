import unittest
from main import run, mask, GatewayError

class Tests(unittest.TestCase):
    def test_ordinary(self):
        self.assertEqual(run("Draft a reply to Evan Lane about case 1042."),
                         "Hello Evan Lane, we received case 1042.")

    def test_outbound_masked(self):
        masked, _ = mask("Draft a reply to Evan Lane about case 1042.", "r7")
        self.assertEqual(masked,
            "Draft a reply to [[r7:NAME:1]] about case [[r7:CASE:1]].")

    def test_repeated_and_distinct(self):
        masked, mapping = mask("Evan Lane, Evan Lane and Maria Ortiz.", "r1")
        self.assertEqual(masked,
            "[[r1:NAME:1]], [[r1:NAME:1]] and [[r1:NAME:2]].")
        self.assertEqual(len(mapping), 2)

    def test_no_sensitive_data(self):
        self.assertEqual(run("Write a thank-you note."),
                         "Hello, we received your request.")

    def test_invalid_placeholder_response(self):
        with self.assertRaises(GatewayError):
            run("Reply to Evan Lane about case 1042.", bad_provider=True)

    def test_reserved_placeholder_input(self):
        with self.assertRaises(GatewayError):
            run("Reply to [[r1:NAME:1]].")

if __name__ == "__main__":
    unittest.main()