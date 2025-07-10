import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory, directory=None):
    full_path = os.path.abspath(os.path.join(working_directory, directory))

    if not full_path.startswith(os.path.abspath(working_directory)):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(full_path):
        return f'Error: "{directory}" is not a directory'

    files = os.listdir(full_path)

    directory_label = "current" if directory == "." else f"'{directory}'"
    return_string = [f"Result for {directory_label} directory:"]
    for file in files:
        try:
            path = os.path.join(full_path, file)
            file_size = os.path.getsize(path)
            is_dir = os.path.isdir(path)

            return_string.append(f"- {file}: file_size={file_size} bytes, is_dir={is_dir}")
        except Exception as e:
            return f"Error: {e}"
        
    
    return "\n".join(return_string)