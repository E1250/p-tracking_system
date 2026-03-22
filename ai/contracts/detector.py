# contracts/detector.py

from pydantic import BaseModel, Field, field_validator, model_validator
from typing import List


class BBox(BaseModel):
    """
    cls: Class id
    name: Class Name
    conf: Confidence
    orig_shape: Original Box Shape  # TODO, mostly thiis is going to be added in the Detection results instead of here.
    xyxy: Box Coordinates
    """

    class_id: int
    class_name: str
    conf: float = Field(ge=0, le=1)  # Annotated means, it should had more than one rule, the first rule is that it must be a float. 
    orig_shape: tuple[int, int]
    # Mostly being used in tracking # TODO define num and type of items here. 
    data: tuple   # xmin, ymin, xmax, ymax, conf, class
    # GPT said this is better and performance saver. 
    xyxy: tuple[float, float, float, float]   # xmin, ymin, xmax, ymax   

    # TODO, There is another kind of validator, it lets you create a function that takes data, then adjust and return it a BBox instance of this class.
    # Keep this here until i apply it somewhere else.  
    # @field_validator("param_name")
    # def validator(cls):
    #     # Test and raise errors if needed.
    #     pass
    @classmethod
    def from_yolo(cls, idx:int, boxes, names:List[str]) -> "BBox":   # <-  Yes, i know, it is str. 
       id_val = int(boxes.cls[idx].item())     # Required twice.
       return cls(                             # represents the class itself. 
                class_id=id_val,
                class_name=names[id_val],
                conf=boxes.conf[idx].item(),
                orig_shape=boxes.orig_shape,
                data=boxes.data[idx].flatten().tolist(),
                xyxy=boxes.xyxy[idx].flatten().tolist(),
            ) 
    

class DetectionResults(BaseModel):
    """
    You can easily return this to json, using .json to be able to send to API server. 
    """
    detections: List[BBox]