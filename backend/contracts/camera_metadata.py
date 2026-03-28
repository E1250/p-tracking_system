from typing import List
from pydantic import BaseModel


class CameraMetadata(BaseModel):
    camera_id: str
    is_danger: bool = False
    detection_metadata: List
    # depth_points: List = []
    # box_detections_ratio: List = []