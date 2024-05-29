from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class MapDataModel(BaseModel):
    country: str
    coords: list
    count: int
