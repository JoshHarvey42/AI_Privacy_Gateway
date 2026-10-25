# Evaluation

## Test Cases

- Normal input: Sensitive information is masked, the ticket is summarized, and valid values are restored.
- Repeated values: Repeated names and ticket numbers use the same placeholders and are restored correctly.
- No sensitive information: The ticket is summarized without masking.
- Invalid placeholder: A placeholder such as `[[r1:EMPLOYEE_ID:999]]` is rejected if it was never issued.
- Multiple values: Different sensitive values in one ticket receive the correct placeholders.
- Structured pattern: Example IP addresses are detected correctly.
- Mock provider: The same masked input produces a predictable response.

## Running Tests

Run the automated tests with the project's documented test command. Record the actual results after running them.

## Results

- Normal input: Record result.
- Repeated values: Record result.
- No sensitive information: Record result.
- Invalid placeholder: Record result.
- Multiple values and IP addresses: Record result.

## Limitations

The prototype only detects supported information types and uses an offline mock provider instead of a real AI service. It is not a complete privacy detector.
