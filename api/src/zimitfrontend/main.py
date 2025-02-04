from http import HTTPStatus

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from schedule import every
from starlette.requests import Request

from zimitfrontend import __about__
from zimitfrontend.blacklist import refresh_blacklist
from zimitfrontend.constants import ApiConfiguration, logger
from zimitfrontend.routes import hook, requests


class Main:

    def create_app(self) -> FastAPI:
        self.app = FastAPI(
            title=__about__.__api_title__,
            description=__about__.__api_description__,
            version=__about__.__version__,
        )

        @self.app.get("/api")
        @self.app.get("/")
        async def landing() -> RedirectResponse:  # pyright: ignore
            """Redirect to root of latest version of the API"""
            return RedirectResponse(
                f"/api/{__about__.__api_version__}/",
                status_code=HTTPStatus.TEMPORARY_REDIRECT,
            )

        api = FastAPI(
            title=__about__.__api_title__,
            description=__about__.__api_description__,
            version=__about__.__version__,
            docs_url="/",
            openapi_tags=[
                {
                    "name": "all",
                    "description": "all APIs",
                },
            ],
            contact={
                "name": "Kiwix/openZIM Team",
                "url": "https://www.kiwix.org/en/contact/",
                "email": "contact+offspot_metrics@kiwix.org",
            },
            license_info={
                "name": "GNU General Public License v3.0",
                "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
            },
        )

        @api.exception_handler(500)
        async def internal_exception_handler(  # pyright: ignore[reportUnusedFunction]
            _: Request, exc: Exception
        ):
            logger.exception(
                exc
            )  # log the exception which occured so that we can debug
            return JSONResponse(
                status_code=500,
                content=jsonable_encoder({"error": str(exc)}),
            )

        api.add_middleware(
            CORSMiddleware,
            allow_origins=ApiConfiguration.allowed_origins,
            allow_credentials=False,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        api.include_router(router=requests.router)
        api.include_router(router=hook.router)

        self.app.mount(f"/api/{__about__.__api_version__}", api)

        if ApiConfiguration.blacklist_url:
            refresh_blacklist()
            every(
                ApiConfiguration.blacklist_refresh_minutes
            ).minutes.do(  # pyright: ignore[reportUnknownMemberType]
                refresh_blacklist
            )

        return self.app
