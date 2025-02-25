from http import HTTPStatus

from fastapi import APIRouter, HTTPException, Request

from zimitfrontend.routes.schemas import TrackerStatusRequest, TrackerStatusResponse
from zimitfrontend.tracker import tracker

router = APIRouter(
    prefix="/tracker_status",
    tags=["all"],
)


@router.post(
    "",
    summary="Get information about ongoing tasks and/or possibility to request"
    " a new task",
    status_code=200,
    responses={
        200: {
            "description": "Tracking status",
        },
    },
)
def post_tracker_status(
    status_request: TrackerStatusRequest, http_request: Request
) -> TrackerStatusResponse:

    if not http_request.client:
        raise HTTPException(
            HTTPStatus.INTERNAL_SERVER_ERROR, detail="http_request.client is missing"
        )

    tracker_status = tracker.add_task(
        http_request.client.host, status_request.unique_id, None
    )
    return TrackerStatusResponse(
        status=tracker_status.status.value, ongoing_tasks=tracker_status.ongoing_tasks
    )
