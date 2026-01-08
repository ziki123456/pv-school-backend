from __future__ import annotations

from typing import Optional

from app.core.models import StudentCreate, Student
from app.db.connection import DbConfig, transaction


class StudentRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def create(self, data: StudentCreate) -> int:
        sql = """
        INSERT INTO student (first_name, last_name, birth_date, class_id, is_active)
        VALUES (%s, %s, %s, %s, %s)
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    data.first_name,
                    data.last_name,
                    data.birth_date,
                    data.class_id,
                    1 if data.is_active else 0,
                ),
            )
            return int(cur.lastrowid)

    def get_by_id(self, student_id: int) -> Optional[Student]:
        sql = """
        SELECT id_student, first_name, last_name, birth_date, class_id, is_active, created_at, last_grade_at
        FROM student
        WHERE id_student = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(student_id),))
            row = cur.fetchone()

        if not row:
            return None

        return Student(
            id_student=int(row[0]),
            first_name=row[1],
            last_name=row[2],
            birth_date=row[3],
            class_id=int(row[4]) if row[4] is not None else None,
            is_active=bool(row[5]),
            created_at=row[6],
            last_grade_at=row[7],
        )

    def list_all(self, limit: int = 50, offset: int = 0):
        sql = """
        SELECT id_student, first_name, last_name, birth_date, class_id, is_active, created_at, last_grade_at
        FROM student
        ORDER BY id_student
        LIMIT %s OFFSET %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(limit), int(offset)))
            rows = cur.fetchall()

        return [
            Student(
                id_student=int(r[0]),
                first_name=r[1],
                last_name=r[2],
                birth_date=r[3],
                class_id=int(r[4]) if r[4] is not None else None,
                is_active=bool(r[5]),
                created_at=r[6],
                last_grade_at=r[7],
            )
            for r in rows
        ]

    def update(self, student_id: int, data: StudentCreate) -> bool:
        sql = """
        UPDATE student
        SET first_name = %s,
            last_name = %s,
            birth_date = %s,
            class_id = %s,
            is_active = %s
        WHERE id_student = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    data.first_name,
                    data.last_name,
                    data.birth_date,
                    data.class_id,
                    1 if data.is_active else 0,
                    int(student_id),
                ),
            )
            return cur.rowcount > 0

    def delete(self, student_id: int) -> bool:
        sql = "DELETE FROM student WHERE id_student = %s"
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(student_id),))
            return cur.rowcount > 0
