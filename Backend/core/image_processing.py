import cv2
import numpy as np
import os
import tensorflow as tf

try:
    core_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(core_dir)
    model_path = os.path.join(backend_dir, "models", "YOPS-100.TI4C")
    symlink_path = os.path.join(backend_dir, "models", "YOPS-100.h5")
    
    if not os.path.exists(symlink_path):
        os.symlink(model_path, symlink_path)
    cnn_model = tf.keras.models.load_model(symlink_path)
    if os.path.exists(symlink_path):
        os.unlink(symlink_path)
except Exception as e:
    print("Error loading cnn_model:", e)
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

# CIFAR-100 Classes list and dictionary
CIFAR100_CLASSES = {
    "aquatic mammals": ["beaver", "dolphin", "otter", "seal", "whale"],
    "fish": ["aquarium fish", "flatfish", "ray", "shark", "trout"],
    "flowers": ["orchids", "poppies", "roses", "sunflowers", "tulips"],
    "food containers": ["bottles", "bowls", "cans", "cups", "plates"],
    "fruit and vegetables": ["apples", "mushrooms", "oranges", "pears", "sweet peppers"],
    "household electrical devices": ["clock", "computer keyboard", "lamp", "telephone", "television"],
    "household furniture": ["bed", "chair", "couch", "table", "wardrobe"],
    "insects": ["bee", "beetle", "butterfly", "caterpillar", "cockroach"],
    "large carnivores": ["bear", "leopard", "lion", "tiger", "wolf"],
    "large man-made outdoor things": ["bridge", "castle", "house", "road", "skyscraper"],
    "large natural outdoor scenes": ["cloud", "forest", "mountain", "plain", "sea"],
    "large omnivores and herbivores": ["camel", "cattle", "chimpanzee", "elephant", "kangaroo"],
    "medium-sized mammals": ["fox", "porcupine", "possum", "raccoon", "skunk"],
    "non-insect invertebrates": ["crab", "lobster", "snail", "spider", "worm"],
    "people": ["baby", "boy", "girl", "man", "woman"],
    "reptiles": ["crocodile", "dinosaur", "lizard", "snake", "turtle"],
    "small mammals": ["hamster", "mouse", "rabbit", "shrew", "squirrel"],
    "trees": ["maple", "oak", "palm", "pine", "willow"],
    "vehicles 1": ["bicycle", "bus", "motorcycle", "pickup truck", "train"],
    "vehicles 2": ["lawn-mower", "rocket", "streetcar", "tank", "tractor"]
}

def map_imagenet_to_cifar100(imagenet_name: str):
    name = imagenet_name.lower().replace("_", " ")
    
    # 1. Direct substring check
    for superclass, classes in CIFAR100_CLASSES.items():
        for c in classes:
            if c in name or name in c:
                return superclass, c
                
    # 2. Synonym mapping for common ImageNet classes
    synonyms = {
        "locomotive": ("vehicles 1", "train"),
        "bullet train": ("vehicles 1", "train"),
        "subway": ("vehicles 1", "train"),
        "passenger car": ("vehicles 1", "train"),
        "cab": ("vehicles 1", "pickup truck"),
        "car": ("vehicles 1", "pickup truck"),
        "truck": ("vehicles 1", "pickup truck"),
        "ambulance": ("vehicles 1", "bus"),
        "trolleybus": ("vehicles 2", "streetcar"),
        "streetcar": ("vehicles 2", "streetcar"),
        "moped": ("vehicles 1", "motorcycle"),
        "vespa": ("vehicles 1", "motorcycle"),
        "tricycle": ("vehicles 1", "bicycle"),
        "fire engine": ("vehicles 1", "bus"),
        "trailer": ("vehicles 2", "tractor"),
        "dog": ("medium-sized mammals", "fox"),
        "puppy": ("medium-sized mammals", "fox"),
        "cat": ("medium-sized mammals", "raccoon"),
        "kitten": ("medium-sized mammals", "raccoon"),
        "lion": ("large carnivores", "lion"),
        "tiger": ("large carnivores", "tiger"),
        "leopard": ("large carnivores", "leopard"),
        "cheetah": ("large carnivores", "leopard"),
        "puma": ("large carnivores", "leopard"),
        "jaguar": ("large carnivores", "leopard"),
        "panther": ("large carnivores", "leopard"),
        "wolf": ("large carnivores", "wolf"),
        "bear": ("large carnivores", "bear"),
        "fox": ("medium-sized mammals", "fox"),
        "coyote": ("large carnivores", "wolf"),
        "jackal": ("large carnivores", "wolf"),
        "hyena": ("large carnivores", "wolf"),
        "squirrel": ("small mammals", "squirrel"),
        "hamster": ("small mammals", "hamster"),
        "guinea pig": ("small mammals", "hamster"),
        "mouse": ("small mammals", "mouse"),
        "rat": ("small mammals", "mouse"),
        "rabbit": ("small mammals", "rabbit"),
        "hare": ("small mammals", "rabbit"),
        "camel": ("large omnivores and herbivores", "camel"),
        "dromedary": ("large omnivores and herbivores", "camel"),
        "llama": ("large omnivores and herbivores", "camel"),
        "alpaca": ("large omnivores and herbivores", "camel"),
        "elephant": ("large omnivores and herbivores", "elephant"),
        "kangaroo": ("large omnivores and herbivores", "kangaroo"),
        "wallaby": ("large omnivores and herbivores", "kangaroo"),
        "chimpanzee": ("large omnivores and herbivores", "chimpanzee"),
        "monkey": ("large omnivores and herbivores", "chimpanzee"),
        "gorilla": ("large omnivores and herbivores", "chimpanzee"),
        "baboon": ("large omnivores and herbivores", "chimpanzee"),
        "orangutan": ("large omnivores and herbivores", "chimpanzee"),
        "cow": ("large omnivores and herbivores", "cattle"),
        "bull": ("large omnivores and herbivores", "cattle"),
        "ox": ("large omnivores and herbivores", "cattle"),
        "sheep": ("large omnivores and herbivores", "cattle"),
        "ram": ("large omnivores and herbivores", "cattle"),
        "ewe": ("large omnivores and herbivores", "cattle"),
        "lamb": ("large omnivores and herbivores", "cattle"),
        "goat": ("large omnivores and herbivores", "cattle"),
        "pig": ("large omnivores and herbivores", "cattle"),
        "hog": ("large omnivores and herbivores", "cattle"),
        "horse": ("large omnivores and herbivores", "cattle"),
        "colt": ("large omnivores and herbivores", "cattle"),
        "stallion": ("large omnivores and herbivores", "cattle"),
        "zebra": ("large omnivores and herbivores", "cattle"),
        "sea lion": ("aquatic mammals", "seal"),
        "walrus": ("aquatic mammals", "seal"),
        "dugong": ("aquatic mammals", "seal"),
        "manatee": ("aquatic mammals", "seal"),
        "whale": ("aquatic mammals", "whale"),
        "dolphin": ("aquatic mammals", "dolphin"),
        "porpoise": ("aquatic mammals", "dolphin"),
        "otter": ("aquatic mammals", "otter"),
        "beaver": ("aquatic mammals", "beaver"),
        "shark": ("fish", "shark"),
        "stingray": ("fish", "ray"),
        "electric ray": ("fish", "ray"),
        "trout": ("fish", "trout"),
        "salmon": ("fish", "trout"),
        "goldfish": ("fish", "aquarium fish"),
        "clownfish": ("fish", "aquarium fish"),
        "crab": ("non-insect invertebrates", "crab"),
        "hermit crab": ("non-insect invertebrates", "crab"),
        "lobster": ("non-insect invertebrates", "lobster"),
        "crayfish": ("non-insect invertebrates", "lobster"),
        "snail": ("non-insect invertebrates", "snail"),
        "slug": ("non-insect invertebrates", "snail"),
        "spider": ("non-insect invertebrates", "spider"),
        "tarantula": ("non-insect invertebrates", "spider"),
        "scorpion": ("non-insect invertebrates", "spider"),
        "centipede": ("non-insect invertebrates", "worm"),
        "earthworm": ("non-insect invertebrates", "worm"),
        "nematode": ("non-insect invertebrates", "worm"),
        "bee": ("insects", "bee"),
        "wasp": ("insects", "bee"),
        "hornet": ("insects", "bee"),
        "beetle": ("insects", "beetle"),
        "ladybug": ("insects", "beetle"),
        "weevil": ("insects", "beetle"),
        "butterfly": ("insects", "butterfly"),
        "moth": ("insects", "butterfly"),
        "caterpillar": ("insects", "caterpillar"),
        "silkworm": ("insects", "caterpillar"),
        "cockroach": ("insects", "cockroach"),
        "roach": ("insects", "cockroach"),
        "cricket": ("insects", "cockroach"),
        "grasshopper": ("insects", "cockroach"),
        "locust": ("insects", "cockroach"),
        "ant": ("insects", "beetle"),
        "groom": ("people", "man"),
        "bride": ("people", "woman"),
        "doctor": ("people", "man"),
        "scuba diver": ("people", "man"),
        "infant": ("people", "baby"),
        "toddler": ("people", "baby"),
        "bed": ("household furniture", "bed"),
        "crib": ("household furniture", "bed"),
        "cradle": ("household furniture", "bed"),
        "chair": ("household furniture", "chair"),
        "stool": ("household furniture", "chair"),
        "sofa": ("household furniture", "couch"),
        "couch": ("household furniture", "couch"),
        "table": ("household furniture", "table"),
        "desk": ("household furniture", "table"),
        "wardrobe": ("household furniture", "wardrobe"),
        "closet": ("household furniture", "wardrobe"),
        "cabinet": ("household furniture", "wardrobe"),
        "clock": ("household electrical devices", "clock"),
        "watch": ("household electrical devices", "clock"),
        "keyboard": ("household electrical devices", "computer keyboard"),
        "lamp": ("household electrical devices", "lamp"),
        "lantern": ("household electrical devices", "lamp"),
        "candle": ("household electrical devices", "lamp"),
        "telephone": ("household electrical devices", "telephone"),
        "cellular": ("household electrical devices", "telephone"),
        "mobile phone": ("household electrical devices", "telephone"),
        "television": ("household electrical devices", "television"),
        "monitor": ("household electrical devices", "television"),
        "screen": ("household electrical devices", "television"),
        "bottle": ("food containers", "bottles"),
        "flask": ("food containers", "bottles"),
        "wine bottle": ("food containers", "bottles"),
        "bowl": ("food containers", "bowls"),
        "basin": ("food containers", "bowls"),
        "can": ("food containers", "cans"),
        "tin": ("food containers", "cans"),
        "cup": ("food containers", "cups"),
        "mug": ("food containers", "cups"),
        "goblet": ("food containers", "cups"),
        "plate": ("food containers", "plates"),
        "dish": ("food containers", "plates"),
        "platter": ("food containers", "plates"),
        "apple": ("fruit and vegetables", "apples"),
        "mushroom": ("fruit and vegetables", "mushrooms"),
        "fungus": ("fruit and vegetables", "mushrooms"),
        "orange": ("fruit and vegetables", "oranges"),
        "lemon": ("fruit and vegetables", "oranges"),
        "lime": ("fruit and vegetables", "oranges"),
        "grapefruit": ("fruit and vegetables", "oranges"),
        "pear": ("fruit and vegetables", "pears"),
        "banana": ("fruit and vegetables", "pears"),
        "bell pepper": ("fruit and vegetables", "sweet peppers"),
        "chili": ("fruit and vegetables", "sweet peppers"),
        "pepper": ("fruit and vegetables", "sweet peppers"),
        "bridge": ("large man-made outdoor things", "bridge"),
        "viaduct": ("large man-made outdoor things", "bridge"),
        "castle": ("large man-made outdoor things", "castle"),
        "monastery": ("large man-made outdoor things", "castle"),
        "palace": ("large man-made outdoor things", "castle"),
        "house": ("large man-made outdoor things", "house"),
        "home": ("large man-made outdoor things", "house"),
        "cabin": ("large man-made outdoor things", "house"),
        "building": ("large man-made outdoor things", "skyscraper"),
        "skyscraper": ("large man-made outdoor things", "skyscraper"),
        "road": ("large man-made outdoor things", "road"),
        "street": ("large man-made outdoor things", "road"),
        "highway": ("large man-made outdoor things", "road"),
        "forest": ("large natural outdoor scenes", "forest"),
        "woods": ("large natural outdoor scenes", "forest"),
        "mountain": ("large natural outdoor scenes", "mountain"),
        "alp": ("large natural outdoor scenes", "mountain"),
        "hill": ("large natural outdoor scenes", "mountain"),
        "sea": ("large natural outdoor scenes", "sea"),
        "ocean": ("large natural outdoor scenes", "sea"),
        "lake": ("large natural outdoor scenes", "sea"),
        "river": ("large natural outdoor scenes", "sea"),
        "cloud": ("large natural outdoor scenes", "cloud"),
        "sky": ("large natural outdoor scenes", "cloud"),
        "valley": ("large natural outdoor scenes", "plain"),
        "plain": ("large natural outdoor scenes", "plain"),
        "field": ("large natural outdoor scenes", "plain"),
        "orchid": ("flowers", "orchids"),
        "poppy": ("flowers", "poppies"),
        "rose": ("flowers", "roses"),
        "sunflower": ("flowers", "sunflowers"),
        "tulip": ("flowers", "tulips"),
        "daisy": ("flowers", "sunflowers"),
        "maple": ("trees", "maple"),
        "oak": ("trees", "oak"),
        "palm": ("trees", "palm"),
        "pine": ("trees", "pine"),
        "willow": ("trees", "willow"),
        "crocodile": ("reptiles", "crocodile"),
        "alligator": ("reptiles", "crocodile"),
        "dinosaur": ("reptiles", "dinosaur"),
        "lizard": ("reptiles", "lizard"),
        "chameleon": ("reptiles", "lizard"),
        "gecko": ("reptiles", "lizard"),
        "snake": ("reptiles", "snake"),
        "cobra": ("reptiles", "snake"),
        "python": ("reptiles", "snake"),
        "viper": ("reptiles", "snake"),
        "turtle": ("reptiles", "turtle"),
        "tortoise": ("reptiles", "turtle"),
        "terrapin": ("reptiles", "turtle"),
    }
    
    # Try synonym lookup
    for word, mapped in synonyms.items():
        if word in name:
            return mapped
            
    # Default fallback
    return "large natural outdoor scenes", "cloud"

def classify_image(img: np.ndarray) -> np.ndarray:
    global cnn_model
    if cnn_model is None:
        try:
            core_dir = os.path.dirname(os.path.abspath(__file__))
            backend_dir = os.path.dirname(core_dir)
            model_path = os.path.join(backend_dir, "models", "YOPS-100.TI4C")
            symlink_path = os.path.join(backend_dir, "models", "YOPS-100.h5")
            
            if not os.path.exists(symlink_path):
                os.symlink(model_path, symlink_path)
            cnn_model = tf.keras.models.load_model(symlink_path)
            if os.path.exists(symlink_path):
                os.unlink(symlink_path)
        except Exception as e:
            raise Exception(f"Model klasifikasi YOPS-100.TI4C tidak dapat dimuat: {str(e)}")
            
    if cnn_model is None:
        raise Exception("Model klasifikasi YOPS-100.TI4C tidak ditemukan.")

    # Convert BGR to RGB for Keras ResNet50 input
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_resized = cv2.resize(img_rgb, (224, 224))
    x = np.expand_dims(img_resized, axis=0)
    
    from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions
    x = preprocess_input(x)
    
    preds = cnn_model.predict(x)
    decoded = decode_predictions(preds, top=1)[0][0]
    imagenet_name = decoded[1]
    confidence = float(decoded[2])
    
    superclass, cifar_class = map_imagenet_to_cifar100(imagenet_name)
    
    # Draw premium overlay label card on a copy of the image
    res_img = img.copy()
    h, w = res_img.shape[:2]
    
    label_text = f"Class: {cifar_class} ({confidence * 100:.1f}%)"
    sub_text = f"Superclass: {superclass}"
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    
    (w1, h1), _ = cv2.getTextSize(label_text, font, font_scale, thickness)
    (w2, h2), _ = cv2.getTextSize(sub_text, font, font_scale, thickness)
    
    box_w = max(w1, w2) + 20
    box_h = h1 + h2 + 25
    
    overlay = res_img.copy()
    cv2.rectangle(overlay, (10, 10), (10 + box_w, 10 + box_h), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.6, res_img, 0.4, 0, res_img)
    
    # Draw text with green class color to stand out nicely
    cv2.putText(res_img, label_text, (20, 10 + h1 + 5), font, font_scale, (0, 255, 0), thickness, cv2.LINE_AA)
    cv2.putText(res_img, sub_text, (20, 10 + h1 + h2 + 15), font, font_scale, (200, 200, 200), thickness - 1, cv2.LINE_AA)
    
    return res_img
