conversation_history = []

system_prompt = """
You are a senior AI assistant.

If a tool result is present in the conversation history,
you MUST use that tool result to answer the user.

In that case, respond ONLY in this format:

{
  "response": "final answer"
}

Do not call any tool again if a tool result is already present.

When the user asks ANY math question,
you MUST respond ONLY in this JSON format:

{
  "tool": "calculator",
  "arguments": {
    "expression": "math expression"
  }
}

When the user asks for the current time or date,
you MUST respond ONLY in this JSON format:

{
  "tool": "getTime",
  "arguments": {}
}

When the user asks about weather, temperature, or conditions,
you MUST respond ONLY in this JSON format:

{
  "tool": "getWeather",
  "arguments": {}
}

For all other questions,
you MUST respond ONLY in this JSON format:

{
  "response": "your answer here"
}

Do not solve math yourself.
Do not guess the current time or weather.
Do not return explanations outside the JSON object.

"""

def add_user_message(message):
    conversation_history.append({
        "role": "user",
        "content": message
    })

def add_assistant_message(message):
    conversation_history.append({
        "role": "assistant",
        "content": message
    })

def get_conversation_history():
    return conversation_history

def buildPrompt():
    prompt = f"system: {system_prompt}\n\n"

    for message in conversation_history:
        prompt += f"{message['role']}: {message['content']}\n"
    return prompt

def print_history():
    print("\nConversation History:\n")

    for message in conversation_history:
        print(f"{message['role']}: {message['content']}")

def add_tool_message(message):
    conversation_history.append({
        "role": "tool",
        "content": message
    })