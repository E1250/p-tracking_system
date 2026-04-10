class ProcessingPipeline:
    def __init__(self, detector, depth_model, safety_detector, redis_client):
        self.detector = detector
        self.depth_model = depth_model
        self.safety_detector = safety_detector
        self.redis_client = redis_client

    async def run(self, camera_id:str, image_array):

        # Run ai models
        # Domain logic
        # save to infra
        pass