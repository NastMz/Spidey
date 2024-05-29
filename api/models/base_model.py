from dataclasses import asdict, is_dataclass


class BaseModel:
    def to_dict(self):
        if is_dataclass(self):
            return asdict(self)
        raise TypeError("to_dict() should only be used on dataclass instances")
