import ollama

def parse_thinking(response):
    return response.split("</think>")[1]

def generate_response(model, prompt, think=True):
    try:
        response = ollama.generate(model=model, prompt=prompt, keep_alive=-1, think=think)["response"]
        print(f"(OLLAMA_LLM) Response: {response}")
        if think:
            return parse_thinking(response).strip()
        else:
            return response.strip()
    except Exception as e:
        try:
            response = ollama.generate(model=model, prompt=prompt, keep_alive=-1, think=False)["response"]
            print(f"(OLLAMA_LLM) Response: {response}")
            return response.strip()
        except Exception as e:
            return f"Error: Failed to generate response: {e}"