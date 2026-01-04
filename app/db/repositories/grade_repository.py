from __future__ import annotations

from app.db.connection import DbConfig, transaction


class GradeRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def create_grade_and_touch_student(
        self,
        student_id: int,
        subject_id: int,
        value: float,
        teacher_id: int | None = None,
        note: str | None = None,
    ) -> int:
        """
        Transakce nad více tabulkami:
        1) INSERT do grade
        2) UPDATE student.last_grade_at
        """
        insert_sql = """
        INSERT INTO grade (student_id, subject_id, teacher_id, value, note)
        VALUES (%s, %s, %s, %s, %s)
        """
        update_sql = """
        UPDATE student
        SET last_grade_at = NOW()
        WHERE id_student = %s
        """

        with transaction(self._cfg) as conn:
            cur = conn.cursor()

            cur.execute(insert_sql, (student_id, subject_id, teacher_id, value, note))
            new_id = int(cur.lastrowid)

            cur.execute(update_sql, (student_id,))
            if cur.rowcount != 1:
                # student neexistuje nebo se neupdatuje -> vyvoláme chybu -> rollback
                raise ValueError("Student not found for last_grade_at update")

            return new_id
