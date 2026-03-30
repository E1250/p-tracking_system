import mlflow

def start_run(camera_id: str):
    return mlflow.start_run(run_name=f"camera_{camera_id}")

def log_config():
    mlflow.log_param("detector", "yolov26_n")
    mlflow.log_param("safety_model", "custom YOLO26_n")
    mlflow.log_param("depth_model", "depthAnything_n")

def log_metrics(metrics:dict):
    for k, v in metrics.items():
        mlflow.log_metric(k, v)