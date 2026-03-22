from typing import List
from pydantic import BaseModel


class CameraMetadata(BaseModel):
    camera_id: str
    is_danger: bool = False
    depth_points: List = []