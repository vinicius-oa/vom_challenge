from fastapi import APIRouter


class BaseController:

    def __init__(self, *, router: APIRouter):
        self._router = router

    @property
    def router(self) -> APIRouter:
        return self._router
