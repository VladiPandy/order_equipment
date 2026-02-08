from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class BaseInfoResponse(BaseModel):
    is_admin: int
    project_name: str
    responsible_fio: str
    is_open: int

class BaseInfoRequest(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None

class BaseInfoListsResponse(BaseModel):
    project: List
    date: List
    analyse: List
    equipment: List
    executor: List
    status: List

class BaseInfoItem(BaseModel):
    id: int
    project: str
    date: str
    analyse: str
    equipment: str
    executor: str
    samples: int
    status: str
    comment: Optional[str] = ""
    messages_count: Optional[int] = 0
    last_message_is_me: Optional[bool] = False

class BaseTableRow(BaseModel):
    monday: Optional[str] = ""
    tuesday: Optional[str] = ""
    wednesday: Optional[str] = ""
    thursday: Optional[str] = ""
    friday: Optional[str] = ""
    saturday: Optional[str] = ""
    sunday: Optional[str] = ""

class InfoProjectResponse(BaseInfoResponse):
    pass

class InfoListsRequest(BaseInfoRequest):
    pass

class InfoListsResponse(BaseInfoListsResponse):
    pass

class InfoBookingItem(BaseInfoItem):
    pass

class InfoExecutorTable(BaseTableRow):
    executor: str

class InfoEquipmentTable(BaseTableRow):
    equipment: str
    monday: str
    tuesday: str
    wednesday: str
    thursday: str
    friday: str
    saturday: str
    sunday: str

class RatingRowResponse(BaseModel):
    executor: str
    avg_total: Optional[float] = None
    avg_on_time: Optional[float] = None
    avg_full_set: Optional[float] = None
    avg_quality: Optional[float] = None
    total_answer_analyses: int = 0
    total_analyses: int = 0


class RatingsResponse(BaseModel):
    items: List[RatingRowResponse]