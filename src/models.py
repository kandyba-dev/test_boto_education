from dataclasses import dataclass


@dataclass(slots=True)
class URLModel:
    id: int | None
    code: str
    original_url: str
