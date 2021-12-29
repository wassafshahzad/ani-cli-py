from dataclasses import dataclass, field
from typing import List, Type

from bs4.element import Tag

@dataclass
class Page:
    previous_page: Type[Tag] = None
    next_page: Type[Tag] = None
    obj: List[Type[Tag]] = field(default_factory=list)
