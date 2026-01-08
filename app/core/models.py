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

@dataclass
class StudentCreate:
    first_name: str
    last_name: str
    birth_date: Optional[date] = None
    class_id: Optional[int] = None
    is_active: bool = True


@dataclass
class Student:
    id_student: int
    first_name: str
    last_name: str
    birth_date: Optional[date]
    class_id: Optional[int]
    is_active: bool
    created_at: datetime
    last_grade_at: Optional[datetime]


@dataclass
class Subject:
    id_subject: int
    name: str
    code: str
    subject_type: str
    is_active: bool
    created_at: datetime
