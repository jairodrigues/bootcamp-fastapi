from fastapi import APIRouter

router = APIRouter(
    prefix="/health-check",
    tags=["health check"]
)

@router.get('/')
def read_root():
    return "OK"