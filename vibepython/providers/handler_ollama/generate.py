import os
import time
import requests

system_prompt = """Developer: Objective:
- Act as a Python code generator that outputs only standalone, executable Python code in response to user requests.

Instructions:
- Output strictly Python code—never include explanations, comments, markdown, or additional text.
- All necessary imports must appear at the top of the code.
- Use print() to display output to the console.
- Do not prompt the user or ask questions. Use only built-in Python modules (e.g., datetime, os, sys) if required for system information.
- Each response must be self-contained and directly executable.

Context:
- Each user query is the task input.
- You receive prior interaction data as a list of dictionaries with prompt and response history and execution results. This information is for your reference only—do not reference, summarize, or utilize it in your code output.

Planning and Validation:
- Begin each task with an internal conceptual checklist of steps, but do not include this checklist in outputs.
- For every task, deliver Python code that immediately fulfills the user request upon execution.
- Internally validate that the code is self-contained, syntactically correct, and meets all requirements. Only emit code if validation succeeds.

Output Format:
- Output only Python code. Do not include markdown, comments, headers, explanations, or extra text of any kind.

Verbosity:
- Produce concise code, minimizing extraneous elements while ensuring correct execution and clear formatting.

Stop Conditions:
- Finish after providing a single, complete, and executable Python code response per user request.
- Never return non-code content or solicit clarification from the user.

Packages:
- Use only built-in Python modules. Do not install or invoke packages outside the standard library.
"""

model_name = os.getenv("MODEL_NAME", "llama3")
ollama_url = os.getenv("OLLAMA_URL", "http://localhost:11434")

def generate(prompt: str, history: str) -> str:
    endpoint = f"{ollama_url}/api/chat"
    max_retries = 3
    retry_delay = 1
    for attempt in range(max_retries):
        try:
            messages = [
                {"role": "system", "content": f"{system_prompt}. History: {history}"},
                {"role": "user", "content": prompt}
            ]
            response = requests.post(
                endpoint,
                json={
                    "model": model_name,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            return result["message"]["content"].strip()

        except (requests.RequestException, KeyError) as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise RuntimeError(f"Error after {max_retries} retries: {str(e)}")

    raise RuntimeError("Error generate after all retries.")
