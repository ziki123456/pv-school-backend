from __future__ import annotations

from app.db.connection import DbConfig, transaction


class TeacherSubjectRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def list_subjects_for_teacher(self, teacher_id: int):
        sql = """
        SELECT
          s.id_subject, s.name, s.code, s.subject_type, s.is_active, s.created_at
        FROM teacher_subject ts
        JOIN subject s ON s.id_subject = ts.subject_id
        WHERE ts.teacher_id = %s
        ORDER BY s.name
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(teacher_id),))
            return cur.fetchall()

    def assign(self, teacher_id: int, subject_id: int) -> bool:
        """
        Returns True if inserted, False if already existed (unique constraint).
        """
        sql = """
        INSERT INTO teacher_subject (teacher_id, subject_id)
        VALUES (%s, %s)
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            try:
                cur.execute(sql, (int(teacher_id), int(subject_id)))
                return True
            except Exception:
                # likely duplicate (uq_teacher_subject)
                return False

    def remove(self, teacher_id: int, subject_id: int) -> bool:
        sql = """
        DELETE FROM teacher_subject
        WHERE teacher_id = %s AND subject_id = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(teacher_id), int(subject_id)))
            return cur.rowcount > 0
