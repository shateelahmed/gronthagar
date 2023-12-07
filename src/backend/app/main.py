from fastapi import FastAPI

app = FastAPI(title="Gronthagar")


@app.get("/")
def read_root():
    return {"hello": "world"}