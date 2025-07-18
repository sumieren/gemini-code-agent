import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Shows the text content of a file, constrained to the working directory. If the file is longer than 10000 characters, will truncate to 10000 and append a message.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'


    with open(full_path, "r") as f:
        try:
            file_content_string = f.read(10001)
            if len(file_content_string) > 10000:
                file_content_string = file_content_string[:10000]
                file_content_string += f'[...File "{file_path}" truncated at 10000 characters]'
        except Exception as e:
            return f"Error: {e}"
    
    return file_content_string