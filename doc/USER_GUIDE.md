# User Guide

## What it does

Takes the text of one IT support ticket, hides private values, gets a summary from an offline mock provider, and shows the summary with the private values restored.

## Run

Run from the project folder (the folder that contains main.py):

    python main.py "<insert ticket>"

Put the ticket text in quotes. Example:

    python main.py "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

To see exactly what is sent to the provider, put --show-request before the ticket:

    python main.py --show-request "<insert ticket>"

This prints the complete outbound request (prompt_version, prompt, and masked text) before the summary.

Each sensitive category uses `MASK` by default. To remove names instead of replacing them with placeholders:

    python main.py --policy=NAME=REMOVE "Sarah Johnson submitted ticket IT-5821."

To set more than one policy, repeat the option. Categories are `NAME`, `EMPID`, `TICKET`, and `IP`; policies are `MASK` and `REMOVE`. Invalid categories or policy values produce a controlled error.

To select the more detailed prompt:

    python main.py --prompt-v2 "Sarah Johnson submitted ticket IT-5821."

The default is prompt V1. Prompt V2 gives more specific instructions about the technician audience, required details, output labels, and placeholder handling.

## Supported formats

- Names: only names in the NAMES list at the top of main.py (add synthetic names there)
- Employee IDs: EMP followed by digits, such as EMP1042
- Ticket numbers: IT- followed by digits, such as IT-5821
- IP addresses: four numbers separated by dots, such as 192.168.1.25

## Warnings

- Use synthetic data only.
- A name that is not in the list is not masked.
- The mock provider is not a real AI. The summary wording is fixed by the program.
- Overlapping detections are resolved consistently by selecting the longest match first.
- Placeholder mappings exist only for the current request. Malformed, unknown, and foreign-request placeholders are rejected before restoration.
- Provider failures produce a controlled error. The gateway does not retry with the original, unmasked ticket.
- The offline mock ignores prompt wording, so selecting V2 does not demonstrate how a real AI model would respond.

## Troubleshooting

- ERROR: input contains reserved placeholder syntax: your text includes something like [[r1:NAME:1]]. Remove it.
- ERROR: invalid placeholder in response: the provider returned a placeholder that was not issued for this request. This is expected with --bad-provider.
- ERROR: malformed placeholder in response: the provider returned a damaged placeholder, such as one missing a bracket. This is expected with --malformed-provider.
- ERROR: invalid placeholder in response: the provider returned an unknown or foreign-request placeholder. This is expected with --bad-provider or --foreign-provider.
- ERROR: provider failure: the simulated provider failed. This is expected with --provider-failure.
- ERROR: invalid policy: check that the category is NAME, EMPID, TICKET, or IP and that the policy is MASK or REMOVE.
- A name was not hidden: add it to NAMES in main.py. Use --show-request to check what was sent.
- python not found: try python3 main.py "..."
- No such file main.py: you are in the wrong folder. Change to the project folder first.

The following flags simulate provider problems:

    python main.py --bad-provider "Sarah Johnson submitted ticket IT-5821."
    python main.py --malformed-provider "Sarah Johnson submitted ticket IT-5821."
    python main.py --foreign-provider "Sarah Johnson submitted ticket IT-5821."
    python main.py --provider-failure "Sarah Johnson submitted ticket IT-5821."

Run the automated tests with:

    python -m unittest -v
