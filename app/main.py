from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import flags, projects, subscriptions

app = FastAPI(
    title='Cascade',
    description='',
    version='1.0.0',
    root_path='/api/v1'
)

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(flags.router, prefix="/flags")
app.include_router(projects.router, prefix="/projects")
app.include_router(subscriptions.router, prefix="/subscriptions")
