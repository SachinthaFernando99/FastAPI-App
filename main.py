from fastapi import FastAPI
from routers.role import router as role_router
from routers.user import router as user_router

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])

