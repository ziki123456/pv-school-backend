from app.db.connection import DbConfig, create_connection


class ClassRepository:
    def __init__(self, cfg: DbConfig):
        self._cfg = cfg

    def list_all(self):
        sql = """
        SELECT id_class, name, school_year, is_active, created_at
        FROM class
        ORDER BY school_year DESC, name
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
