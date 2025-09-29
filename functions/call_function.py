import os   
from google import genai
from google.genai import types
from .get_files_info import get_files_info
from .get_file_content import get_file_content
from .run_python_file import run_python_file
from .write_file import write_file




def call_function(function_call_part, verbose=False):
    functions_dict = {}
    functions_dict["get_files_info"] = get_files_info
    functions_dict["get_file_content"] = get_file_content
    functions_dict["run_python_file"] = run_python_file
    functions_dict["write_file"] = write_file

    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    
    else:
        print(f" - Calling function: {function_call_part.name}")
     
    func = functions_dict.get(function_call_part.name)
    func_name = function_call_part.name
    if func is None:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )

    kwargs = dict(function_call_part.args or {})
    kwargs["working_directory"] = "./calculator"

    function_result = func(**kwargs)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result},
            )
        ],
    )


