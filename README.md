# AWS Lambda SQS Translator

A serverless function that leverages OpenAI's GPT-3.5-turbo to translate SQS messages into simpler, clearer language.

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Deployment](#deployment)
- [Configuration](#configuration)
- [Usage](#usage)
- [Message Format](#message-format)
- [Customization](#customization)
- [Database Integration](#database-integration)
- [Contributing](#contributing)
- [License](#license)

## Use Cases

### API Message Translation & Storage
This solution is perfect for scenarios where you need to process, simplify, or enhance API-generated messages before storing them. Common use cases include:

1. **Customer Support Integration**
   ```json
   // Original SQS Message from API
   {
     "ticket_id": "T123",
     "customer_message": "Unable to access the platform despite multiple attempts with correct credentials",
     "timestamp": "2024-01-07T10:30:00Z"
   }
   
   // AI-Translated and Stored in Database
   {
     "ticket_id": "T123",
     "original_message": "Unable to access the platform despite multiple attempts with correct credentials",
     "translated_message": "Customer can't log in even with the right password",
     "sentiment": "frustrated",
     "category": "login_issues",
     "timestamp": "2024-01-07T10:30:00Z"
   }
   ```

2. **Technical Log Processing**
   ```json
   // Original SQS Message from API
   {
     "log_id": "L456",
     "error_message": "NullPointerException in UserAuthenticationService.validateToken() at line 234",
     "severity": "ERROR"
   }
   
   // AI-Translated and Stored in Database
   {
     "log_id": "L456",
     "original_message": "NullPointerException in UserAuthenticationService.validateToken() at line 234",
     "translated_message": "Authentication failed because the user's login token was missing",
     "recommended_action": "Check if token is being properly passed in the request header",
     "severity": "ERROR"
   }
   ```

3. **Sales Data Enhancement**
   ```json
   // Original SQS Message from API
   {
     "sale_id": "S789",
     "notes": "Cust req spec conf w/ 3yr maint plan + custom impl",
     "value": "50000"
   }
   
   // AI-Translated and Stored in Database
   {
     "sale_id": "S789",
     "original_notes": "Cust req spec conf w/ 3yr maint plan + custom impl",
     "translated_notes": "Customer requested special configuration with a 3-year maintenance plan and custom implementation",
     "key_requirements": ["special_config", "maintenance_plan", "custom_implementation"],
     "contract_duration": "3 years",
     "value": "50000"
   }
   ```

### Benefits
- Transforms cryptic API messages into clear, actionable information
- Enriches data with AI-generated insights and categorizations
- Maintains original message while adding translated/enhanced versions
- Enables better reporting and analysis through structured data
- Automates the process of message interpretation and categorization

## Overview

The AWS Lambda SQS Translator is a serverless application that:
- Processes JSON messages from an Amazon SQS queue
- Translates message content into simpler language using OpenAI's GPT-3.5-turbo
- Provides batch processing capabilities
- Returns detailed processing statistics
- Supports optional database integration for persistent storage

### Key Features
- Automated message simplification
- Batch processing support
- Configurable OpenAI parameters
- Extensible architecture
- Comprehensive error handling
- Optional database integration

## Architecture

### Components
- **Amazon SQS**: Message queue service that triggers the Lambda function
- **AWS Lambda**: Serverless compute service that processes the messages
- **OpenAI API**: Natural language processing service for message translation
- **Optional Database**: Storage for processed messages (implementation ready)

### Flow
1. Messages arrive in SQS queue
2. Lambda function is triggered automatically
3. Messages are processed in configurable batches
4. OpenAI API translates each message
5. Results are logged and summarized
6. Optional database storage of translations

## Prerequisites

- AWS Account with appropriate permissions
- OpenAI API key
- Python 3.8 or higher
- AWS CLI (for local development)
- Git (for version control)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/aws-lambda-sqs-translator.git
cd aws-lambda-sqs-translator
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt -t .
```

## Deployment

### Manual Deployment
1. Zip the contents of the project directory:
```bash
zip -r function.zip .
```

2. Upload to AWS Lambda:
```bash
aws lambda update-function-code --function-name YourFunctionName --zip-file fileb://function.zip
```

### Using Infrastructure as Code
Sample AWS SAM template:
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Resources:
  TranslatorFunction:
    Type: AWS::Serverless::Function
    Properties:
      Handler: app.lambda_handler
      Runtime: python3.8
      Timeout: 30
      MemorySize: 256
      Environment:
        Variables:
          OPENAI_API_KEY: '{{resolve:secretsmanager:OpenAIAPIKey:SecretString:key}}'
```

## Configuration

### Environment Variables
- `OPENAI_API_KEY`: Your OpenAI API key
- `BATCH_SIZE`: Number of messages to process in each batch (default: 10)
- `DB_HOST`: Database host (optional)
- `DB_SECRET_ARN`: AWS Secrets Manager ARN for database credentials (optional)

### OpenAI Parameters
```python
OPENAI_CONFIG = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.0,
    "max_tokens": 150
}
```

## Usage

### Message Format
Input SQS message body:
```json
{
  "message": "Your original text to be translated into simpler terms."
}
```

### Batch Processing Example
```json
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
```

### Response Format
```json
{
  "processed": 2,
  "succeeded": 2,
  "failed": 0,
  "errors": []
}
```

## Customization

### Translation Prompt
Modify the system prompt in `BatchPromptProcessor`:
```python
self.system_prompt = """
You are a helpful assistant that translates messages into simpler terms.
Please maintain the original meaning while making the language more accessible.
"""
```

### Batch Size
Adjust the batch size in the Lambda configuration or environment variables:
```python
batch_size = int(os.getenv('BATCH_SIZE', '10'))
```

## Database Integration

To enable database storage:

1. Uncomment the database code sections
2. Install required database dependencies:
```bash
pip install psycopg2-binary -t .
```

3. Configure database environment variables:
```bash
DB_HOST=your-database-host
DB_SECRET_ARN=arn:aws:secretsmanager:region:account:secret:name
```

4. Create the necessary database table:
```sql
CREATE TABLE translations (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    translated_text TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
