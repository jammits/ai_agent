import os
import subprocess

from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Takes a file path in the working directory to a python file and runs it along with any provided arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to a python file to be run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="A list of arguements that can be provided alongside the file path.",
                items=types.Schema(type=types.Type.STRING)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    file_rel_path = os.path.join(working_directory,file_path)
    file_abs_path = os.path.abspath(file_rel_path)
    working_abs_path = os.path.abspath(working_directory)

    try:

        if not file_abs_path.startswith(working_abs_path):
            raise PermissionError()
    
        if not os.path.exists(file_abs_path):
            raise FileExistsError()
        
        head, tail = os.path.split(file_abs_path)

        if not tail.endswith(".py"):
            raise FileNotFoundError()

        completed_process = subprocess.run(["python3",f"{tail}"] + list(map(str,args)),cwd=working_abs_path ,capture_output=True,timeout=30,text=True)

        output = completed_process.stdout
        error_out = completed_process.stderr
        exit_str = completed_process.returncode

        result = f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

        if not output and not error_out:
            return "No output produced."
        
        if exit_str != 0:
            result += f"\nProcess exited with code {exit_str}"

        return result

            
        


    except FileNotFoundError:
        return f'Error: "{file_path}" is not a Python file.'

    except FileExistsError:
        return f'Error: File "{file_path}" not found.'

    except PermissionError:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    except Exception as e:
       return f"Error: executing Python file: {e}"
