from __future__ import annotations

from dataclasses import dataclass
from contextlib import contextmanager
from typing import Iterator

import mysql.connector
from mysql.connector import MySQLConnection


class DbError(Exception):
    pass


@dataclass(frozen=True)
class DbConfig:
    host: str
    port: int
    database: str
    user: str
    password: str
    charset: str = "utf8mb4"


def create_connection(cfg: DbConfig) -> MySQLConnection:
    try:
        return mysql.connector.connect(
            host=cfg.host,
            port=cfg.port,
            database=cfg.database,
            user=cfg.user,
            password=cfg.password,
            charset=cfg.charset,
            use_unicode=True,
            autocommit=False,  # transakce řídíme my
        )
    except mysql.connector.Error as e:
        raise DbError(str(e)) from e


@contextmanager
def transaction(cfg: DbConfig) -> Iterator[MySQLConnection]:
    conn = create_connection(cfg)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def ping_db(cfg: DbConfig) -> dict:
    conn = create_connection(cfg)
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        return {"ok": True, "result": result[0]}
    finally:
        conn.close()
