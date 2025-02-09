from .common import CommonModel
from typing import Optional, List
from datetime import date, datetime

class Booking(CommonModel):
    """Модель фильма"""

    id: int
    project: str
    date_booking: date
    analyze: str
    equipment: str
    executor: str
    samples: int
    status: str
    created: datetime
    modified: datetime
    is_block: Optional[bool] = False


class BookingList(CommonModel):
    results: list[Booking]