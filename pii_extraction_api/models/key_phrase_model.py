from pydantic import BaseModel, ConfigDict, conlist


class KeyPhrases(BaseModel):
    key_phrases : conlist(item_type=str, min_length=0)

    model_config = ConfigDict(extra='forbid', frozen=True)