import os
import sys
import subprocess

from .models import ExecuteModel

python_path = sys.executable

def run_code(code: str) -> ExecuteModel:
    file_path = "temp_execution_vibepython.py"
    try:
        with open(file_path, 'w') as f:
            f.write(code)
        result = subprocess.run([python_path, file_path], capture_output=True, text=True)
        return ExecuteModel(stdout=result.stdout,stderr=result.stderr,exit_code=result.returncode, is_internal_error=False, code=code)
    except Exception as e:
        return ExecuteModel(stdout="",stderr=f"Error during execution: {str(e)}",exit_code=1, is_internal_error=True, code=code)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
