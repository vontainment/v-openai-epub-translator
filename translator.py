### translator.py
import os
import asyncio
import httpx
from dotenv import load_dotenv

# Load environment variables from a .env file into the program's environment.
load_dotenv()

# Grab the OpenAI API key and model from the environment; default to 'gpt-4' model if not specified.
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-4')

# If the API key isn't found in the environment, raise an error to prevent further execution.
if not OPENAI_API_KEY:
    raise ValueError("Missing environment variable: OPENAI_API_KEY")

# Define an asynchronous function for executing the translation request.
async def translate_text_async(text, target_language):
    # Informing the user about the translation process.
    print(f"Preparing to translate text to {target_language}.")

    # Input validation to ensure 'text' and 'target_language' parameters are not empty.
    if not text or not target_language:
        raise ValueError("Text or target language cannot be empty.")

    # Set the authorization headers required by the OpenAI API.
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }

    # Prepare the data to be sent in the API call, instructing the model on how to perform the translation.
    data = {
        "model": OPENAI_MODEL,  # The AI model used for translation is specified from the .env file
        "messages": [
            # System-level prompt providing guidelines for the translation style
            {"role": "system", "content": "You are an expert in literary translation. Rather than adhering to a literal, word-for-word translation, deeply consider the distinct cultural nuances, structural and syntactical variations, grammatical norms, idiomatic expressions, and cultural contexts of each language. Make appropriate adjustments to ensure these elements are accurately represented, while still preserving the original tone and intent of the text and maintaining the original HTML structure."},
            # User-level prompt including both the translation instructions and the text to be translated
            {"role": "user", "content": f"1. Translate the text from English to German with a focus on distinct cultural nuances, structural and syntactical variations, grammatical norms, idiomatic expressions, and cultural contexts of each language. 2. Maintain the original HTML structure. 3. Do not add comments surrounding the translation. 4. Ensure the translation reflects the spirit and context of the original text, beyond a literal word-for-word approach so the translation feels more natural: {text}"}
        ]
    }

    # Timeout configurations for the HTTP request.
    timeout = httpx.Timeout(300.0, connect=60.0)

    # The asynchronous context manager to manage the HTTP request lifecycle rules.
    async with httpx.AsyncClient(timeout=timeout) as client:
        for attempt in range(3):  # Try sending the request up to 3 times in case of failures.
            try:
                # Log the attempt and send the request to the OpenAI API with provided data.
                print(f"Attempt {attempt+1}: Sending translation request to OpenAI API with data: {data}")
                response = await client.post(
                    'https://api.openai.com/v1/chat/completions',
                    json=data,
                    headers=headers
                )
                response.raise_for_status()  # Raise an exception if response status is an error (4XX or 5XX).

                response_data = response.json()  # Convert the response to a JSON format for data extraction.
                print("Translation request successful.")

                break  # On successful request, exit from the retries loop.

            except Exception as e:
                # Log the error and retry unless this was the last attempt.
                print(f"An error occurred: {e}")
                if attempt == 2:
                    raise

    # Check for a valid response structure that contains translation results.
    if 'choices' in response_data and response_data['choices']:
        choice = response_data['choices'][0]

        # Extract the translated text from the response, if the expected fields are present.
        if 'message' in choice and 'content' in choice['message']:
            translated_text = choice['message']['content'].strip()
            print("Translation completed successfully.")
            print(response_data)  # Debugging line, consider removing for production code.
            return translated_text
    else:
        # Log and raise an error if the response does not match the expected format.
        print("Unexpected response from the API:")
        print(response_data)
        raise ValueError("The response from the API was not in the expected format.")
