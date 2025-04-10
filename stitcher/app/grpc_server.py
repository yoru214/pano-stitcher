import grpc
from concurrent import futures
import time
import os
import cv2
import uuid
import numpy as np
from PIL import Image
import stitcher_pb2
import stitcher_pb2_grpc

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class StitcherService(stitcher_pb2_grpc.StitcherServicer):
    def Process(self, request, context):
        if request.key != os.getenv("STITCH_KEY", "dev-secret-key"):
            context.set_code(grpc.StatusCode.PERMISSION_DENIED)
            context.set_details("Invalid key")
            return stitcher_pb2.StitchResponse()

        imgs = []
        for image in request.images:
            npimg = np.frombuffer(image.content, np.uint8)
            img_cv = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            if img_cv is not None:
                imgs.append(img_cv)

        if len(imgs) < 2:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details("Need at least 2 images")
            return stitcher_pb2.StitchResponse()

        stitcher = cv2.Stitcher_create(cv2.Stitcher_PANORAMA)
        status, stitched = stitcher.stitch(imgs)

        if status != cv2.Stitcher_OK:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Stitching failed")
            return stitcher_pb2.StitchResponse()

        format = request.format if request.format in ["webp", "jpg", "jpeg"] else "webp"
        filename = f"{uuid.uuid4().hex}.{format}"
        path = os.path.join(UPLOAD_DIR, filename)

        img_pil = Image.fromarray(cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB))
        img_pil.save(path, format.upper())

        with open(path, "rb") as f:
            stitched_bytes = f.read()

        return stitcher_pb2.StitchResponse(
            filename=filename,
            stitched_image=stitched_bytes,
            content_type=f"image/{format}",
            message="Stitch successful"
        )

def serve_grpc():
    options = [
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),  # 100MB
        ('grpc.max_send_message_length', 100 * 1024 * 1024),     # 100MB
    ]
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=4),
        options=options
    )
    stitcher_pb2_grpc.add_StitcherServicer_to_server(StitcherService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("gRPC Stitcher Server started on port 50051")
    server.wait_for_termination()

