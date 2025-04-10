from fastapi import FastAPI, UploadFile, File, Header, HTTPException, Query
from fastapi.responses import FileResponse
from PIL import Image
import cv2
import numpy as np
import os
import uuid

app = FastAPI()
UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/stitch")
async def stitch_images(
    x_internal_key: str = Header(None),
    format: str = Query("webp", enum=["webp", "jpg", "jpeg"]),
    images: list[UploadFile] = File(...)
):
    if x_internal_key != os.getenv("STITCH_KEY", "dev-secret-key"):
        raise HTTPException(status_code=403, detail="Unauthorized")

    imgs = []
    for image in images:
        contents = await image.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is not None:
            imgs.append(img)

    if len(imgs) < 2:
        raise HTTPException(400, detail="Need at least 2 images")

    stitcher = cv2.Stitcher_create()
    status, stitched = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        raise HTTPException(500, detail="Stitching failed")

    filename = f"{uuid.uuid4().hex}.{format}"
    path = os.path.join(UPLOAD_DIR, filename)

    # Convert OpenCV to PIL and save with desired format
    img_pil = Image.fromarray(cv2.cvtColor(stitched, cv2.COLOR_BGR2RGB))
    img_pil.save(path, format.upper())

    return FileResponse(path, media_type=f"image/{format}", filename=filename)
