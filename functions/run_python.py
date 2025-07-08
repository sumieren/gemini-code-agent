import os
import subprocess

def run_python_file(working_directory, file_path):
    full_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if os.path.commonpath([abs_working_directory, full_path]) != abs_working_directory:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.isfile(full_path):
        return f'Error: File "{file_path}" not found.'
    
    if not full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        captured_output = subprocess.run(["python3", file_path], timeout=30, capture_output=True, cwd=working_directory)

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



run_python_file("../calculator", "main.py")