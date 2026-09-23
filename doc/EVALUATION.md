# Evaluation

## Test 1: Normal Input

Input:

Sarah Johnson (EMP1042) submitted ticket IT-5821. Her laptop cannot connect to Wi-Fi.

Expected:

* The private information is hidden.
* The ticket is summarized.
* The original information is put back.

## Test 2: Repeated Information

Input:

Sarah Johnson submitted ticket IT-5821. Sarah Johnson wants an update on IT-5821.

Expected:

* Repeated information is handled correctly.
* The original information is put back correctly.

## Test 3: No Private Information

Input:

The laptop cannot connect to Wi-Fi.

Expected:

* Nothing is hidden.
* The ticket is summarized normally.

## Test 4: Invalid Information

Expected:

* The program recognizes the problem.
* The program returns an error.
* The invalid information is not put back into the response.

## Results

* Results will be added after testing.

## Limitations

* The program only protects the types of information listed in the project.
