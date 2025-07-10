import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.write_file import schema_write_file, write_file
from functions.run_python import schema_run_python, run_python_file

# Define static variables: The system prompt and any available functions
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
available_functions = types.Tool(
    function_declarations=[
        schema_get_file_content,
        schema_get_files_info,
        schema_write_file,
        schema_run_python,
    ]
)

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

        
def generate_content(client, messages, verbose):
    # do a prompt, get a response and print it
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt)
    )

    if response.function_calls:
        for function_call_part in response.function_calls:
            call_result = call_function(function_call_part, verbose)
            if not call_result.parts[0].function_response.response:
                raise Exception("Function call did not return response")
            if verbose:
                print(f"-> {call_result.parts[0].function_response.response}")
    else:
        print(response.text)

    # keep track of used tokens in prompt and reponse
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

def call_function(function_call_part, verbose=False):
    function_dict = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")

    function_name = function_call_part.name
    function_call_part.args["working_directory"] = "./calculator"
    try:
        function_result = function_dict[function_name](**function_call_part.args)
    except:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


if __name__ == "__main__":
    main()