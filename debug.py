import uvicorn

from app.models import project, state, subscription
from app.settings import settings


def bootstrap_tables():
    for model in (project.Project, state.State, subscription.Subscription):
        table_name = model.get_table_name()
        if model.exists():
            print(f"Table '{table_name}' exists.")
        elif settings.initialize:
            print(f"Table '{table_name}' does not exist. Creating...")
            model.initialize()
        else:
            print(f"Table '{table_name}' does not exist and not initialized. Set 'cascade_initialize=true'.")


if __name__ == "__main__":
    bootstrap_tables()
    uvicorn.run('app.main:app', host="0.0.0.0", port=8001, reload=True)
