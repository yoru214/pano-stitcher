import grpc
import os
import stitcher_pb2
import stitcher_pb2_grpc
from PIL import Image

# Set up gRPC channel and stub
options = [
    ('grpc.max_receive_message_length', 100 * 1024 * 1024),
    ('grpc.max_send_message_length', 100 * 1024 * 1024),
]
channel = grpc.insecure_channel("localhost:50051", options=options)
stub = stitcher_pb2_grpc.StitcherStub(channel)

# Auto-load all .jpg, .jpeg, .png from the test_images folder
image_folder = "./images/src"
allowed_ext = [".jpg", ".jpeg", ".png"]
image_paths = [
    os.path.join(image_folder, f)
    for f in os.listdir(image_folder)
    if os.path.splitext(f)[1].lower() in allowed_ext
]

# Prepare the images
images = []
for path in image_paths:
    with open(path, "rb") as f:
        content = f.read()
        images.append(stitcher_pb2.ImageData(
            filename=os.path.basename(path),
            content=content
        ))

# Build the gRPC request
request = stitcher_pb2.StitchRequest(
    images=images,
    format="webp",
    key="dev-secret-key"
)

# Call the API
try:
    response = stub.Process(request)
    print("✅ Stitch successful")

    # Ask for filename and format
    output_dir = "./images/output"
    os.makedirs(output_dir, exist_ok=True)
    suggested_name = os.path.splitext(response.filename)[0]

    user_filename = input(f"\nSave file as (default: {suggested_name}): ").strip()
    if not user_filename:
        user_filename = suggested_name

    # Ask for format
    user_format = input("Save format? [webp/jpeg] (default: webp): ").strip().lower()
    if user_format not in ["jpeg", "jpg"]:
        user_format = "webp"
    ext = ".jpeg" if user_format == "jpeg" or user_format == "jpg" else ".webp"

    filename = user_filename + ext
    output_path = os.path.join(output_dir, filename)

    # Save image using Pillow to chosen format
    from io import BytesIO
    img_pil = Image.open(BytesIO(response.stitched_image))
    img_pil.save(output_path, user_format.upper())

    print(f"✅ Saved stitched image to {output_path}")

except grpc.RpcError as e:
    print("❌ gRPC error:", e.code(), e.details())