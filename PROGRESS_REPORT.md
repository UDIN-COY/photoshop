# 📸 Mini Photoshop Web — Progress Report

> **Mata Kuliah:** Pengolahan Citra Digital
> **Dosen Pengampu:** Rizki Elisa Nalawati, S.T., M.T.
> **Tanggal:** 9 Juni 2026
> **Status Proyek:** ✅ Berjalan — Full Stack Web App aktif

---

## 🏗️ Arsitektur Proyek

```text
citra digital/
├── Backend/
│   ├── core/
│   │   └── image_processing.py (Logika algoritma OpenCV & CNN Inference)
│   ├── models/
│   │   ├── YOPS-100.TI4C (Model klasifikasi gambar)
│   │   ├── YOPS-H.TI4C (Kerangka CNN Bounding Box)
│   │   └── YOPSBOX.TI4C (Otak CNN Bounding Box)
│   ├── venv/
│   ├── main.py (FastAPI Routing)
│   ├── train_yops_model.py (Script dokumentasi training CNN)
│   ├── requirements.txt
│   └── run_api.sh
├── src/ (Frontend React + Vite)
├── package.json
└── vite.config.ts
```

## Update Terakhir
1. **Refactoring ke Web App:** Memindahkan aplikasi desktop lama (Tkinter) menjadi aplikasi **Full Stack Web App** modern berbasis React (Vite) dan FastAPI (Python).
2. **Upgrade Machine Learning:** Menggunakan arsitektur CNN kustom **YOPSBOX-TI4C** yang dioptimasi untuk melakukan deteksi objek dengan *Bounding Box* (kotak pembatas) dan menyeleksi objek menggunakan *Non-Maximum Suppression (NMS)*.
3. **Lokalisasi Model:** Mengubah seluruh kelas prediksi model ke dalam bahasa Indonesia untuk kemudahan penggunaan.

**Stack teknologi:** React · TailwindCSS · Python · FastAPI · OpenCV · NumPy · TensorFlow

---

## ✅ Checklist Spesifikasi Dosen

### 1. 🗂️ Image Management
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Load image (Upload Form) | ✅ | `<input type="file">` + `FastAPI UploadFile` |
| Save image | ✅ | Tombol Download di UI React |
| Preview: before–after panel | ✅ | Dual image display (Before / After) di layar |

### 2. ✨ Image Enhancement
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Brightness & Contrast (slider) | ✅ | `cv2.convertScaleAbs(alpha, beta)` |
| Histogram Equalization | ✅ | YUV-based, channel Y saja → jaga warna |
| Sharpening | ✅ | Kernel laplacian 3×3 via `cv2.filter2D` |
| Smoothing / Blur | ✅ | Average blur 5×5 |

### 3. 📐 Geometric Transformation
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Rotate (0°–360°) | ✅ | `getRotationMatrix2D` + `warpAffine` |
| Flip horizontal/vertikal | ✅ | `cv2.flip` |
| Crop | ✅ | Auto-crop center 50% |
| Resize (scaling) | ✅ | `cv2.resize` dengan Interpolasi |
| Translation (geser) | ✅ | `warpAffine` translation matrix |

### 4. 🔄 Image Restoration (Noise Reduction)
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Gaussian Blur | ✅ | `cv2.GaussianBlur` kernel 5×5 |
| Median Filter | ✅ | `cv2.medianBlur` ksize=5 |

### 5. 🔲 Binary & Edge Processing
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Thresholding (binary) | ✅ | `cv2.threshold` |
| Canny Edge | ✅ | Threshold 100–200 |
| Sobel Edge | ✅ | Sobel X + Y → magnitude |
| Prewitt Edge | ✅ | Manual kernel via `filter2D` |
| Robert Edge | ✅ | Kernel cross-gradient 2×2 |
| Laplacian Edge | ✅ | `cv2.Laplacian` |
| Morphology Erosion/Dilation | ✅ | `cv2.erode` & `cv2.dilate` kernel 5×5 |

### 6. 🎨 Color Processing
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| RGB → Grayscale | ✅ | `cv2.cvtColor(COLOR_BGR2GRAY)` |
| Channel splitting (R, G, B) | ✅ | `cv2.split` |

### 7. 🧩 Image Segmentation
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Threshold-based segmentation | ✅ | Binary thresholding |
| Edge-based segmentation | ✅ | Canny + `findContours` + `drawContours` |
| Region-based sederhana | ✅ | K-Means Clustering (K=4) via `cv2.kmeans` |

### 8. 🗜️ Image Compression
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Simulasi kompresi JPEG | ✅ | `cv2.imencode` + `imdecode` |
| Metode RLE & Kuantisasi | ✅ | Simulasi statistik (ratio, segment count) |

### 9. 🤖 Bonus: AI Object Detection *(Nilai Tambah Ekstra)*
| Fitur Spek | Status | Implementasi |
|---|:---:|---|
| Pengenalan objek dengan CNN | ✅ | Arsitektur kustom **YOPSBOX-TI4C** via `cv2.dnn` |
| Algoritma NMS | ✅ | Implementasi *Non-Maximum Suppression* untuk cegah box overlap |
| Translasi 20 Kelas Objek | ✅ | Label Bahasa Indonesia (Orang, Mobil, Kucing, dll) |

**20 Kelas terdeteksi:** `Background, Pesawat, Sepeda, Burung, Perahu, Botol, Bus, Mobil, Kucing, Kursi, Sapi, Meja Makan, Anjing, Kuda, Motor, Orang, Tanaman Hias, Domba, Sofa, Kereta, Monitor TV`

---

## 🚀 Cara Menjalankan Aplikasi

```bash
# Buka terminal dan jalankan perintah sakti ini:
npm run dev
```

Aplikasi akan menyala otomatis:
- Frontend (React) di `http://localhost:3000`
- Backend (FastAPI) di `http://localhost:8000`

---
*Progress Report — Mini Photoshop Web | Pengolahan Citra Digital | 9 Juni 2026*
