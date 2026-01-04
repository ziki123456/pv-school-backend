from app.db.connection import DbConfig, create_connection


class TimetableViewRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def get_by_class(self, class_id: int):
        sql = """
        SELECT *
        FROM v_class_timetable
        WHERE class_id = %s
        ORDER BY weekday, lesson_no
        """
        conn = create_connection(self._cfg)
        try:
            cur = conn.cursor()
            cur.execute(sql, (class_id,))
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        finally:
            conn.close()
