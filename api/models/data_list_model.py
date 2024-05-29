from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class DataListModel(BaseModel):
    data: list
