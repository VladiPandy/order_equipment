from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class InfoProjectResponse(BaseModel):
    is_admin: int
    project_name: str
    responsible_fio: str

class InfoListsRequest(BaseModel):
    year: int
    week: int  # Обязательно, формат "dd.mm.yyyy-dd.mm.yyyy"

class InfoListsResponse(BaseModel):
    project: List
    date: List
    analyse: List
    equipment: List
    executor: List
    status: List

class InfoBookingItem(BaseModel):
    id: int
    project: str
    date: str  # Формат: "dd.mm.yyyy"
    analyse: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: Optional[str] = ""