# 📸 Mini Photoshop — Progress Report

> **Mata Kuliah:** Pengolahan Citra Digital
> **Dosen Pengampu:** Rizki Elisa Nalawati, S.T., M.T.
> **Tanggal:** 3 Juni 2026
> **Status Proyek:** ✅ Berjalan — App aktif

---

## 🏗️ Arsitektur Proyek

```text
citra digital/
├── Backend/
│   ├── core/
│   │   ├── image_processing.py (Logika algoritma & CNN Inference)
│   ├── models/
│   │   ├── YOPS.h5 (Model pre-trained 1000 kelas)
│   ├── venv/
│   ├── main.py (FastAPI Routing)
│   ├── requirements.txt
│   ├── run_api.sh
│   ├── run_ngrok.sh
│   └── download_resnet.py
├── src/ (Frontend React)
├── package.json
└── vite.config.ts
```

## Update Terakhir
1. **Refactoring Monorepo:** Memisahkan kode Backend dan Frontend ke dalam foldernya masing-masing agar struktur kode menjadi bersih.
2. **Upgrade Machine Learning:** Mengganti CNN custom `YOPS.h5` dengan arsitektur **ResNet50** yang memiliki bobot pre-trained `ImageNet`. Ini meningkatkan kemampuan deteksi objek dari 10 kategori menjadi **1000 kategori**, sehingga model dapat mengenali objek yang kompleks (termasuk manusia, pakaian, perlengkapan, dll).
3. **Frontend Integration:** Frontend React dikonfigurasi untuk langsung memanggil `http://localhost:8000` alih-alih melalui URL *ngrok* untuk stabilitas koneksi lokal.

**Stack teknologi:** Python · FastAPI · OpenCV · NumPy · TensorFlow / tf-nightly

---

## ✅ Checklist Spesifikasi Dosen

### 1. 🗂️ Image Management

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Load image (JPG, PNG, BMP) | ✅ | `filedialog.askopenfilename` + `cv2.imread` |
| Save image (custom filename & format) | ✅ | `filedialog.asksaveasfilename` + `cv2.imwrite` |
| Reset ke gambar awal | ✅ | `self.current_image = self.cv_img_orig.copy()` |
| Preview: before–after panel | ✅ | Dual card panel (Before / After) di area kanan |

---

### 2. ✨ Image Enhancement

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Brightness & Contrast (slider) | ✅ | `cv2.convertScaleAbs(alpha, beta)` |
| Histogram Equalization | ✅ | YUV-based, channel Y saja → jaga warna |
| Sharpening | ✅ | Kernel laplacian 3×3 via `cv2.filter2D` |
| Smoothing / Blur | ✅ | Average blur 5×5 |

---

### 3. 📐 Geometric Transformation

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Rotate (0°–360°) | ✅ | `getRotationMatrix2D` + `warpAffine` |
| Flip horizontal | ✅ | `cv2.flip(img, 1)` |
| Flip vertikal | ✅ | `cv2.flip(img, 0)` |
| Crop (drag area) | ⚠️ | Auto-crop center 50% *(drag-select belum ada)* |
| Resize (scaling) | ✅ | Slider 10–200%, `cv2.INTER_LINEAR` |
| Translation (geser) | ✅ | Slider X & Y, `warpAffine` translation matrix |
| Transformasi matriks affine | ✅ | Digunakan di Rotate & Translate |
| Interpolasi | ✅ | `cv2.INTER_LINEAR` |

---

### 4. 🔄 Image Restoration (Noise Reduction)

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Gaussian Blur | ✅ | `cv2.GaussianBlur` kernel 5×5 |
| Median Filter | ✅ | `cv2.medianBlur` ksize=5 |
| Noise removal salt & pepper | ✅ | Median Filter efektif untuk salt-&-pepper |

---

### 5. 🔲 Binary & Edge Processing

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Thresholding (binary) | ✅ | `cv2.threshold` nilai 127 |
| Canny Edge | ✅ | Threshold 100–200 |
| Sobel Edge | ✅ | Sobel X + Y → magnitude |
| Prewitt Edge | ✅ | Manual kernel via `filter2D` |
| Robert Edge | ✅ | Kernel cross-gradient 2×2 |
| Laplacian Edge | ✅ | `cv2.Laplacian` + CV_64F |
| LoG (Laplacian of Gaussian) | ✅ | GaussianBlur + Laplacian |
| Morphology Erosion | ✅ | `cv2.erode` kernel 5×5 |
| Morphology Dilation | ✅ | `cv2.dilate` kernel 5×5 |

---

### 6. 🎨 Color Processing

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| RGB → Grayscale | ✅ | `cv2.cvtColor(COLOR_BGR2GRAY)` |
| Channel splitting (R, G, B) | ✅ | `cv2.split` → tampil per channel |
| Color adjustment (hue/saturation) | ✅ | Slider Hue & Saturation via ruang HSV |

---

### 7. 🧩 Image Segmentation

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Threshold-based segmentation | ✅ | Binary thresholding |
| Edge-based segmentation | ✅ | Canny + `findContours` + `drawContours` |
| Region-based sederhana | ✅ | K-Means Clustering (K=4) via `cv2.kmeans` |

---

### 8. 🗜️ Image Compression

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Save kualitas berbeda (low–high) | ✅ | Slider JPEG quality + `cv2.imwrite` |
| Simulasi kompresi JPEG | ✅ | `cv2.imencode` + `imdecode` |
| Metode RLE | ✅ | Simulasi statistik (ratio, segment count) |
| Metode Kuantisasi | ✅ | Reduksi ke 8 level intensitas |
| Huffman / Aritmik / LZW | ⚠️ | Belum diimplementasi *(opsional dari spek)* |

---

### 9. 📊 Histogram Analysis *(Tambahan Penting)*

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Histogram grayscale | ✅ | `ax.hist()` via Matplotlib |
| Perbandingan before–after | ✅ | Dual histogram (ax1 = original, ax2 = edited) |
| Visualisasi Matplotlib embedded | ✅ | `FigureCanvasTkAgg` di dalam Tkinter |
| Update real-time | ✅ | `update_histogram()` dipanggil tiap edit |

---

### 10. 🖥️ User Interface (GUI)

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Menu toolbar (File) | ✅ | File: Open, Save As, Reset, Exit |
| Panel preview before vs after | ✅ | Dual card side-by-side |
| Slider untuk parameter | ✅ | Brightness, Contrast, Rotate, Resize, Translate, HSV, JPEG |
| Tombol aksi cepat | ✅ | Sidebar 8 tab navigasi |

---

### 🤖 Bonus: CNN Object Detection *(Nilai Tambah)*

| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Pengenalan objek dengan CNN | ✅ | MobileNet SSD (Caffe) via `cv2.dnn` |
| Pilih objek untuk direkognisi | ✅ | 20 kelas objek (orang, hewan, kendaraan, dll.) |
| Download model otomatis | ✅ | Auto-download dari GitHub jika belum ada |

**Kelas terdeteksi:** `aeroplane, bicycle, bird, boat, bottle, bus, car, cat, chair, cow, diningtable, dog, horse, motorbike, person, pottedplant, sheep, sofa, train, tvmonitor`

---

## 📊 Ringkasan Kelengkapan

| No | Modul | Fitur Spek | ✅ Done | ⚠️ Partial |
|:---:|---|:---:|:---:|:---:|
| 1 | Image Management | 4 | 4 | 0 |
| 2 | Enhancement | 4 | 4 | 0 |
| 3 | Geometric Transformation | 8 | 7 | 1 |
| 4 | Image Restoration | 3 | 3 | 0 |
| 5 | Binary & Edge Processing | 9 | 9 | 0 |
| 6 | Color Processing | 3 | 3 | 0 |
| 7 | Image Segmentation | 3 | 3 | 0 |
| 8 | Image Compression | 5 | 4 | 1 |
| 9 | Histogram Analysis | 4 | 4 | 0 |
| 10 | GUI | 4 | 4 | 0 |
| 🎁 | CNN Bonus | 3 | 3 | 0 |
| | **TOTAL** | **50** | **48** | **2** |

> **Tingkat kelengkapan: 96%** — Hampir semua fitur spek terpenuhi. 2 item partial (crop drag-select & Huffman/LZW) tidak kritis.

---

## ⚠️ Catatan Item Partial

### 1. Crop — Drag Area
- **Spek:** Crop dengan drag-select area bebas
- **Saat ini:** Auto-crop center 50% (koordinat hardcoded)
- **Dampak:** Fungsional tapi tidak sefleksibel spek

### 2. Kompresi — Huffman / Aritmik / LZW
- **Spek:** "Gunakan metode (Huffman, Aritmik, LZW, RLE, Kuantisasi)"
- **Saat ini:** RLE (statistik) dan Kuantisasi sudah ada
- **Dampak:** Minor, RLE & Kuantisasi sudah cukup membuktikan konsep kompresi

---

## 📁 Statistik Kode

| File | Baris | Fungsi/Method |
|---|---|---|
| `Mini_Photoshop.py` | 28 | 1 class (composer) |
| `image_ops.py` | 414 | ~30 method pemrosesan |
| `ui_layout.py` | 451 | ~15 method UI |
| **Total** | **~893 baris** | **~46 method** |

---

## 🚀 Cara Menjalankan

```bash
# Install dependencies
pip install opencv-python numpy pillow matplotlib python-docx

# Jalankan aplikasi
cd "Documents/citra digital"
python Mini_Photoshop.py
```

---

*Progress Report — Mini Photoshop | Pengolahan Citra Digital | 3 Juni 2026*
