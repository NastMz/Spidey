from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class BarDataModel(BaseModel):
    categories: list
    data: list
