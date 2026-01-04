from fastapi import FastAPI

app = FastAPI(title="PV School App")


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
