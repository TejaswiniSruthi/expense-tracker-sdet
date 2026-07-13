from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class ExpenseResponse(BaseModel):
    """Contract for a single expense returned by the API."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    id: str = Field(alias="_id")
    amount: float = Field(gt=0)
    category: Literal[
        "Food", "Travel", "Shopping", "Bills", "Entertainment", "Health", "Other"
    ]
    description: Optional[str] = None
    paymentMethod: Literal["cash", "card", "upi", "netbanking"]
    date: datetime
    createdAt: datetime
    updatedAt: datetime
    v: int = Field(alias="__v")