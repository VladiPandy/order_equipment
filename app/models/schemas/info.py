from pydantic import BaseModel
from typing import List, Optional

class InfoProjectResponse(BaseModel):
    is_admin: int
    project_name: str
    responsible_fio: str

class InfoListsRequest(BaseModel):
    date_period: str  # Обязательно, формат "dd.mm.yyyy-dd.mm.yyyy"

class InfoListsResponse(BaseModel):
    projects: List[str]
    date_bookings: List[str]
    analyzes: List[str]
    equipments: List[str]
    executors: List[str]
    statuses: List[str]

class InfoBookingItem(BaseModel):
    id: int
    project: str
    date_booking: str  # Формат: "dd.mm.yyyy"
    analyze: str
    equipment: str
    executor: str
    count_samples: int
    status: str
    comment: Optional[str] = ""