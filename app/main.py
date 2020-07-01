from fastapi import FastAPI
from .routers import flags, projects, subscriptions

app = FastAPI(
    title='Cascade',
    description='',
    version='1.0.0',
)

app.include_router(flags.router, prefix="/flags")
app.include_router(projects.router, prefix="/projects")
app.include_router(subscriptions.router, prefix="/subscriptions")


@app.get("/")
async def root():
    return {"message": "Hello World"}
