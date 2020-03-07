import uvicorn

from app.models import project


def bootstrap_tables():
    for model in (project.Project,):
        if not model.exists():
            model.create_table(True)


if __name__ == "__main__":
    bootstrap_tables()
    uvicorn.run('app.main:app', host="0.0.0.0", port=80, reload=True)
