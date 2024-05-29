from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class BagOfWordsModel(BaseModel):
    words: dict
