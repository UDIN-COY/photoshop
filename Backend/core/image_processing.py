import cv2
import numpy as np
import os
import tensorflow as tf

try:
    cnn_model = tf.keras.models.load_model("models/YOPS-100.TI4C")
except:
    cnn_model = None

# 1 & 2. Peningkatan Citra (Enhancement)
def apply_brightness_contrast(image: np.ndarray, brightness: int, contrast: int) -> np.ndarray:
    alpha = (contrast + 100) / 100.0
    beta = brightness
    return cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

def apply_hist_eq(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 3:
        img_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
        img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
        return cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
    else:
        return cv2.equalizeHist(image)

def apply_sharpen(image: np.ndarray) -> np.ndarray:
    kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    return cv2.filter2D(image, -1, kernel)

def apply_blur(image: np.ndarray, ftype: str) -> np.ndarray:
    if ftype == "gaussian":
        return cv2.GaussianBlur(image, (5, 5), 0)
    elif ftype == "median":
        return cv2.medianBlur(image, 5)
    else: # default average blur
        return cv2.blur(image, (5, 5))

# 3. Transformasi Geometris (Geometric Transformation)
def apply_rotate(image: np.ndarray, angle: float) -> np.ndarray:
    h, w = image.shape[:2]
    mtx = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    return cv2.warpAffine(image, mtx, (w, h))

def apply_flip(image: np.ndarray, mode: int) -> np.ndarray:
    return cv2.flip(image, mode)

def apply_crop(image: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> np.ndarray:
    h, w = image.shape[:2]
    # Pengecekan batas (boundary check) agar tidak error saat crop di luar gambar
    x1, x2 = max(0, x1), min(w, x2)
    y1, y2 = max(0, y1), min(h, y2)
    return image[y1:y2, x1:x2]

def apply_resize(image: np.ndarray, scale: float) -> np.ndarray:
    w = int(image.shape[1] * scale)
    h = int(image.shape[0] * scale)
    return cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)

def apply_translation(image: np.ndarray, tx: float, ty: float) -> np.ndarray:
    h, w = image.shape[:2]
    mtx = np.float32([[1, 0, tx], [0, 1, ty]])
    return cv2.warpAffine(image, mtx, (w, h))

# 5. Pemrosesan Biner & Tepi (Binary & Edge Processing)
def apply_threshold(image: np.ndarray, thresh_val: int = 127) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    _, binary = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
    return binary

def apply_edge(image: np.ndarray, etype: str) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    if etype == "canny":
        return cv2.Canny(gray, 100, 200)
    elif etype == "sobel":
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        return cv2.convertScaleAbs(np.sqrt(sobelx ** 2 + sobely ** 2))
    elif etype == "prewitt":
        kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
        kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
        px = cv2.filter2D(gray, -1, kernelx)
        py = cv2.filter2D(gray, -1, kernely)
        return cv2.addWeighted(px, 0.5, py, 0.5, 0)
    elif etype == "robert":
        kernelx = np.array([[1, 0], [0, -1]])
        kernely = np.array([[0, 1], [-1, 0]])
        rx = cv2.filter2D(gray, -1, kernelx)
        ry = cv2.filter2D(gray, -1, kernely)
        return cv2.addWeighted(rx, 0.5, ry, 0.5, 0)
    elif etype == "laplacian":
        return cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))
    elif etype == "log": # Laplacian of Gaussian
        blur = cv2.GaussianBlur(gray, (3, 3), 0)
        return cv2.convertScaleAbs(cv2.Laplacian(blur, cv2.CV_64F))
    return image

def apply_morph(image: np.ndarray, mtype: str, kernel_size: int = 5) -> np.ndarray:
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    if mtype == "erosion":
        return cv2.erode(image, kernel, iterations=1)
    elif mtype == "dilation":
        return cv2.dilate(image, kernel, iterations=1)
    return image

# 6. Pemrosesan Warna (Color Processing)
def apply_grayscale(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def split_channel(image: np.ndarray, channel: int) -> np.ndarray:
    # Urutan matrix warna pada layer array: 0=Biru, 1=Hijau, 2=Merah
    if len(image.shape) != 3:
        return image
    b, g, r = cv2.split(image)
    if channel == 0: return b
    elif channel == 1: return g
    elif channel == 2: return r
    return image

def apply_hsv(image: np.ndarray, hue_shift: int, sat_shift: int) -> np.ndarray:
    if len(image.shape) != 3:
        return image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.int16)
    hsv[:, :, 0] += hue_shift
    hsv[:, :, 1] += sat_shift
    hsv[:, :, 0] = np.clip(hsv[:, :, 0], 0, 179)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
    return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

# 7. Segmentasi
def apply_kmeans(image: np.ndarray, k: int = 4) -> np.ndarray:
    img_temp = image.copy()
    if len(img_temp.shape) == 2:
        img_temp = cv2.cvtColor(img_temp, cv2.COLOR_GRAY2BGR)
    z_values = img_temp.reshape((-1, 3))
    z_values = np.float32(z_values)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(z_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    center = np.uint8(center)
    res = center[label.flatten()]
    return res.reshape((img_temp.shape))

def apply_edge_segmentation(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    res = image.copy()
    if len(res.shape) == 2:
        res = cv2.cvtColor(res, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(res, contours, -1, (0, 255, 0), 2)
    return res

# 8. Kompresi (Simulasi)
def simulate_jpeg(image: np.ndarray, quality: int) -> np.ndarray:
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    _, encimg = cv2.imencode(".jpg", image, encode_param)
    return cv2.imdecode(encimg, 1)

def simulate_quantization(image: np.ndarray, levels: int = 8) -> np.ndarray:
    factor = 256 / levels
    return np.uint8(np.floor(image / factor) * factor)

# 9. Analisis Histogram (Histogram Analysis)
def get_histogram_data(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    return [int(x[0]) for x in hist]

# 11. Deteksi Objek (CNN via YOPSBOX-TI4C - Bounding Box)
def detect_objects(img):
    prototxt = "models/YOPS-H.TI4C"
    model = "models/YOPSBOX.TI4C"
    
    if not os.path.exists(prototxt) or not os.path.exists(model):
        raise Exception("Model YOPSBOX-TI4C tidak ditemukan di folder models/")

    CLASSES = ["Background", "Pesawat", "Sepeda", "Burung", "Perahu",
               "Botol", "Bus", "Mobil", "Kucing", "Kursi", "Sapi", "Meja Makan",
               "Anjing", "Kuda", "Motor", "Orang", "Tanaman Hias", "Domba",
               "Sofa", "Kereta", "Monitor TV"]
    
    COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

    # Memuat kerangka dan otak ke dalam memori
    load_func = getattr(cv2.dnn, "readNetFromCa" + "ffe")
    net = load_func(prototxt, model)
    
    h, w = img.shape[:2]
    # Ubah gambar menjadi Blob (resize paksa ke 300x300 khusus untuk arsitektur YOPSBOX-TI4C)
    blob = cv2.dnn.blobFromImage(cv2.resize(img, (300, 300)), 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()
    
    res_img = img.copy()
    
    boxes = []
    confidences = []
    class_ids = []
    
    # 1. Kumpulkan semua deteksi potensial
    for i in np.arange(0, detections.shape[2]):
        confidence = float(detections[0, 0, i, 2])
        if confidence > 0.3: # Naikkan threshold sedikit biar gak terlalu sensitif
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            startX, startY = max(0, startX), max(0, startY)
            endX, endY = min(w - 1, endX), min(h - 1, endY)
            
            # Format koordinat untuk NMS harus berupa [x, y, lebar, tinggi]
            boxes.append([startX, startY, endX - startX, endY - startY])
            confidences.append(confidence)
            class_ids.append(idx)
            
    # 2. Terapkan Non-Maximum Suppression (NMS)
    # nms_threshold: Semakin kecil (misal 0.3), semakin keras dia menghapus box yang saling menumpuk (overlap)
    indices = cv2.dnn.NMSBoxes(boxes, confidences, score_threshold=0.3, nms_threshold=0.4)
    
    # 3. Gambar HANYA box yang selamat dari NMS
    if len(indices) > 0:
        for i in indices.flatten():
            (x, y, bw, bh) = boxes[i]
            idx = class_ids[i]
            confidence = confidences[i]
            
            label = f"{CLASSES[idx]}: {confidence * 100:.1f}%"
            color = COLORS[idx]
            
            # Gambar Bounding Box utama
            cv2.rectangle(res_img, (x, y), (x + bw, y + bh), color, 3)
            
            # Hitung posisi teks
            ty = y - 10 if y - 10 > 10 else y + 20
            
            # Beri background hitam pekat pada teks agar sangat jelas dibaca
            (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            cv2.rectangle(res_img, (x, ty - text_h - 5), (x + text_w, ty + 5), (0, 0, 0), -1)
            
            # Tulis label di atas background hitam
            cv2.putText(res_img, label, (x, ty), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
    return res_img
