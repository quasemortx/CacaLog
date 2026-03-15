from typing import Dict
from pydantic import BaseModel

class StatsResponse(BaseModel):
    total: int
    by_status: Dict[str, int]
    by_setor: Dict[str, int]
