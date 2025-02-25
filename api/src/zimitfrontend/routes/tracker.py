from fastapi import APIRouter, Request

from zimitfrontend.constants import ApiConfiguration
from zimitfrontend.routes.schemas import TrackerStatusRequest, TrackerStatusResponse
from zimitfrontend.tracker import AddTaskResponse, tracker

router = APIRouter(
    prefix="/tracker_status",
    tags=["all"],
)


@router.post(
    "",
    summary="Get information about ongoing tasks and/or possibility to request a new task",
    status_code=200,
    responses={
        200: {
            "description": "Tracking status",
        },
    },
)
def post_tracker_status(status_request: TrackerStatusRequest, request: Request) -> TrackerStatusResponse:
    tracker_status = tracker.add_task(request.client.host, status_request.unique_id, None)
    return TrackerStatusResponse(status = tracker_status.status, ongoing_tasks=tracker_status.ongoing_tasks)
    
