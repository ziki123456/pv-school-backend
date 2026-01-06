from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Optional

from app.db.connection import DbConfig, transaction


@dataclass(frozen=True)
class TeacherImportRow:
    first_name: str
    last_name: str
    email: Optional[str]
    hired_date: Optional[date]
    is_active: bool


@dataclass(frozen=True)
class StudentImportRow:
    first_name: str
    last_name: str
    birth_date: Optional[date]
    class_id: Optional[int]
    is_active: bool


class ImportRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    # ---------- CSV LOADERS ----------
    def load_teachers_csv(self, csv_path: Path) -> list[TeacherImportRow]:
        rows: list[TeacherImportRow] = []
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader, start=2):  # 1 = header
                first = (r.get("first_name") or "").strip()
                last = (r.get("last_name") or "").strip()
                email = (r.get("email") or "").strip() or None
                hired_raw = (r.get("hired_date") or "").strip()
                active_raw = (r.get("is_active") or "1").strip()

                if not first or not last:
                    raise ValueError(f"teachers.csv line {i}: first_name/last_name required")

                hired = date.fromisoformat(hired_raw) if hired_raw else None
                is_active = active_raw in ("1", "true", "True", "yes", "YES")

                rows.append(
                    TeacherImportRow(
                        first_name=first,
                        last_name=last,
                        email=email,
                        hired_date=hired,
                        is_active=is_active,
                    )
                )
        return rows

    def load_students_csv(self, csv_path: Path) -> list[StudentImportRow]:
        rows: list[StudentImportRow] = []
        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for i, r in enumerate(reader, start=2):
                first = (r.get("first_name") or "").strip()
                last = (r.get("last_name") or "").strip()
                birth_raw = (r.get("birth_date") or "").strip()
                class_raw = (r.get("class_id") or "").strip()
                active_raw = (r.get("is_active") or "1").strip()

                if not first or not last:
                    raise ValueError(f"students.csv line {i}: first_name/last_name required")

                birth = date.fromisoformat(birth_raw) if birth_raw else None
                class_id = int(class_raw) if class_raw else None
                is_active = active_raw in ("1", "true", "True", "yes", "YES")

                rows.append(
                    StudentImportRow(
                        first_name=first,
                        last_name=last,
                        birth_date=birth,
                        class_id=class_id,
                        is_active=is_active,
                    )
                )
        return rows

    # ---------- DB INSERTS (TRANSACTION) ----------
    def import_teachers(self, rows: list[TeacherImportRow]) -> dict:
        sql = """
        INSERT INTO teacher (first_name, last_name, email, hired_date, is_active)
        VALUES (%s, %s, %s, %s, %s)
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            inserted = 0
            for r in rows:
                cur.execute(
                    sql,
                    (
                        r.first_name,
                        r.last_name,
                        r.email,
                        r.hired_date,
                        1 if r.is_active else 0,
                    ),
                )
                inserted += 1
        return {"inserted": inserted}

    def import_students(self, rows: list[StudentImportRow]) -> dict:
        sql = """
        INSERT INTO student (first_name, last_name, birth_date, class_id, is_active)
        VALUES (%s, %s, %s, %s, %s)
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            inserted = 0
            for r in rows:
                cur.execute(
                    sql,
                    (
                        r.first_name,
                        r.last_name,
                        r.birth_date,
                        r.class_id,
                        1 if r.is_active else 0,
                    ),
                )
                inserted += 1
        return {"inserted": inserted}
