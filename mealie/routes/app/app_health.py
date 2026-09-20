from fastapi import APIRouter

from mealie.schema.response.responses import SuccessResponse

router = APIRouter(prefix="/health")


@router.get("", response_model=SuccessResponse)
def get_health():
    """Lightweight liveness probe for container orchestrators"""
    return SuccessResponse(message="ok")
