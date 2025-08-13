from __future__ import annotations

from pydantic import BaseModel


class ExecuteModel(BaseModel):
    is_internal_error: bool
    exit_code: int
    stdout: str
    stderr: str
    code: str
