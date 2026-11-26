import re
import sys

NAMES = ["Sarah Johnson", "Michael Chen"]  # synthetic term list
PATTERNS = {
    "EMPID": re.compile(r"\bEMP\d+\b"),
    "TICKET": re.compile(r"\bIT-\d+\b"),
    "IP": re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b"),
}
CATEGORIES = {"NAME", "EMPID", "TICKET", "IP"}
PROMPTS = {
    "v1": ("You summarize IT help desk tickets in one or two sentences. "
           "Keep every [[...]] placeholder exactly as written. Do not invent facts."),
    "v2": ("You summarize an IT help desk ticket for a technician. "
           "Return a Summary and Details section. Include the reported issue "
           "and relevant device or ticket details when present. "
           "Keep every [[...]] placeholder exactly as written. Do not invent facts."),
}
TOKEN_RE = re.compile(r"\[\[([A-Za-z0-9_-]+):([A-Z]+):(\d+)\]\]")

class GatewayError(Exception):
    pass

def detect(text):
    matches = [(m.start(), m.end(), "NAME", m.group())
               for name in NAMES
               for m in re.finditer(re.escape(name), text)]
    for category, pattern in PATTERNS.items():
        matches += [(m.start(), m.end(), category, m.group())
                    for m in pattern.finditer(text)]
    return matches

def resolve_overlaps(matches):
    selected = []
    for match in sorted(matches, key=lambda m: (m[0], -(m[1] - m[0]), m[2])):
        if not selected or match[0] >= selected[-1][1]:
            selected.append(match)
    return selected

def apply_policies(matches, policies=None):
    policies = policies or {}
    result = []
    for category, policy in policies.items():
        if category not in CATEGORIES:
            raise GatewayError(f"invalid policy category: {category}")
        if not isinstance(policy, str) or policy.upper() not in ("MASK", "REMOVE"):
            raise GatewayError(f"invalid policy for {category}: {policy}")

    for start, end, category, value in resolve_overlaps(matches):
        result.append((start, end, category, value,
                       policies.get(category, "MASK").upper()))
    return result

def build_mapping(text, matches, rid):
    mapping, seen, counts = {}, {}, {}
    output, position = [], 0
    for start, end, category, value, policy in matches:
        output.append(text[position:start])
        if policy == "REMOVE":
            replacement = ""
        else:
            key = (category, value)
            if key not in seen:
                counts[category] = counts.get(category, 0) + 1
                token = f"[[{rid}:{category}:{counts[category]}]]"
                seen[key] = token
                mapping[token] = value
            replacement = seen[key]
        output.append(replacement)
        position = end
    output.append(text[position:])
    return "".join(output), mapping

def mask(text, rid, policies=None):
    if "[[" in text or "]]" in text:
        raise GatewayError("input contains reserved placeholder syntax")
    matches = apply_policies(detect(text), policies)
    return build_mapping(text, matches, rid)

def prepare_request(text, rid, policies=None, prompt_version="v1"):
    if prompt_version not in PROMPTS:
        raise GatewayError(f"invalid prompt version: {prompt_version}")
    masked, mapping = mask(text, rid, policies)
    request = {"prompt_version": prompt_version,
               "prompt": PROMPTS[prompt_version],
               "text": masked}
    return request, mapping

def mock_provider(request, mode="normal", rid="r1"):
    if mode == "failure":
        raise GatewayError("provider failure")
    if mode == "invalid":
        return f"Summary: [[{rid}:NAME:99]] reported an issue."
    if mode == "foreign":
        return "Summary: [[foreign:NAME:1]] reported an issue."
    if mode == "malformed":
        return f"Summary: [[{rid}:NAME:1] reported an issue."

    tokens = {}
    for match in TOKEN_RE.finditer(request["text"]):
        tokens.setdefault(match.group(2), match.group())
    who = tokens.get("NAME", "A user")
    if "EMPID" in tokens:
        who += f" ({tokens['EMPID']})"
    summary = f"Summary: {who} reported an issue"
    if "TICKET" in tokens:
        summary += f" in ticket {tokens['TICKET']}"
    if "IP" in tokens:
        summary += f" on device {tokens['IP']}"
    details = re.split(r"(?<=[.!?])\s+", request["text"].strip())[-1]
    return f"{summary}. Details: {details}"

def validate(response, rid, mapping):
    if not isinstance(response, str):
        raise GatewayError("malformed provider response")
    for match in TOKEN_RE.finditer(response):
        if match.group(1) != rid or match.group() not in mapping:
            raise GatewayError(f"invalid placeholder in response: {match.group()}")
    remaining = TOKEN_RE.sub("", response)
    if "[[" in remaining or "]]" in remaining:
        raise GatewayError("malformed placeholder in response")

def restore(response, mapping):
    return TOKEN_RE.sub(lambda match: mapping[match.group()], response)

def run(text, rid="r1", provider_mode="normal", show_request=False,
        policies=None, prompt_version="v1"):
    request, mapping = prepare_request(text, rid, policies, prompt_version)
    if show_request:
        print("OUTBOUND REQUEST:")
        for key, value in request.items():
            print(f"  {key}: {value}")
    try:
        response = mock_provider(request, provider_mode, rid)
    except GatewayError:
        raise
    except Exception:
        raise GatewayError("provider failure") from None
    validate(response, rid, mapping)
    return restore(response, mapping)

def main(args):
    policies = {}
    text = []
    mode = "normal"
    prompt_version = "v1"
    show_request = False

    for arg in args:
        if arg == "--show-request":
            show_request = True
        elif arg == "--bad-provider":
            mode = "invalid"
        elif arg == "--malformed-provider":
            mode = "malformed"
        elif arg == "--foreign-provider":
            mode = "foreign"
        elif arg == "--provider-failure":
            mode = "failure"
        elif arg == "--prompt-v2":
            prompt_version = "v2"
        elif arg.startswith("--policy="):
            setting = arg[len("--policy="):]
            if "=" not in setting:
                raise GatewayError("policy must use CATEGORY=MASK or CATEGORY=REMOVE")
            category, policy = setting.split("=", 1)
            policies[category.upper()] = policy.upper()
        else:
            text.append(arg)

    print(run(" ".join(text), provider_mode=mode, show_request=show_request,
              policies=policies, prompt_version=prompt_version))

if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except GatewayError as error:
        print("ERROR:", error)
        sys.exit(1)
