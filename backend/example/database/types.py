from dataclasses import dataclass
from datetime import date



@dataclass
class Tool:
    name: str
    end_of_life: date
    entry_date: date
