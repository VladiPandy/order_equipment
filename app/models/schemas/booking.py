from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional

class PossibleCreateBookingRequest(BaseModel):
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
    id: int
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


class Point(BaseModel):
    lat: float
    lon: float

class ChoseData(BaseModel):
    project: str
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: str
    point: Optional[Point] = None
    city: Optional[str] = None

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
    analyse: str
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

class FeedbackRequest(BaseModel):
    id: int
    question_1: bool
    question_2: bool
    question_3: bool




class FeedbackResponse(BaseModel):
    id: int
    data: str