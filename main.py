import json

from conversation import (
    add_user_message,
    add_assistant_message,
    print_history,
    buildPrompt,
    add_tool_message
)

from llm_client import generate_response

from tools import run_tool

RED = "\033[31m"
RESET = "\033[0m"

while True:

    user_input = input(f"\n{RED}You:{RESET} ")

    if user_input.lower() == "exit":
        break

#store user input in the conversation history
    add_user_message(user_input)

#generate the assistant response    
    prompt = buildPrompt()
    assistant_response = generate_response(prompt)

    try:
    #parse the assistant response as JSON
        print("\nAssistant Response:", assistant_response)
        parsed_response = json.loads(assistant_response)
        if "tool" in parsed_response:
            tool = parsed_response["tool"]
            arguments = parsed_response["arguments"]
            tool_result = run_tool(tool, arguments)
            add_tool_message(json.dumps({
                "tool": tool,
                "result": tool_result
            }))
            print("\nTool Result:", tool_result)

            # SECOND LLM CALL
            prompt = buildPrompt()

            final_response = generate_response(prompt)

            final_response_json = json.loads(final_response)

            add_assistant_message(
                final_response_json["response"]
            )
            print("\nFinal Response:", final_response)
        else:   
            actual_response = parsed_response["response"]
            add_assistant_message(actual_response)

    except Exception as e:
        print("\nJSON Parsing Failed")
        print(e)

        add_assistant_message(assistant_response)

#print the conversation history
    # print_history()