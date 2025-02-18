from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class PossibleCreateBookingRequest(BaseModel):
    year: int
    week: int
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
    date:  Dict[str, Any]
    analyse:  Dict[str, Any]
    equipment:  Dict[str, Any]
    executor:  Dict[str, Any]
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
    year: int
    week: int
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
    date: Dict[str, Any]
    analyse: Dict[str, Any]
    equipment: Dict[str, Any]
    executor: Dict[str, Any]
    samples_limit: int
    samples_used: int
    status: Dict[str, Any]

class PossibleChangesResponse(BaseModel):
    chose: ChoseData
    change: ChangeData

class ChangeRequest(BaseModel):
    id: int
    project: str
    date: str
    analyze: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: str

class ChangeResponse(BaseModel):
    id: int
    changed_fields: Dict[str, Dict[str, Any]]

class CancelRequest(BaseModel):
    id: int

class CancelResponse(BaseModel):
    id: int
    data: str