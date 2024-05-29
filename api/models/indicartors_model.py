from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class IndicatorsModel(BaseModel):
    universities: int
    countries: int
    docs: int
