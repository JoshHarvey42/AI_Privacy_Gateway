import re
import sys

NAMES = ["Sarah Johnson", "Michael Chen"]  # synthetic term list
PATTERNS = {                                # structured patterns
    "EMPID": re.compile(r"\bEMP\d+\b"),
    "TICKET": re.compile(r"\bIT-\d+\b"),
    "IP": re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"),
}
PROMPT_VERSION = "v1"
PROMPT_V1 = ("You summarize IT help desk tickets in one or two sentences. "
             "Keep every [[...]] placeholder exactly as written. "
             "Do not invent facts.")
TOKEN_RE = re.compile(r"\[\[(r\d+):([A-Z]+):(\d+)\]\]")  # one valid placeholder
FLAGS = {"--show-request", "--bad-provider", "--malformed-provider"}


class GatewayError(Exception):
    pass


def mask(text, rid):
    """Replace sensitive values with [[rid:CATEGORY:n]]; mapping stays local."""
    if TOKEN_RE.search(text):
        raise GatewayError("input contains reserved placeholder syntax")
    matches = [(m.start(), m.end(), "NAME") for n in NAMES
               for m in re.finditer(re.escape(n), text)]
    for cat, rx in PATTERNS.items():
        matches += [(m.start(), m.end(), cat) for m in rx.finditer(text)]
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


def prepare_request(text, rid):
    """Build the complete outbound request: the only thing the provider sees."""
    masked, mapping = mask(text, rid)
    request = {"prompt_version": PROMPT_VERSION,
               "prompt": PROMPT_V1,
               "text": masked}
    return request, mapping


def mock_provider(request, mode="normal"):
    """Offline, deterministic stand-in for the AI (ignores the prompt text)."""
    if mode == "invalid":
        return "Summary: [[r1:NAME:99]] reported an issue."
    if mode == "malformed":
        return "Summary: [[r1:NAME:1] reported an issue."
    masked = request["text"]
    t = {}
    for m in TOKEN_RE.finditer(masked):
        t.setdefault(m.group(2), m.group(0))
    who = t.get("NAME", "A user") + (f" ({t['EMPID']})" if "EMPID" in t else "")
    s = f"Summary: {who} reported an issue"
    if "TICKET" in t:
        s += f" in ticket {t['TICKET']}"
    if "IP" in t:
        s += f" on device {t['IP']}"
    details = re.split(r"(?<=[.!?])\s+", masked.strip())[-1]
    return f"{s}. Details: {details}"


def validate(response, rid, mapping):
    """Reject placeholders that are unissued, foreign, or malformed."""
    for m in TOKEN_RE.finditer(response):
        if m.group(1) != rid or m.group(0) not in mapping:
            raise GatewayError(f"invalid placeholder in response: {m.group(0)}")
    leftover = TOKEN_RE.sub("", response)
    if "[[" in leftover or "]]" in leftover:
        raise GatewayError("malformed placeholder in response")


def run(text, rid="r1", provider_mode="normal", show_request=False):
    request, mapping = prepare_request(text, rid)
    if show_request:
        print("OUTBOUND REQUEST:")
        for key, value in request.items():
            print(f"  {key}: {value}")
    response = mock_provider(request, provider_mode)
    validate(response, rid, mapping)
    return TOKEN_RE.sub(lambda m: mapping[m.group(0)], response)


if __name__ == "__main__":
    args = sys.argv[1:]
    flags = [a for a in args if a in FLAGS]
    text = " ".join(a for a in args if a not in FLAGS)
    mode = ("invalid" if "--bad-provider" in flags else
            "malformed" if "--malformed-provider" in flags else "normal")
    try:
        print(run(text, provider_mode=mode, show_request="--show-request" in flags))
    except GatewayError as e:
        print("ERROR:", e)
        sys.exit(1)
