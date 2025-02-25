from fastapi import APIRouter, Request

from zimitfrontend.constants import tracker

router = APIRouter(
    prefix="/tracking",
    tags=["all"],
)


@router.get(
    "",
    status_code=200,
    responses={
        200: {
            "description": "Tracking data",
        },
    },
)
def get_tracking(request: Request) -> str:
    tracker.increment()
    headers = [f"{key}: {value}" for (key, value) in request.headers.items()]
    return (
        f"{request.client.host if request.client else "??"}: {tracker.count}"
        f" - {" ".join(headers)}"
    )
