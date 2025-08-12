import os
import sys
import datetime
import subprocess

from loguru import logger

from .providers import generate
from .history import History

GRAY = "\033[90m"
RESET = "\033[0m"

python_path = sys.executable

def execute_code(code: str) -> tuple[str, str]:
    file_path = "temp_execution_vibepython.py"
    try:
        with open(file_path, 'w') as f:
            f.write(code)
        result = subprocess.run([python_path, file_path], capture_output=True, text=True)
        stdout = result.stdout
        stderr = result.stderr
        return stdout, stderr
    except Exception as e:
        return "", f"Error during execution: {str(e)}"
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

def main():
    history_path = os.getenv("HISTORY_PATH", "history.json")
    history_size = int(os.getenv("HISTORY_SIZE", 7))
    h = History(history_path=history_path, history_size=history_size)

    while True:
        prompt = input(GRAY + "Prompt: " + RESET)
        h.new.datetime = datetime.datetime.now()
        h.new.user_prompt = prompt
        try:
            code = generate(prompt=prompt, history=h.load().model_dump(mode="json")["history"][-history_size:])
            h.new.ai_model_response = code
            print(GRAY + "#" * 15 + RESET)
            print(GRAY + code + RESET)
            print(GRAY + "#" * 15 + RESET)
            h.new.stdout_result_code_execute, h.new.stderr_result_code_execute = execute_code(code)
            if h.new.stderr_result_code_execute != "":
                logger.warning(h.new.stderr_result_code_execute)
            if h.new.stdout_result_code_execute != "":
                logger.info(h.new.stdout_result_code_execute)
        except Exception as e:
            logger.warning(e)
        finally:
            h.save()

if __name__ == "__main__":
    main()
