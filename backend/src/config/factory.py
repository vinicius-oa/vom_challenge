""" WebApp Setup. """
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi import Request
from starlette.responses import JSONResponse

from config.di import DI
from config.exception import GeneralException
from domain.config_backend.controllers.config_backend import (
    ConfigBackendController
)
from domain.execution_engine.controllers.execution_engine import (
    ExecutionEngineController
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    dependencies = DI()
    dependencies.database().setup_database()
    yield


def create_app() -> FastAPI:
    app_ = FastAPI(title="Decision Policy API", lifespan=lifespan)
    app_.include_router(
        ConfigBackendController(
            router=APIRouter(
                prefix="/policy",
                tags=["ConfigBackend"]
            )
        ).router
    )
    app_.include_router(
        ExecutionEngineController(
            router=APIRouter(
                prefix="/execute",
                tags=["ExecutionEngine"]
            )
        ).router
    )
    return app_


app = create_app()


@app.exception_handler(GeneralException)
def general_exception_handler(request: Request, exc: GeneralException): # noqa
    return JSONResponse(
        content=exc.content,
        status_code=exc.status_code
    )
