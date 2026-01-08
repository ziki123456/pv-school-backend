from __future__ import annotations

from typing import Optional

from app.core.models import TeacherCreate, Teacher
from app.db.connection import DbConfig, transaction


class TeacherRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def create(self, data: TeacherCreate) -> int:
        sql = """
        INSERT INTO teacher (first_name, last_name, email, hired_date, is_active)
        VALUES (%s, %s, %s, %s, %s)
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    data.first_name,
                    data.last_name,
                    data.email,
                    data.hired_date,
                    1 if data.is_active else 0,
                ),
            )
            return int(cur.lastrowid)

    def get_by_id(self, teacher_id: int) -> Optional[Teacher]:
        sql = """
        SELECT id_teacher, first_name, last_name, email, hired_date, is_active, created_at
        FROM teacher
        WHERE id_teacher = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (teacher_id,))
            row = cur.fetchone()

        if not row:
            return None

        return Teacher(
            id_teacher=int(row[0]),
            first_name=row[1],
            last_name=row[2],
            email=row[3],
            hired_date=row[4],
            is_active=bool(row[5]),
            created_at=row[6],
        )

    def list_all(self, limit: int = 50, offset: int = 0):
        sql = """
        SELECT id_teacher, first_name, last_name, email, hired_date, is_active, created_at
        FROM teacher
        ORDER BY id_teacher
        LIMIT %s OFFSET %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(limit), int(offset)))
            rows = cur.fetchall()

        return [
            Teacher(
                id_teacher=int(r[0]),
                first_name=r[1],
                last_name=r[2],
                email=r[3],
                hired_date=r[4],
                is_active=bool(r[5]),
                created_at=r[6],
            )
            for r in rows
        ]

    def update(self, teacher_id: int, data: TeacherCreate) -> bool:
        """Update an existing teacher. Returns True if updated, else False."""
        sql = """
        UPDATE teacher
        SET first_name = %s,
            last_name = %s,
            email = %s,
            hired_date = %s,
            is_active = %s
        WHERE id_teacher = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(
                sql,
                (
                    data.first_name,
                    data.last_name,
                    data.email,
                    data.hired_date,
                    1 if data.is_active else 0,
                    int(teacher_id),
                ),
            )
            return cur.rowcount > 0

    def delete(self, teacher_id: int) -> bool:
        """Delete a teacher by id. Returns True if deleted, else False."""
        sql = "DELETE FROM teacher WHERE id_teacher = %s"
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(teacher_id),))
            return cur.rowcount > 0
