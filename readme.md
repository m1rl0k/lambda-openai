# AWS Lambda SQS Translator

This Lambda function reads JSON messages from an Amazon SQS queue, each containing a `message` field. It uses the OpenAI API to translate these messages into simpler, clearer terms. After processing each batch of messages, it returns a JSON response indicating how many translations succeeded or failed.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Usage](#usage)
- [Customizing the Translation Prompt](#customizing-the-translation-prompt)
- [Future Database Integration](#future-database-integration)

---

## Overview

**Purpose:** Convert messages from SQS into simpler language using OpenAI’s GPT-3.5-turbo model.  
**Input:** SQS records with a JSON body that includes a `message` field.  
**Output:** Logs the translation result and returns a summary of how many messages were successfully processed versus failed.

---

## Architecture

- **Amazon SQS**: Receives messages to be processed by the Lambda function.

- **AWS Lambda**:
  - Reads a batch of records from SQS.
  - Sends the `message` text to OpenAI to get a clearer translation.
  - (Optional) Stores results in a database if needed (code is commented out).
  - Returns a JSON result indicating success/failure counts.

- **OpenAI API**:
  - Provides the translation using the GPT-3.5-turbo model.

---

## Deployment

1. **Clone or download this repository.**

2. **Install dependencies** (if building the Lambda package locally):
   ```bash
   pip install -r requirements.txt -t .

	3.	Zip the contents of the folder (Python files and dependencies), then upload to AWS Lambda, or deploy using a CI/CD tool (e.g., AWS SAM, Serverless Framework, Terraform).
	4.	Configure environment variables in your Lambda function:
	•	OPENAI_API_KEY: Your OpenAI API key.
	•	(Optional) DB_HOST, DB_SECRET_ARN: If connecting to a database later.
	5.	Connect the Lambda to your SQS queue:
	•	Configure the event source with the SQS queue ARN.
	•	Set the batch size (recommended: 10).

Configuration

Batch Size

In the code, the batch size is set to 10. You can adjust this based on performance:

batch_size = 10

OpenAI Model

Currently set to gpt-3.5-turbo with a temperature=0.0. You can modify this in the code:

completion = self.client.chat.completions.create(
    model="gpt-3.5-turbo",
    ...
)

System Prompt

The system prompt is located in self.system_prompt within the BatchPromptProcessor. Update it to customize the translation style.

Usage

Once deployed and configured, the Lambda function will automatically process batches of SQS messages. Each SQS message should have a JSON string in the body, which itself must contain the key message.

Example SQS Message

{
  "Records": [
    {
      "body": "{\"message\":\"It is with great pleasure that I announce my departure.\"}"
    },
    {
      "body": "{\"message\":\"Ensure all code is merged to main before EOD.\"}"
    }
  ]
}

Process Flow
	1.	The Lambda function parses the JSON in each record’s body.
	2.	It extracts the value of the message key.
	3.	It sends the text to the OpenAI API for simplification.
	4.	Logs and returns how many messages were successfully processed or failed.

Customizing the Translation Prompt

To modify how messages are translated, update the BatchPromptProcessor:
	•	System Prompt: Defines the assistant’s context or style.

self.system_prompt = "Translate messages into simpler terms."


	•	User Prompt: The actual question sent to OpenAI:

{"role": "user", "content": f"Translate this message in simpler terms: {user_message}"}



Feel free to adapt these prompts to your needs.

Future Database Integration

To store translations in a database:
	•	Uncomment the relevant sections in the code:
	•	get_db_connection and get_db_password: For database connection.
	•	insert_record: For inserting records into the database.
	•	Install necessary libraries (e.g., psycopg2) and configure them for your database.

Example of inserting into a table (example_table):

insert_record(db_connection, "example_table", translation_result)

You can adapt these snippets to your specific database setup.
