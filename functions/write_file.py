import os

from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Takes a file path in the working directory to a file then writes the content to it, constrained to the working directory. If file doesn't exists it creates it",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to be written in, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING  ,
                description="The actual text that will be written to the file.",
            ),
        },
    ),
)

def write_file(working_directory, file_path, content):
    file_rel_path = os.path.join(working_directory,file_path)
    file_abs_path = os.path.abspath(file_rel_path)
    working_path = os.path.abspath(working_directory)

    try:
        if not file_abs_path.startswith(working_path):
            raise Exception()
        
        if not os.path.exists(file_abs_path):
            parent = os.path.dirname(file_abs_path)
            os.makedirs(parent, exist_ok=True)
            


        with open(file_abs_path, "w") as file:
            file.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'


    

    except FileExistsError:
        return f'Error: Target directory already exists.'
    except Exception:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

