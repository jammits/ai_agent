import os

from functions.config import *

from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Prints a file's content up to the max defined characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file, relative to the working directory. If file path doesn't exist it creates it.",
            ),
        },
    ),
)

def get_file_content(working_directory, file_path):
    file_rel_path = os.path.join(working_directory,file_path)
    file_abs_path = os.path.abspath(file_rel_path)
    working_path = os.path.abspath(working_directory) 

    try:
        if not file_abs_path.startswith(working_path): 
            raise Exception()

        if not os.path.isfile(file_abs_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(file_abs_path,"r") as file:
            file_contents = file.read(MAX_CHARS)

            if os.path.getsize(file_abs_path) > MAX_CHARS:
                file_contents += f'[...File "{file_path}" trucated at {MAX_CHARS}]'

            return file_contents



    except Exception:
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

