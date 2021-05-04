from fastapi import FastAPI

from hex.configuration import configure_inject
from hex.web.post_router import create_post_routers


def create_application() -> FastAPI:
    application = FastAPI(title=__name__)
    configure_inject()

    application.include_router(
        create_post_routers(),
        prefix="/posts",
        tags=["Post"],
        responses={404: {"description": "Not found"}},
    )

    return application
