from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class PieDataModel(BaseModel):
    value: int
    name: str
