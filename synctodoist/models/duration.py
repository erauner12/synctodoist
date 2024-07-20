from pydantic import BaseModel, Field

class Duration(BaseModel):
    amount: int = Field(gt=0)
    unit: str = Field(pattern="^(minute|day)$")
