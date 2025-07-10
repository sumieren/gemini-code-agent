import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes text to a given file path, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    dir_path = os.path.dirname(full_path)

    if not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except Exception as e:
            return f"Error creating directory: {e}"
        
    try:
        with open(full_path, "w") as f:
            f.write(content)

            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
            return f"Error writing to file: {e}"
        
   