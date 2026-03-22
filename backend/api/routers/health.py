# Very simple and important file, uesd to check the api health, if it return 200 everything is great, otherwise, there is an issue. 
# This file is being used mostly in HTTP and not websockets. 
# Health check is being used for example by docker, to check is dependencies are working fine, if not, he might restart. 

from http import HTTPStatus
from datetime import datetime
from fastapi import APIRouter, Response

from backend.api.routers.metrics import active_cameras

router = APIRouter()

@router.get("/")
@router.get("/live")
async def live_check(response: Response):
    """
    Prove that the process is running, No logic requried here. 
    Confirming that the server is not dead. 
    It is fails, container killed and restarted..
    Has to be very cheap.
    """
    response.status_code = HTTPStatus.OK
    # TODO you can add also some prometheus info here.
    return {
        "status": "live",
        "active_cameras": active_cameras._value.get(),
        "timestamp": datetime.now().isoformat()
        }

@router.get("/ready")
async def ready_check(response: Response):
    """
    Checck if parts work here, ex. are data readable. 
    Are data readable here. 
    Also can this instance accept traffic right now, or send them to another healthy instance.
    """
    # 1. Check database ping
    # 2. Check Redis or cache ping
    # 3. Queue connection or length

    response.status_code = HTTPStatus.OK
    # response.status_code = HTTPStatus.SERVICE_UNAVAILABLE
    return {
        "status": "ready",
        "timestamp": datetime.now().isoformat(),   # Sending the time also is a good practise
        "version": "1.0.0",
        }