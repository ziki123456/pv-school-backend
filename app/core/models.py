from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass
class TeacherCreate:
    first_name: str
    last_name: str
    email: Optional[str] = None
    hired_date: Optional[date] = None
    is_active: bool = True


@dataclass
class Teacher:
    id_teacher: int
    first_name: str
    last_name: str
    email: Optional[str]
    hired_date: Optional[date]
    is_active: bool
    created_at: datetime
