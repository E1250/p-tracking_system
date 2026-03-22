from prometheus_client import Counter, Histogram, Gauge, make_asgi_app

metrics_asgi_app = make_asgi_app()

active_cameras = Gauge(
    "active_camera_connections",
    "Number of Currently Connected camera websockets"
)

active_dashboards = Gauge(
    "active_dashboards",
    "Number of active dashboards which fetching data"
)

frame_processing_duration_seconds = Histogram(
    "frame_processing_duration_seconds",
    "Time to process one frame",
    ["camera_id"]
)

