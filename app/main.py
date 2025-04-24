import uvicorn
from fastapi import FastAPI

from app.routers import auth, user
from app.routers.config import root_api


app = FastAPI()
app_v1 = FastAPI()


app.mount("/v1", app_v1)

@app.get(root_api+"/")
async def welcome() -> dict:
    return {"message": "My todo app"}


app.include_router(auth.router)
app.include_router(user.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)