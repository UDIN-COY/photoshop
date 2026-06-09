import io
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import core.image_processing as ip

app = FastAPI(title="Mini Photoshop Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def decode_image(file_bytes: bytes) -> np.ndarray:
    nparr = np.frombuffer(file_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise HTTPException(status_code=400, detail="Invalid image file")
    return img

def encode_image(img: np.ndarray, format: str = ".jpg") -> io.BytesIO:
    success, encoded_img = cv2.imencode(format, img)
    if not success:
        raise HTTPException(status_code=500, detail="Could not encode image")
    return io.BytesIO(encoded_img.tobytes())

@app.get("/")
def read_root():
    return {"message": "Mini Photoshop API is running."}

# 2. Image Enhancement
@app.post("/api/enhance/brightness-contrast")
async def enhance_brightness_contrast(file: UploadFile = File(...), brightness: int = Form(0), contrast: int = Form(0)):
    img = decode_image(await file.read())
    res = ip.apply_brightness_contrast(img, brightness, contrast)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/enhance/equalize")
async def enhance_equalize(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_hist_eq(img)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/enhance/sharpen")
async def enhance_sharpen(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_sharpen(img)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/enhance/smooth")
async def enhance_smooth(file: UploadFile = File(...), ftype: str = Form("gaussian")):
    img = decode_image(await file.read())
    res = ip.apply_blur(img, ftype)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 3. Geometric Transformation
@app.post("/api/geom/rotate")
async def geom_rotate(file: UploadFile = File(...), angle: float = Form(0)):
    img = decode_image(await file.read())
    res = ip.apply_rotate(img, angle)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/geom/flip")
async def geom_flip(file: UploadFile = File(...), mode: int = Form(1)): # 1 horizontal, 0 vertical, -1 both
    print(f"--- geom_flip API called with mode={mode} ---")
    img = decode_image(await file.read())
    print(f"Original image shape: {img.shape}")
    res = ip.apply_flip(img, mode)
    print(f"Flipped image shape: {res.shape}")
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/geom/crop")
async def geom_crop(file: UploadFile = File(...), x1: int = Form(...), y1: int = Form(...), x2: int = Form(...), y2: int = Form(...)):
    img = decode_image(await file.read())
    res = ip.apply_crop(img, x1, y1, x2, y2)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/geom/resize")
async def geom_resize(file: UploadFile = File(...), scale: float = Form(1.0)):
    img = decode_image(await file.read())
    res = ip.apply_resize(img, scale)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/geom/translate")
async def geom_translate(file: UploadFile = File(...), tx: float = Form(0), ty: float = Form(0)):
    img = decode_image(await file.read())
    res = ip.apply_translation(img, tx, ty)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 4. Restoration
@app.post("/api/restore/gaussian")
async def restore_gaussian(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_blur(img, "gaussian")
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/restore/median")
async def restore_median(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_blur(img, "median")
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 5. Binary & Edge Processing
@app.post("/api/edge/threshold")
async def edge_threshold(file: UploadFile = File(...), thresh_val: int = Form(127)):
    img = decode_image(await file.read())
    res = ip.apply_threshold(img, thresh_val)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/edge/detect")
async def edge_detect(file: UploadFile = File(...), etype: str = Form("canny")):
    img = decode_image(await file.read())
    res = ip.apply_edge(img, etype)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/morphology")
async def morphology(file: UploadFile = File(...), mtype: str = Form("erosion"), kernel_size: int = Form(5)):
    img = decode_image(await file.read())
    res = ip.apply_morph(img, mtype, kernel_size)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 6. Color Processing
@app.post("/api/color/grayscale")
async def color_grayscale(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_grayscale(img)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/color/split-channel")
async def color_split(file: UploadFile = File(...), channel: int = Form(0)):
    img = decode_image(await file.read())
    res = ip.split_channel(img, channel)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/color/hsv-adjust")
async def color_hsv(file: UploadFile = File(...), hue_shift: int = Form(0), sat_shift: int = Form(0)):
    img = decode_image(await file.read())
    res = ip.apply_hsv(img, hue_shift, sat_shift)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 7. Image Segmentation
@app.post("/api/segment/kmeans")
async def segment_kmeans(file: UploadFile = File(...), k: int = Form(4)):
    img = decode_image(await file.read())
    res = ip.apply_kmeans(img, k)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/segment/edge-based")
async def segment_edge(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    res = ip.apply_edge_segmentation(img)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 8. Image Compression
@app.post("/api/compress/simulate")
async def compress_simulate(file: UploadFile = File(...), quality: int = Form(50)):
    img = decode_image(await file.read())
    res = ip.simulate_jpeg(img, quality)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

@app.post("/api/compress/quantize")
async def compress_quantize(file: UploadFile = File(...), levels: int = Form(8)):
    img = decode_image(await file.read())
    res = ip.simulate_quantization(img, levels)
    return StreamingResponse(encode_image(res), media_type="image/jpeg")

# 9. Histogram Analysis
@app.post("/api/histogram")
async def histogram_analysis(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    hist_data = ip.get_histogram_data(img)
    return JSONResponse(content={"histogram": hist_data})

# 11. ML Object Detection
@app.post("/api/ml/detect-objects")
async def ml_detect(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    try:
        res = ip.detect_objects(img)
        return StreamingResponse(encode_image(res), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ml/classify-image")
async def ml_classify(file: UploadFile = File(...)):
    img = decode_image(await file.read())
    try:
        res = ip.classify_image(img)
        return StreamingResponse(encode_image(res), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
