import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"

def generate_response(prompt):

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": True
        },
        stream=True
    )

    assistant_response = ""

    print("\nAssistant: ", end="", flush=True)

    for line in response.iter_lines():

        chunk = json.loads(line)

        token = chunk.get("response", "")

        print(token, end="", flush=True)

        assistant_response += token

        if chunk.get("done"):
            break

    print("\n")

    return assistant_response