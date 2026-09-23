# Design

## User

* IT help desk technician

## Task

* Summarize IT help desk tickets using AI.

## Goal

* Keep private information on the user's computer while still getting a useful summary.

## Sensitive Information

* Employee names
* Employee IDs
* Ticket numbers
* IP addresses

## Expected Output

* A short summary of the problem.
* Any requested action from the ticket.

## Non-Goals

* No real employee information
* No real help desk system
* No graphical interface
* No live AI service
* No multi-turn conversations

## How It Works

* The user enters a ticket.
* The program finds private information.
* The private information is replaced with placeholders.
* The ticket is sent to a mock AI.
* The response is checked.
* The original information is put back into the response.

## Language

* Python will be used.
* Java was considered as an alternative.
* Python was chosen because it makes working with text simpler.
* Java would provide more structure but would require more code.

## Basic Flow

* Input
* Find private information
* Replace private information
* Get AI response
* Check response
* Put information back
* Show final result

## Placeholder Examples

* [[r1:NAME:1]]
* [[r1:EMPLOYEE_ID:1]]
* [[r1:TICKET:1]]
* [[r1:IP:1]]

The placeholders allow the program to keep track of the original information.

## Initial Prompt

You are an IT help desk ticket summarization assistant.

Summarize the technical problem in 1–3 sentences. Identify the main issue and requested action. Do not invent information. Preserve all placeholders exactly as they appear.
