from ai.detectors.yolo_detector import YOLO_Detector
from app.config import AppConfig
from ultralytics.utils.plotting import Annotator
import cv2 as cv

test_image = r"G:\MyComputer\Workspace\Projects\gp-tracking-dashboard\tracking_dashboard\ai\dummy_data\home fire smoke.jpg"

config = AppConfig()
annotator = Annotator(cv.imread(test_image))

# Person Detector
# yolo_detector = YOLO_Detector(model_path=config.yolo.model_path)
# Fire-Smoke Detector
yolo_detector = YOLO_Detector(model_path=r"G:\MyComputer\Workspace\Projects\gp-tracking-dashboard\tracking_dashboard\ai\dl_models\yolo_smoke_fire.pt")

detections = yolo_detector.detect(test_image).detections

for det in detections:
    print()
    annotator.box_label(det.xyxy, label=f'{det.class_name}')

output_image = annotator.result()
cv.imshow("Annotation", output_image)
cv.waitKey(0)
cv.destroyAllWindows()