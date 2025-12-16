from fastapi import FastAPI

app = FastAPI(
    title="Smaragd MVP"
)

@app.get("/")
def healthcheck():
    return {"status": "ok"}
