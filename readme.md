AWS Lambda SQS Translator

This Lambda function reads JSON messages from an Amazon SQS queue, each containing a "message" field. It uses the OpenAI API to translate these messages into simpler, clearer terms. After processing each batch of messages, it returns a JSON response indicating how many translations succeeded or failed.

Table of Contents

Overview
Architecture
Deployment
Configuration
Usage
Customizing the Translation Prompt
Future Database Integration

Overview

Purpose: Convert messages from SQS into simpler language using OpenAI’s GPT-3.5-turbo model.
Input: SQS records with a JSON body that includes a "message" field.
Output: Logs the translation result and returns a summary of how many messages were successfully processed versus failed.
Architecture

SQS: Receives messages to be processed by the Lambda function.

Lambda:

Reads batch of records from SQS.
Sends the "message" text to OpenAI to get a clearer translation.
(Optional) Could store results in a database if needed (code is commented out).
Returns a JSON result indicating success/failure counts.
OpenAI:

Provides the completion/translation using the GPT-3.5-turbo model.
Deployment

Clone or download this repository.

Install dependencies (if you plan to build the Lambda package locally):

bash
'''
pip install -r requirements.txt -t .
Zip the contents of the folder (including the Python files and dependencies) and upload to AWS Lambda, or deploy using a CI/CD pipeline of your choice (e.g., AWS SAM, Serverless Framework, Terraform).
'''
Configure the environment variables in your Lambda function:

OPENAI_API_KEY – Your OpenAI API key.
(Optional) DB_HOST, DB_SECRET_ARN – If you plan to connect to a database later on.
Connect the Lambda to your SQS queue by configuring the Event Source in AWS Lambda:

Specify the SQS queue ARN and the batch size (recommended: 10).
Configuration

Batch Size: In the code, batch_size is set to 10. You can adjust it based on performance needs:
'''
batch_size = 10
OpenAI Model: Currently set to "gpt-3.5-turbo" with temperature=0.0. Adjust if desired:


completion = self.client.chat.completions.create(
    model="gpt-3.5-turbo",
    ...
)
System Prompt: Located in self.system_prompt within the BatchPromptProcessor. Update to customize the translation style.
Usage

Once deployed and configured, the Lambda function will automatically be triggered for each batch of SQS messages. Each SQS message should have a JSON string in the "body", which itself must contain the key "message":
'''
{
  "message": "Your original text to be translated into simpler terms."
}
Example SQS Message

'''

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
When the Lambda processes these records, it will:

Parse the JSON in each record’s body.
Extract the "message" key’s value.
Send that text to the OpenAI API for simplification.
Log and return how many messages were successfully processed or failed.
Customizing the Translation Prompt

If you want to modify how messages are processed, see BatchPromptProcessor:

self.system_prompt: Defines the assistant’s context or style (e.g., “translate this message in simpler terms”).
{"role": "user", "content": f"Translate this message in simpler terms: {user_message}"}: The actual prompt sent to OpenAI. Feel free to adapt this question or command.
Future Database Integration

If you want to store translations in a database, there are commented-out sections in the code showing how to:

Create a database connection (get_db_connection and get_db_password).
Insert a record into example_table (insert_record).
You can uncomment these sections, install the necessary libraries (psycopg2, etc.), and adapt them to your database configuration.
