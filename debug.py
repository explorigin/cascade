import uvicorn

from app.models import project, flagvalue


def bootstrap_tables():
    for model in (project.Project, flagvalue.FlagValue):
        if model.exists():
            print(f"Table '{model.get_table_name()}' exists.")
        else:
            print(f"Table '{model.get_table_name()}' does not exist. Creating.")
            model.create_table(True)


if __name__ == "__main__":
    bootstrap_tables()
    uvicorn.run('app.main:app', host="0.0.0.0", port=80, reload=True)
