import cv2
import numpy as np
import os
import tensorflow as tf

try:
    cnn_model = tf.keras.models.load_model("models/YOPS.h5")
except:
    cnn_model = None

# 1 & 2. Image Enhancement
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

# 3. Geometric Transformation
def apply_rotate(image: np.ndarray, angle: float) -> np.ndarray:
    h, w = image.shape[:2]
    mtx = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
    return cv2.warpAffine(image, mtx, (w, h))

def apply_flip(image: np.ndarray, mode: int) -> np.ndarray:
    return cv2.flip(image, mode)

def apply_crop(image: np.ndarray, x1: int, y1: int, x2: int, y2: int) -> np.ndarray:
    h, w = image.shape[:2]
    # boundary check
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

# 5. Binary & Edge Processing
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

# 6. Color Processing
def apply_grayscale(image: np.ndarray) -> np.ndarray:
    if len(image.shape) == 3:
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return image

def split_channel(image: np.ndarray, channel: int) -> np.ndarray:
    # channel: 0=Blue, 1=Green, 2=Red
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

# 9. Histogram Analysis
def get_histogram_data(image: np.ndarray) -> list:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if len(image.shape) == 3 else image
    hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
    return [int(x[0]) for x in hist]

# 11. Object Detection (CNN via ResNet50)
def detect_objects(img, prototxt=None, model=None):
    if cnn_model is None:
        raise Exception("Model YOPS tidak ditemukan di models/YOPS.h5!")
    
    # Preprocess gambar untuk ResNet50 (resize ke 224x224, konversi ke float)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    img_array = np.expand_dims(img_resized, axis=0) # (1, 224, 224, 3)
    
    # Normalisasi khusus ResNet50
    img_array = tf.keras.applications.resnet50.preprocess_input(img_array.astype(np.float32))
    
    # Prediksi menggunakan ResNet50
    prediction = cnn_model.predict(img_array, verbose=0)
    
    # Decode hasil prediksi ke nama kategori (Top 1)
    decoded = tf.keras.applications.resnet50.decode_predictions(prediction, top=1)[0][0]
    class_id, class_name, confidence = decoded
    
    # Ganti underscore dengan spasi agar lebih cantik
    class_name = class_name.replace('_', ' ').title()
    label = f"Prediksi: {class_name} ({confidence*100:.1f}%)"
    
    # Warna emas elegan
    color = (0, 215, 255)
        
    # Tulis hasil prediksi di gambar dengan font yang lebih jelas
    res_img = img.copy()
    
    # Background untuk teks agar mudah dibaca di gambar terang/gelap
    (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 3)
    cv2.rectangle(res_img, (15, 15), (25 + text_w, 55 + text_h), (0, 0, 0), -1)
    
    cv2.putText(res_img, label, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)
    return res_img
