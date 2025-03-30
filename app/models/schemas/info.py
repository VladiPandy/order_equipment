from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class InfoProjectResponse(BaseModel):
    is_admin: int
    project_name: str
    responsible_fio: str
    is_open: int

class InfoListsRequest(BaseModel):
    start: Optional[str] = None  # Поле start может быть строкой или отсутствовать
    end: Optional[str] = None

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


class InfoExecutorTable(BaseModel):
    executor: str
    monday: Optional[str] = ""
    tuesday: Optional[str] = ""
    wednesday: Optional[str] = ""
    thursday: Optional[str] = ""
    friday: Optional[str] = ""
    saturday: Optional[str] = ""
    sunday: Optional[str] = ""

class InfoEquipmentTable(BaseModel):
    equipment: str
    monday: str
    tuesday: str  # Формат: "dd.mm.yyyy"
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str