import asyncio
import itertools
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from ai.contracts.detector import DetectionResults
from backend.api.routers.metrics import active_cameras, frame_processing_duration_seconds
from backend.contracts.camera_metadata import CameraMetadata 
import traceback

import cv2 as cv
import numpy as np
import time

router = APIRouter()

@router.websocket("/stream/{camera_id}")
async def websocket_detect(websocket: WebSocket, camera_id:str):
    """
    WebSocket stream takes the frame pass it to the ai models, save it under the camera id provided in the url. 
    
     url here is:  ws://127.0.0.1:8000/detectors/stream/camera_id
    """
    # Yes, I asked the same questions, is using webscoket.app.state many times here is consuming.   after checking, it is not performance consuming. 
    state = websocket.app.state
    logger = state.logger
    detector = state.detection_model
    safety_detector = state.safety_detection_model
    depth_model = state.depth_model
    
    # Accepting the connection from the client
    await websocket.accept()

    # Logging and tracking action    
    active_cameras.inc()
    logger.info(f"Client ID >>{camera_id}<< Connected...")
    
    loop = asyncio.get_running_loop() 

    try:
        # What are the info you aim to collect from the camera? 
        # How many frames received by second. 
        # Frame processing time. 
        # Average processing time  for logger. 
        # Model processing time. 

        # frame_count = itertools.count()

        logger.info(f"Camera {camera_id} start sending frames...")

        def decode_frame():
            # Decode image
            return cv.imdecode(np.frombuffer(frame_bytes, np.uint8), cv.IMREAD_COLOR)        
            
        def run_detection(frame) -> DetectionResults:
            return detector.detect(frame)

        def run_safety(frame) -> DetectionResults:
            return safety_detector.detect(frame)

        def run_depth(frame, points):
            return depth_model.calculate_depth(frame, points)

        # Keep receiving messages in a loop until disconnection. 
        while True:

            # Profiling
            time_start = time.time()

            frame_bytes = await websocket.receive_bytes()
            
            image_array = await loop.run_in_executor(None, decode_frame)

            detection_task = loop.run_in_executor(None, run_detection, image_array)
            safety_task = loop.run_in_executor(None, run_safety, image_array)
            detections, safety_detection = await asyncio.gather(detection_task, safety_task)
            
            boxes_center = []
            boxes_center_ratio = []
            for box in detections.detections:
                print(type(box))
                xmin, ymin, xmax, ymax = box.xyxy
                xcenter = (xmax + xmin) / 2
                ycenter = (ymax + ymin) / 2
                boxes_center.append((int(xcenter), int(ycenter)))
                boxes_center_ratio.append(xcenter / image_array.shape[1])
            
            depth_points = await loop.run_in_executor(None, run_depth, image_array, boxes_center) if boxes_center else []

            detection_metadata = [{"depth": depth, "xRatio": xRatio} for depth, xRatio in zip(depth_points, boxes_center_ratio)]
            metadata = CameraMetadata(camera_id=camera_id, is_danger = True if safety_detection else False, detection_metadata=detection_metadata)
            print(metadata)
            state.camera_metadata[camera_id] = metadata.model_dump()

            # Profiling
            duration = time.time() - time_start
            frame_processing_duration_seconds.labels(camera_id).observe(round(duration, 3))
            logger.debug("Frame processed", camera_id=camera_id)
            
            # Note that JSONResponse doesn't work here, as it is for HTTP
            await websocket.send_json({"status": 200, "camera_id": camera_id})

    except WebSocketDisconnect:
        logger.warn(f"Client ID >>{camera_id}<< Disconnected Normally...")
        traceback.print_exc()  # This one is actually really better, it shows more details about the issue happened. 
        # Also work on and create the logger.exception, as it directly controls printing more details about the issue happened.
        state.camera_metadata.pop(camera_id, None)

    except Exception as e:
        logger.error(f"Error in websocker, Client ID: >>{camera_id}<<: {e}")
        traceback.print_exc()
        await websocket.close()
    finally:
        active_cameras.dec()


# Uncomment this when needed, It is the same but using HTTP, which is Request Response only. could be used for testing. 
# from fastapi import Request, UploadFile
# @router.post("/detect")
# async def post_detection(request: Request, file: UploadFile):
#     # Request here is being used to access the app.state.model

#     request.app.state.model.detect(file)