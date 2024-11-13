from fastapi import FastAPI
from routers.role import router as role_router
from routers.user import router as user_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(role_router, prefix="/roles", tags=["Roles"])
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

