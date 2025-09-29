import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    
    client = genai.Client(api_key=api_key)
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    try:
        verbose = False
        limit = 0
        input = sys.argv[1]
        
        messages = [
            types.Content(role="user", parts=[types.Part(text=input)])
        ] 

        available_functions = types.Tool(
            function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,

            ]
        )

        while limit < 20:

            response = client.models.generate_content(
                model="gemini-2.0-flash-001", 
                contents=messages,
                config = types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

            if len(sys.argv) == 3:
                option = sys.argv[2]
                verbose = True
                print(f"User prompt: {input}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
       

            for candidate in response.candidates:
                messages.append(candidate.content)


            if response.function_calls:
                for call in response.function_calls:

                    call_response = call_function(call, verbose)


                    if call_response.parts[0].function_response.response is None:
                        raise RuntimeError("Function call failed; No response.")

                    if verbose:
                        print(f"-> {call_response.parts[0].function_response.response}")
               
                    messages.append(
                        types.Content(
                            role = "user",
                            parts =[types.Part(text=str(call_response.parts[0].function_response.response))]
                        )
                    )
                limit += 1
                continue

            if response.text:
                print(response.text)
                break

            limit += 1
 
           
    except RuntimeError as e:
        sys.exit(e)

    except IndexError:
        sys.exit("No prompt given. Exiting program")

if __name__ == "__main__":
    main() 
