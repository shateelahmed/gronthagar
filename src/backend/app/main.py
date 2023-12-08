from fastapi import FastAPI
from app.models import database, User

app = FastAPI(title="Gronthagar")


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()
    # create a dummy entry
    await User.objects.get_or_create(email="shateel@gronthagar.com")

@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()

@app.get("/")
async def read_root():
    return await User.objects.all()