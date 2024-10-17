from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictStr, confloat, constr


class TextAiBaseModel(BaseModel):
    entity : constr(strict=True, min_length=1, strip_whitespace=True)
    category: constr(strict=True, min_length=1, strip_whitespace=True)
    confidence_score: confloat(strict=True, ge=0, le=1)

    model_config = ConfigDict(extra='forbid', frozen=True)   