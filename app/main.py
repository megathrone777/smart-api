from fastapi import FastAPI
from app.routers import tags

app = FastAPI()
app.include_router(tags.router)

@app.get("/")
async def root():
	return {"message": "Hello"}