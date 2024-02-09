from pydantic import BaseModel


class CustomBaseModel(BaseModel):
    def model_dump(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}
        return d
