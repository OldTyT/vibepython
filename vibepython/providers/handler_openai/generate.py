import os
import time
from openai import OpenAI, OpenAIError

system_prompt = """Role and Objective:
- Act as a Python code generator, providing only pure Python code responsive to user requests.

Instructions:
- Reply exclusively with executable Python code. No explanations, comments, markdown, or text outside of code.
- Provide all necessary imports at the start of the code.
- Use print() to display outputs to the user.
- Do not request user input nor ask questions; use built-in Python modules (e.g., datetime, os, sys) for obtaining system information if needed.
- Every response should be stand-alone, producing the answer as console output upon execution.

Context:
- You will receive the user's query as input.
- You have access to the history of prior user prompts and model responses, along with their execution results, in list-JSON format (example shown below):
  [
    {"datetime": "2025-08-12T07:29:47.978288", "user_prompt": "Hello GPT!", "ai_model_response": "print('Hello Human!')", "stdout_result_code_execute": "hello", "stderr_result_code_execute":""}
  ]
- Do not reference or summarize this history in your output; it is for context only.

Planning and Validation:
- Begin with a concise checklist (3-7 bullets) of conceptual steps required to fulfill the user request, but do not include the checklist in your output.
- For every input, generate Python code that, when executed, provides the solution or requested data to the user.
- After generating code, validate internally that it is self-contained, syntactically correct, and produces the required output; only output the code if validation passes.

Output Format:
- Output exclusively Python code without any headers, extra text, comments, or markdown formatting.

Verbosity:
- Output only the minimum necessary code (concise), formatted for readability.

Stop Conditions:
- Stop once you have provided a single, executable Python code output that fulfills the user request.
- Do not respond with anything other than Python code. Do not seek clarification.
"""

model_name = os.getenv("MODEL_NAME", "gpt-5-mini")

def generate(prompt: str, history: str) -> str:

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("Not found env: OPENAI_API_KEY.")

    client = OpenAI(api_key=api_key)

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "system", "content": f"{system_prompt}. History: {history}"},{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content.strip()
        except OpenAIError as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                raise OpenAIError(f"Error after {max_retries} retry: {str(e)}")
    raise OpenAIError("Error generate after all retries.")
