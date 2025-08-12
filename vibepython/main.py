import os
import io
import sys
import datetime
from .providers import generate
from .history import History

GRAY = "\033[90m"
RESET = "\033[0m"

def main():
    history_path = os.getenv("HISTORY_PATH", "history.json")
    history_size = int(os.getenv("HISTORY_SIZE", 7))
    h = History(history_path=history_path, history_size=history_size)

    class Tee(io.StringIO):
        def __init__(self, original):
            super().__init__()
            self.original = original

        def write(self, s):
            super().write(s)
            self.original.write(s)

        def flush(self):
            super().flush()
            self.original.flush()

    while True:
        prompt = input(GRAY + "Prompt: " + RESET)
        h.new.datetime = datetime.datetime.now()
        h.new.user_prompt = prompt
        code = generate(prompt=prompt, history=h.load().model_dump(mode="json")["history"][-history_size:])
        h.new.ai_model_response = code
        print(GRAY + "#" * 15 + RESET)
        print(GRAY + code + RESET)
        print(GRAY + "#" * 15 + RESET)
        original_stdout = sys.stdout
        original_stderr = sys.stderr
        sys.stdout = Tee(original_stdout)
        sys.stderr = Tee(original_stderr)
        exec(code)
        # Capture stdout/stderr
        captured_stdout = sys.stdout.getvalue()
        captured_stderr = sys.stderr.getvalue()
        # Set default for stdout/stderr
        sys.stdout = original_stdout
        sys.stderr = original_stderr
        h.new.stdout_result_code_execute = captured_stdout
        h.new.stderr_result_code_execute = captured_stderr
        h.save()

if __name__ == "__main__":
    main()
