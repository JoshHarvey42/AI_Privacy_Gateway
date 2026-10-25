"""AI Privacy Gateway - M2 prototype.
Pipeline: input -> detect -> mask -> mock provider -> validate -> restore -> output
Usage:  python gateway.py "Draft a reply to Evan Lane about case 1042."
        python gateway.py --bad-provider "..."   (mock returns an invalid placeholder)
"""
import re
import sys

NAMES = ["Evan Lane", "Maria Ortiz"]           # synthetic term list (NAME)
CASE_RE = re.compile(r"(?i:(?<=case ))\d{3,}")  # structured pattern (CASE)
TOKEN_RE = re.compile(r"\[\[(r\d+):([A-Z]+):(\d+)\]\]")

class GatewayError(Exception):
    pass


def mask(text, rid):
    """Replace sensitive values with [[rid:CATEGORY:n]]; mapping stays local."""
    if TOKEN_RE.search(text):
        raise GatewayError("input contains reserved placeholder syntax")
    matches = [(m.start(), m.end(), "NAME") for n in NAMES
               for m in re.finditer(re.escape(n), text)]
    matches += [(m.start(), m.end(), "CASE") for m in CASE_RE.finditer(text)]
    mapping, seen, counts, out, pos = {}, {}, {}, [], 0
    for start, end, cat in sorted(matches):
        if start < pos:                         # skip overlapping match
            continue
        value = text[start:end]
        if (cat, value) not in seen:            # repeated value -> same token
            counts[cat] = counts.get(cat, 0) + 1
            seen[(cat, value)] = f"[[{rid}:{cat}:{counts[cat]}]]"
            mapping[seen[(cat, value)]] = value
        out += [text[pos:start], seen[(cat, value)]]
        pos = end
    return "".join(out) + text[pos:], mapping


def mock_provider(masked, bad=False):
    """Offline, deterministic stand-in for the AI."""
    tokens = {m.group(2): m.group(0) for m in TOKEN_RE.finditer(masked)}
    if bad:
        return "Hello [[r1:NAME:99]], we received your request."
    greeting = f"Hello {tokens['NAME']}," if "NAME" in tokens else "Hello,"
    body = f"we received case {tokens['CASE']}." if "CASE" in tokens \
        else "we received your request."
    return f"{greeting} {body}"


def validate(response, rid, mapping):
    for m in TOKEN_RE.finditer(response):
        if m.group(1) != rid or m.group(0) not in mapping:
            raise GatewayError(f"invalid placeholder in response: {m.group(0)}")


def run(text, rid="r1", bad_provider=False):
    masked, mapping = mask(text, rid)           # mapping exists only in this call
    response = mock_provider(masked, bad_provider)
    validate(response, rid, mapping)
    return TOKEN_RE.sub(lambda m: mapping[m.group(0)], response)


if __name__ == "__main__":
    args = sys.argv[1:]
    bad = "--bad-provider" in args
    args = [a for a in args if a != "--bad-provider"]
    try:
        print(run(" ".join(args), bad_provider=bad))
    except GatewayError as e:
        print("ERROR:", e)
        sys.exit(1)