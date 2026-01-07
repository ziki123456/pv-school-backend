from __future__ import annotations

from app.db.connection import DbConfig, transaction


class ExportRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def list_teachers(self) -> list[tuple]:
        sql = """
        SELECT id_teacher, first_name, last_name, email, hired_date, is_active, created_at
        FROM teacher
        ORDER BY id_teacher
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()

    def list_students(self) -> list[tuple]:
        sql = """
        SELECT id_student, first_name, last_name, birth_date, class_id, is_active, created_at, last_grade_at
        FROM student
        ORDER BY id_student
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql)
            return cur.fetchall()
