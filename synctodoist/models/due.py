from datetime import datetime, date
from typing import Optional

from pydantic import BaseModel, Field

class Due(BaseModel):
    date: Optional[date | datetime] = None
    is_recurring: bool = False
    lang: Optional[str] = None
    string: Optional[str] = None
    timezone: Optional[str] = None
