import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    if len(sys.argv) == 1:
        sys.exit("Include a prompt when using program. Format: python3 main.py <prompt> [--verbose]")
        
    prompt = sys.argv[1]
    verbose = "--verbose" in sys.argv

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]

    if verbose:
        print(f"User prompt: {prompt}")

    generate_content(client, messages, verbose)

        
def generate_content(client, messages,  verbose):
    # do a prompt, get a response and print it
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )

    print(response.text)

    # keep track of used tokens in prompt and reponse
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()