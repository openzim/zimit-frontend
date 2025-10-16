from http import HTTPStatus

from fastapi import APIRouter, HTTPException

from zimitfrontend.constants import ApiConfiguration
from zimitfrontend.routes.schemas import OfflinerDefinitionSchema
from zimitfrontend.zimfarm import query_api

router = APIRouter(
    prefix="/offliner-definition",
    tags=["all"],
)


@router.get(
    "",
    summary="Get the definition for the zimit offliner",
    status_code=200,
    responses={
        200: {
            "description": "Zimit offliner definition schema",
        },
    },
)
def get_offliner_definition() -> OfflinerDefinitionSchema:
    _, status, schema = query_api(
        "GET", f"/offliners/zimit/{ApiConfiguration.zimit_definition_version}"
    )
    if status != HTTPStatus.OK:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail={
                "error": (
                    f"Failed to get offliner defintion on Zimfarm with HTTP {status}"
                ),
                "zimfarm_message": schema,
            },
        )
    return OfflinerDefinitionSchema.model_validate(schema)
