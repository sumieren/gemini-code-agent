import os
import subprocess
from google.genai import types

schema_run_python = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs the Python code in a given file, constrained to the working directory. Responds with stdout, stderr and an exit code where applicable.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="The arguments passed to the function call.",
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if os.path.commonpath([abs_working_directory, full_path]) != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    commands = ["python3", file_path]
    if args:
        commands.extend(args)

    try:
        captured_output = subprocess.run(commands, timeout=30, capture_output=True, cwd=working_directory)

        stdout = captured_output.stdout.decode()
        stderr = captured_output.stderr.decode()
        exit_code = captured_output.returncode

        output_string = []

        if stdout:
            output_string.append(f"STDOUT: {stdout}")
        if stderr:
            output_string.append(f"STDERR: {stderr}")
        if exit_code != 0:
            output_string.append(f"Process exited with code {exit_code}")
        
        if not output_string:
            return "No output produced."

        return "\n".join(output_string)

    except Exception as e:
        return f"Error: executing Python file: {e}"