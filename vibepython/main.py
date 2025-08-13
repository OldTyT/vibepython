import os
import datetime

from loguru import logger

from .providers import generate
from .history import History
from .execute import run_code, ExecuteModel

GRAY = "\033[90m"
RESET = "\033[0m"

history_path = os.getenv("HISTORY_PATH", "history.json")
history_size = int(os.getenv("HISTORY_SIZE", 7))
h = History(history_path=history_path, history_size=history_size)


def gray_print(text: str):
    print(GRAY + text + RESET)


def execute_code(user_prompt: str) -> ExecuteModel:
    MAX_RETRIES = 3
    for i in range(MAX_RETRIES):
        if i != 0:
            user_prompt = "Fix it!"
            logger.warning(f"Trying to fix the code automatically, attempt: {i+1}/{MAX_RETRIES}")
        h.new.datetime = datetime.datetime.now()
        h.new.user_prompt = user_prompt
        code = generate(prompt=user_prompt, history=h.load().model_dump(mode="json")["history"][-history_size:])
        h.new.ai_model_response = code
        r = run_code(code)
        h.new.stdout_result_code_execute = r.stdout
        h.new.stderr_result_code_execute = r.stderr
        h.new.exit_code = r.exit_code
        h.save()
        if r.exit_code == 0:
            return r
        if r.is_internal_error:
            if r.stdout != "":
                logger.info(f"STDOUT: {r.stdout}")
            if r.stderr != "":
                logger.warning(f"STDERR: {r.stderr}")
            return r
    logger.warning(f"Error auto fixing code.")
    return r


def main():
    while True:
        prompt = input(GRAY + "Prompt: " + RESET)
        try:
            r = execute_code(user_prompt=prompt)
            if not r.is_internal_error:
                gray_print(r.code)
            if r.stdout != "":
                logger.info("STDOUT:")
                logger.info(r.stdout)
            if r.stderr != "":
                logger.info("STDERR:")
                logger.info(r.stderr)
            if r.exit_code != 0:
                logger.warning(f"Exit code: {r.exit_code}")
        except Exception as e:
            logger.warning(e)

if __name__ == "__main__":
    main()
