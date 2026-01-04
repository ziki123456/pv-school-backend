from app.db.connection import DbConfig, create_connection


class ReportRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def get_class_subject_grades(self):
        sql = """
        SELECT *
        FROM v_report_class_subject_grades
        ORDER BY class_name, subject_name
        """
        conn = create_connection(self._cfg)
        try:
            cur = conn.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, r)) for r in rows]
        finally:
            conn.close()
