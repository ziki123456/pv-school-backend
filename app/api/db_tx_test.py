from fastapi import APIRouter, Request

from app.db.connection import DbConfig, transaction

router = APIRouter()


def _db_cfg(request: Request) -> DbConfig:
    config = request.app.state.config
    db = config.db
    return DbConfig(
        host=db["host"],
        port=int(db["port"]),
        database=db["database"],
        user=db["user"],
        password=db["password"],
        charset=db.get("charset", "utf8mb4"),
    )


@router.get("/api/db/tx-test")
def tx_test(request: Request):
    cfg = _db_cfg(request)

    # 1) commit test
    with transaction(cfg) as conn:
        cur = conn.cursor()
        cur.execute("CREATE TEMPORARY TABLE tmp_tx_test (id INT PRIMARY KEY)")
        cur.execute("INSERT INTO tmp_tx_test (id) VALUES (1)")
        cur.execute("SELECT COUNT(*) FROM tmp_tx_test")
        committed_count = cur.fetchone()[0]

    # 2) rollback test (duplicitní PK -> error -> rollback)
    rolled_back = False
    try:
        with transaction(cfg) as conn:
            cur = conn.cursor()
            cur.execute("CREATE TEMPORARY TABLE tmp_tx_test2 (id INT PRIMARY KEY)")
            cur.execute("INSERT INTO tmp_tx_test2 (id) VALUES (1)")
            cur.execute("INSERT INTO tmp_tx_test2 (id) VALUES (1)")
    except Exception:
        rolled_back = True

    return {
        "commit_ok": committed_count == 1,
        "rollback_ok": rolled_back,
    }
