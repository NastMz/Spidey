from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class LanguagesDataModel(BaseModel):
    language: str
    count: int
