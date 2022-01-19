from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Relation(Enum):
    FAMILY = 0
    FRIEND = 1


class Language(Enum):
    RU = 0
    EN = 1
    TAT = 2


@dataclass
class Contact:
    whatsapp: Optional[str]
    telegram_id: Optional[str]
