import os

import sys

import json

import traceback

from datetime import datetime



# If you plan to use a DB in the future, you can uncomment these:

# import psycopg2

# import boto3

# from botocore.config import Config

from openai import OpenAI



class BatchPromptProcessor:

    def __init__(self):

        """

        Initializes the processor with an OpenAI client and a system prompt 

        instructing it to translate incoming messages into clearer terms.

        """

        self.logger = print



        openai_api_key = os.environ.get('OPENAI_API_KEY')

        if not openai_api_key:

            raise ValueError("OpenAI API key not found in environment variables")



        self.client = OpenAI(api_key=openai_api_key)

        

        # System prompt for translating the message into clearer terms.

        self.system_prompt = (

            "You are an assistant that helps translate messages into simpler, clearer terms. "

            "Keep the translation concise and easy to understand."

        )



    def process_prompt(self, user_message):

        """

        Sends the user_message to the OpenAI API to get a translation in clearer terms.

        """

        try:

            completion = self.client.chat.completions.create(

                model="gpt-3.5-turbo",

                temperature=0.0,

                messages=[

                    {"role": "system", "content": self.system_prompt},

                    {"role": "user", "content": f"Translate this message in simpler terms: {user_message}"}

                ]

            )

            response = completion.choices[0].message.content

            self.logger(f"GPT response: {response}")

            return response

        except Exception as e:

            self.logger(f"Error processing prompt: {str(e)}")

            self.logger(f"Full error: {traceback.format_exc()}")

            raise



    """

    # Uncomment and adapt if you plan to use a database in the future:

    # def get_db_connection(self):

    #     ...

    #

    # def get_db_password(self):

    #     ...

    #

    # def insert_record(self, conn, record_id, translated_text):

    #     ...

    """



def handler(event, context):

    """

    AWS Lambda entry point.

    Expects 'Records' containing a JSON-serialized 'message' for each SQS record.

    Processes them in batches of 10 by default.

    """

    processed = {'success': 0, 'failed': 0}



    try:

        processor = BatchPromptProcessor()

        # conn = processor.get_db_connection()  # Uncomment if using DB

        

        if 'Records' not in event or not event['Records']:

            print("No records to process")

            return {

                'statusCode': 200,

                'body': json.dumps({'message': 'No records to process'})

            }



        batch_size = 10

        current_batch = []



        for record in event['Records']:

            try:

                # SQS message body is typically a JSON string we need to parse

                message = json.loads(record['body'])

                # We expect the actual text to be in the "message" key

                prompt_text = message.get('message')

                if not prompt_text:

                    raise ValueError("Missing 'message' in the SQS JSON body")



                current_batch.append(prompt_text)



                # Process the batch when it reaches batch_size

                if len(current_batch) >= batch_size:

                    process_batch(processor, current_batch, processed)

                    current_batch = []



            except Exception as record_error:

                processed['failed'] += 1

                print(f"Failed to process record: {str(record_error)}")

                continue



        # Process any leftovers if not empty

        if current_batch:

            process_batch(processor, current_batch, processed)



    except Exception as main_error:

        print(f"Main handler error: {str(main_error)}")

        return {

            'statusCode': 500,

            'body': json.dumps({

                'error': str(main_error),

                'processed': processed

            })

        }



    finally:

        """

        # If you were using DB connections, close them here:

        # if conn:

        #     try:

        #         conn.close()

        #         print("Database connection closed")

        #     except Exception as e:

        #         print(f"Error closing database connection: {str(e)}")

        """

    

    return {

        'statusCode': 200,

        'body': json.dumps({

            'message': 'Processing complete',

            'processed': processed

        })

    }
