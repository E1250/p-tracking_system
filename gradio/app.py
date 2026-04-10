import websockets
import gradio as gr
import asyncio
import requests


def check_backend_health():
    health_url = "https://e1250-tracking-system-backend.hf.space/health/live"
    try:
        response = requests.get(health_url, timeout=5)
        if response.status_code == 200:
            return "Server Online"
        else:
            return "Server Offline"
    except Exception as e:
        return f"Server Error, {e}"


async def send_frame_to_websocket(image_path: str | None, camera_id: str | None):
    if image_path is None:
        raise gr.Error("No Image provided")
    if camera_id is None:
        raise gr.Error("Camera ID is requried")

    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # uri = f"ws://127.0.0.1:8000/detectors/stream/{camera_id}"
    uri = f"wss://e1250-tracking-system-backend.hf.space/detectors/stream/{camera_id}"

    try:
        async with websockets.connect(uri) as websocket:
            await websocket.send(image_bytes)
            gr.Info(f"Frame was sent to {camera_id}..")
            return f"Frame was sent to {camera_id}"
    except Exception as e:
        gr.Error("Error while connecting and sending the frame..")
        return f"Error: {e}"


def wrapper(image, camera_id):
    return asyncio.run(send_frame_to_websocket(image, camera_id))


with gr.Blocks() as demo:
    # On load - Refresh every 60 Seconds
    status_indicator = gr.Markdown("Checking Server Status")
    demo.load(fn=check_backend_health, outputs=status_indicator, every=60)

    gr.Markdown(
        """
        # Tracking System demo  
        A fast way to test the system just by uploading an image, Please make sure you check the guide to be able to use it.
        """
    )

    with gr.Accordion("How to use this system", open=False):
        gr.Markdown(
            """
            1. Make sure first backend is opened [HF Backend](https://huggingface.co/spaces/e1250/tracking_system_backend).
                * If it is inactive, activate it or reach out to me.
                * There is an indicator at the top of the page showing if the server is online or offline
            2. Open Vercel Dashboard and make sure you create a line and place a camera with an id. [Dashboard Vercel](https://p-tracking-system.vercel.app/)
            3. Open Gradio, Make sure you add the same `camera_id`, upload an image, then click send
            4. Go back into the dashboard, Give it couple of seconds (Due to HF env limitation - CPU). then see the updates       
            """
        )

    with gr.Row():
        with gr.Column():
            camera_id = gr.Textbox(
                label="Camera ID", placeholder="Enter Camera ID", value="from_gradio"
            )
            outputs = gr.Textbox(label="Results", value="None")
            send_btn = gr.Button("Send")

        image_input = gr.Image(type="filepath", label="Upload Image")

    send_btn.click(fn=wrapper, inputs=[image_input, camera_id], outputs=outputs)


demo.launch(share=True)
