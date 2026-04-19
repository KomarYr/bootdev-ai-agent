import sys
from google import genai
from google.genai import types
import argparse

from prompts import system_prompt
from functions.call_function import available_functions, call_function

OLLAMA_URL = "http://localhost:11434/v1"
OLLAMA_MODEl = "qwen3.5:27b"

def main():
    # Parser for user prompt from command line
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt for AI")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Create client instance with local Ollama url
    client = genai.Client(
        vertexai=True,  # Enable this to unlock the base_url override
        http_options=types.HttpOptions(
            base_url=OLLAMA_URL
        )
    )

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # print(f"Message from prompt: {messages}")     #for debug

    config = types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt,
        temperature=0
    )

    for i in range(20):
        if i >= 20:
            sys.exit("Reached the maximum numbers of iterations.")
        # Chose model and send message
        response = client.models.generate_content(
            model=OLLAMA_MODEl,
            contents=messages,
            config=config,
        )

        if not response or not response.usage_metadata:
            raise RuntimeError("Failed API request.")

        verbose_output = (
            f"User prompt: {args.user_prompt}/n"
            f"Prompt tokens: {response.usage_metadata.prompt_token_count}/n"
            f"Response tokens: {response.usage_metadata.candidates_token_count}"
        )

        # Add response 'candidates.content'(list of model response) to conversation history
        if response.candidates:
            for model_response in response.candidates:
                if not model_response.content:
                    print("Model response is empty.")
                    return
                messages.append(model_response.content)
                # print(f"Message with 'response.candidates': {messages}")  #for debug

        function_responses = []
        if func_calls := response.function_calls:
            for used_function in func_calls:
                function_call_result = call_function(used_function)
                if not function_call_result.parts:
                    raise Exception('Empty parts list')
                if not function_call_result.parts[0].function_response:
                    raise Exception("FunctionResponse object is None or empty")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception('Actual function result is None or empty')

                function_responses.append(function_call_result.parts[0])
                messages.append(types.Content(role="tool", parts=function_responses))
                # print(f"Message after func tools call: {messages}") #for debug

                if args.verbose:
                    print(
                        verbose_output.join(f"-> {function_call_result.parts[0].function_response.response}")
                    )
        else:
            print(f"Final response:\n{response.text}")
            return




if __name__ == "__main__":
    main()