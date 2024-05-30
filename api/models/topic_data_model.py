from dataclasses import dataclass
from api.models import BaseModel


@dataclass
class TopicWordModel(BaseModel):
    word: int
    probability: str


@dataclass
class TopicDataModel(BaseModel):
    topic: str
    words: list
