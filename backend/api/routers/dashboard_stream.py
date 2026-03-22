from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import asyncio

from backend.api.routers.metrics import active_dashboards 

router = APIRouter()

@router.websocket("/stream")
async def dashboard_websocket(websocket: WebSocket):
    """
    WebScoket sending updates to the dashboard. 

    url: ws://127.0.0.1:8000/dashboard/stream
    """
    state = websocket.app.state
    logger = state.logger

    # Accept the client connection. 
    await websocket.accept()

    # Logging and tracking 
    active_dashboards.inc()
    logger.info("Dashboard Connected...")

    try:
        while True:
            logger.debug("Sending updates to Dashboard...")
            cameras_metadata = state.camera_metadata
            await websocket.send_json(cameras_metadata)

            # Sending data to the dashboard every 1.5 seconds.
            await asyncio.sleep(state.settings.intervals.realtime_updates_every)

    except WebSocketDisconnect:
        logger.warn("Dashboard Disconnected Normally...")

    except Exception as e:
        logger.error(f"Dashboard Error: {e}")
    finally:
        active_dashboards.dec()