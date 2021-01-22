from typing import Optional
from contextvars import ContextVar

import functools

project: ContextVar = ContextVar("project", default=None)
environment: ContextVar = ContextVar("environment", default=None)


def set_context(project_name, environment_name=None):
    project.set(project_name)
    environment.set(environment_name)


def extract_context(fn):
    @functools.wraps(fn)
    async def wrapper(*args, **kwargs):
        set_context(kwargs.get('project'), kwargs.get('environment'))
        try:
            return await fn(*args, **kwargs)
        finally:
            set_context(None, None)
    return wrapper
