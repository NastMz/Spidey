from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class TreeMapDataModel(BaseModel):
    value: int
    name: str
