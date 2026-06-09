# 📸 Mini Photoshop Web App

Aplikasi pengolahan citra digital berbasis Web (React + FastAPI) yang dilengkapi dengan berbagai macam fitur mulai dari *Image Enhancement*, *Geometric Transformation*, *Noise Reduction*, *Image Segmentation*, *Compression*, hingga kemampuan cerdas **Object Detection** menggunakan AI (Convolutional Neural Network).

Proyek ini disusun untuk memenuhi spesifikasi Tugas Mata Kuliah Pengolahan Citra Digital (Dosen Pengampu: Rizki Elisa Nalawati, S.T., M.T.).

## ✨ Fitur Utama
1. **Image Management:** Upload, Download, Reset gambar dengan preview Before-After ganda.
2. **Image Enhancement:** Brightness, Contrast, Histogram Equalization, Sharpening, Smoothing.
3. **Geometric Transformation:** Rotate, Flip, Crop, Resize, Translation.
4. **Image Restoration:** Gaussian Blur, Median Filter (Noise Reduction).
5. **Binary & Edge Processing:** Thresholding, Canny, Sobel, Prewitt, Robert, Laplacian, Morphology (Erosi/Dilasi).
6. **Color Processing:** Grayscale konversi, Channel Splitting, HSV Adjustment.
7. **Image Segmentation:** Threshold, Edge-based, K-Means Clustering.
8. **Image Compression:** JPEG Compression Simulation & RLE/Kuantisasi.
9. **Histogram Analysis:** Grafik interaktif distribusi warna citra secara real-time.
10. **AI Object Detection:** Deteksi objek cerdas menggunakan arsitektur CNN kustom kebanggaan kita **YOPSBOX-TI4C** dengan dukungan algoritma *Non-Maximum Suppression (NMS)*. Mampu mendeteksi dan mengkotakkan 20 jenis objek yang berbeda (manusia, mobil, anjing, dsb) secara sangat akurat.

## 🛠️ Tech Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Backend:** Python, FastAPI, Uvicorn, OpenCV (cv2), NumPy.
- **Machine Learning:** TensorFlow, OpenCV DNN Module.

## 🚀 Cara Menjalankan Aplikasi Secara Lokal

**Prasyarat Sistem:**
- Node.js terinstall di komputer.
- Python versi 3.10 ke atas terinstall di komputer.

**Langkah Instalasi & Eksekusi:**
1. Buka folder proyek `citra digital` di Terminal atau Command Prompt.
2. Install kebutuhan modul (cukup dilakukan sekali):
   ```bash
   npm install
   ```
3. Jalankan aplikasi dengan perintah pamungkas ini:
   ```bash
   npm run dev
   ```
4. Aplikasi akan menyala otomatis!
   - Buka **`http://localhost:3000`** di browser untuk melihat User Interface.
   - Server Backend API berjalan tersembunyi di `http://localhost:8000`.

## 📄 Lisensi

Proyek ini menggunakan lisensi **MIT License**. Kamu bebas menggunakan, menyalin, memodifikasi, dan mendistribusikan kode ini untuk keperluan apapun asalkan menyantumkan kredit hak cipta (copyright) kepada pengembang aslinya.
Lihat file [LICENSE](LICENSE) untuk detail lengkap.

---
*Developed with ❤️ by Kelas TI-4C — 2026*
