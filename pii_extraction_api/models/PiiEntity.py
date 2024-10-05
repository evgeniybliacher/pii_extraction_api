from typing import Self
from pydantic import BaseModel, Field, StrictFloat, StrictStr, model_validator


class PiiEntity(BaseModel):
    name: StrictStr = Field(frozen= True)
    category: StrictStr = Field(frozen = True)
    confidence_score: StrictFloat = Field(frozen=True, ge=0, le=1)