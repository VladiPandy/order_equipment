from pydantic import BaseModel
from typing import List, Optional

class InfoProjectResponse(BaseModel):
    is_admin: int
    project_name: str
    responsible_fio: str

class InfoListsRequest(BaseModel):
    date_period: str  # Обязательно, формат "dd.mm.yyyy-dd.mm.yyyy"

class InfoListsResponse(BaseModel):
    project: List[str]
    date: List[str]
    analyse: List[str]
    equipment: List[str]
    executor: List[str]
    status: List[str]

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