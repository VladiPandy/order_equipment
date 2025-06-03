from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class BaseBookingRequest(BaseModel):
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

class BaseBookingResponse(BaseModel):
    date: Dict[str, Any]
    analyse: Dict[str, Any]
    equipment: Dict[str, Any]
    executor: Dict[str, Any]
    is_priority: Dict[str, Any]
    samples_limit: int
    used: int

class BaseBookingData(BaseModel):
    project: str
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: str

class Point(BaseModel):
    lat: float
    lon: float

class ChoseData(BaseBookingData):
    point: Optional[Point] = None
    city: Optional[str] = None

class ChangeData(BaseModel):
    date: Dict[str, Any]
    analyse: Dict[str, Any]
    equipment: Dict[str, Any]
    executor: Dict[str, Any]
    is_priority: Dict[str, Any]
    samples_limit: int
    samples_used: int
    status: Dict[str, Any]

class PossibleCreateBookingRequest(BaseBookingRequest):
    pass

class PossibleCreateBookingResponse(BaseBookingResponse):
    pass

class CreateBookingRequest(BaseModel):
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int

class CreateBookingResponse(BaseModel):
    id: int

class PossibleChangesRequest(BaseBookingRequest):
    id: int

class PossibleChangesResponse(BaseModel):
    chose: ChoseData
    change: ChangeData

class ChangeRequest(BaseBookingData):
    id: int

class ChangeResponse(BaseModel):
    id: int
    changed_fields: Dict[str, Dict[str, Any]]

class CancelRequest(BaseModel):
    id: int

class CancelResponse(BaseModel):
    id: int
    data: str

class FeedbackRequest(BaseModel):
    id: int
    question_1: bool
    question_2: bool
    question_3: bool

class FeedbackResponse(BaseModel):
    id: int
    data: str