from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class PossibleCreateBookingRequest(BaseModel):
    date_period: str = Field(
        ...,
        description="Период в формате dd.mm.yyyy-dd.mm.yyyy",
        example="19.01.2024-27.10.2024"
    )
    date: Optional[str] = Field(
        None,
        description="Дополнительное поле; если передается, заполнение запрещено",
        example="26.08.2024"
    )
    analyse: Optional[str] = Field(
        None,
        description="Дополнительное поле; если передается, заполнение запрещено",
        example="Анализ 1"
    )
    equipment: Optional[str] = Field(
        None,
        description="Дополнительное поле; если передается, заполнение запрещено",
        example="Прибор 1"
    )
    executor: Optional[str] = Field(
        None,
        description="Дополнительное поле; если передается, заполнение запрещено",
        example="Иванов Иван Дмитриевич"
    )

class PossibleCreateBookingResponse(BaseModel):
    date: List[str]
    analyse: List[str]
    equipment: List[str]
    executor: List[str]
    samples_limit: int
    used: int


class CreateBookingRequest(BaseModel):
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int

class CreateBookingResponse(BaseModel):
    id: int


class PossibleChangesRequest(BaseModel):
    date_period: str
    id: int


class ChoseData(BaseModel):
    project: str
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: str
class ChangeData(BaseModel):
    date: List[str]
    analyse: List[str]
    equipment: List[str]
    executor: List[str]
    samples_limit: int
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