# User Guide

## What it does

Takes the text of one IT support ticket, hides private values, gets a summary from an offline mock provider, and shows the summary with the private values restored.

## Run

    python main.py "<insert ticket>"

Put the ticket text in quotes. Example:

    python main.py "Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi."

## Supported formats

- Names: only names in the NAMES list at the top of main.py (add synthetic names there)
- Employee IDs: EMP followed by digits, such as EMP1042
- Ticket numbers: IT- followed by digits, such as IT-5821
- IP addresses: four numbers separated by dots, such as 192.168.1.25

## Warnings

- Use synthetic data only.
- A name that is not in the list is not masked.
- The mock provider is not a real AI. The summary wording is fixed by the program.

## Troubleshooting

- ERROR: input contains reserved placeholder syntax: your text includes something like [[r1:NAME:1]]. Remove it.
- ERROR: invalid placeholder in response: the provider returned a placeholder that was not issued for this request. This is expected with --bad-provider.
- A name was not hidden: add it to NAMES in main.py.
- python not found: try python3 main.py "..."
