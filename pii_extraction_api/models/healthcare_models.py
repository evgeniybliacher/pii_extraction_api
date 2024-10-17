from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr

from pii_extraction_api.models.text_ai_base_model import TextAiBaseModel


class DataSource(BaseModel):
    entity_id: StrictStr = Field(frozen= True)
    name: StrictStr = Field(frozen=True)

    class Config:
        frozen = True


class HealthcareEntity(TextAiBaseModel):
    subcategory: Optional[str]
    data_sources: Optional[List[DataSource]]
