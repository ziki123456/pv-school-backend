from __future__ import annotations

from typing import Optional

from app.core.models import Subject
from app.db.connection import DbConfig, transaction


class SubjectRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def list_all(self, active_only: bool = True):
        if active_only:
            sql = """
            SELECT id_subject, name, code, subject_type, is_active, created_at
            FROM subject
            WHERE is_active = 1
            ORDER BY name
            """
            params = ()
        else:
            sql = """
            SELECT id_subject, name, code, subject_type, is_active, created_at
            FROM subject
            ORDER BY name
            """
            params = ()

        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            rows = cur.fetchall()

        return [
            Subject(
                id_subject=int(r[0]),
                name=r[1],
                code=r[2],
                subject_type=r[3],
                is_active=bool(r[4]),
                created_at=r[5],
            )
            for r in rows
        ]

    def get_by_id(self, subject_id: int) -> Optional[Subject]:
        sql = """
        SELECT id_subject, name, code, subject_type, is_active, created_at
        FROM subject
        WHERE id_subject = %s
        """
        with transaction(self._cfg) as conn:
            cur = conn.cursor()
            cur.execute(sql, (int(subject_id),))
            r = cur.fetchone()

        if not r:
            return None

        return Subject(
            id_subject=int(r[0]),
            name=r[1],
            code=r[2],
            subject_type=r[3],
            is_active=bool(r[4]),
            created_at=r[5],
        )
