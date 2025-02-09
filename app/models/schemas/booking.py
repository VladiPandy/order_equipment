from pydantic import BaseModel
from typing import Dict, List, Any

class PossibleCreateBookingRequest(BaseModel):
    date_period: str  # Обязательно, формат "dd.mm.yyyy-dd.mm.yyyy"
    # Если передаются другие поля, то это считается запрещённым заполнением.
    date_booking: str = None
    analyze: str = None
    equipment: str = None
    executor: str = None

class PossibleCreateBookingResponse(BaseModel):
    dates: List[str]
    analyzes: List[str]
    equipments: List[str]
    executors: List[str]
    sample_limits: int


class CreateBookingRequest(BaseModel):
    date_booking: str
    analyze: str
    equipment: str
    executor: str
    count_samples: int

class CreateBookingResponse(BaseModel):
    id: int


class PossibleChangesRequest(BaseModel):
    date_period: str
    id: int


class ChoseData(BaseModel):
    project: str
    date: str
    analyze: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: str
class ChangeData(BaseModel):
    dates: List[str]
    analyzes: List[str]
    equipments: List[str]
    executors: List[str]
    sample_limits: int
    status: List[str]

class PossibleChangesResponse(BaseModel):
    chose: ChoseData
    change: ChangeData

class ChangeRequest(BaseModel):
    date_period: str
    id: int
    project: str          # Для админов
    date: str     # Формат "dd.mm.yyyy"
    analyze: str
    equipment: str
    executor: str
    samples: int
    status: str           # Для админов
    comment: str          # Для админов

class ChangeResponse(BaseModel):
    id: int
    changed_fields: Dict[str, Dict[str, Any]]

class CancelRequest(BaseModel):
    date_period: str
    id: int

class CancelResponse(BaseModel):
    id: int
    data: str