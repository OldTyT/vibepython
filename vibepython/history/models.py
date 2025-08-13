from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class HistoryModel(BaseModel):
    datetime: datetime
    user_prompt: Optional[str] = None
    ai_model_response: Optional[str] = None
    exit_code: Optional[int] = None
    stdout_result_code_execute: Optional[str] = None
    stderr_result_code_execute: Optional[str] = None


class HistoryList(BaseModel):
    history: List[HistoryModel]
