# 3rd Party
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# routers
from .routers import *

app = FastAPI()
app.include_router(post_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(vote_router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
