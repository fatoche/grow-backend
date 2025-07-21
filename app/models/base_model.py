from pydantic import BaseModel
from typing import Any


class BusinessModelBase(BaseModel):
    class Config:
        from_attributes = True

    @classmethod
    def model_validate(cls, obj: Any, **kwargs):
        if hasattr(obj, "id"):
            obj.id = str(obj.id)
        return super().model_validate(obj, **kwargs)
