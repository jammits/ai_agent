import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


def main():
    print("Hello from ai-agent!")
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    
    client = genai.Client(api_key=api_key)
   
    try:
        input = sys.argv[1]
        
        messages = [
            types.Content(role="user", parts=[types.Part(text=input)])
        ] 
        
        response = client.models.generate_content(
            model="gemini-2.0-flash-001", contents=messages
        )

        if len(sys.argv) == 3:
            option = sys.argv[2]
            print(f"User prompt: {input}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}") 
            
        print(response.text)
        
    except IndexError:
        sys.exit("No prompt given. Exiting program")

if __name__ == "__main__":
    main() 
