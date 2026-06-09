# 📸 Mini Photoshop Web App

A web-based digital image processing application (React + FastAPI) equipped with various features ranging from *Image Enhancement*, *Geometric Transformation*, *Noise Reduction*, *Image Segmentation*, *Compression*, to smart **Object Detection** capabilities using AI (Convolutional Neural Network).

This project was developed to fulfill the specifications of the Digital Image Processing Course (Instructor: Rizki Elisa Nalawati, S.T., M.T.).

## ✨ Key Features
1. **Image Management:** Upload, Download, and Reset images with a dual Before-After preview.
2. **Image Enhancement:** Brightness, Contrast, Histogram Equalization, Sharpening, and Smoothing.
3. **Geometric Transformation:** Rotate, Flip, Crop, Resize, and Translation.
4. **Image Restoration:** Gaussian Blur and Median Filter (Noise Reduction).
5. **Binary & Edge Processing:** Thresholding, Canny, Sobel, Prewitt, Robert, Laplacian, and Morphology (Erosion/Dilation).
6. **Color Processing:** Grayscale conversion, Channel Splitting, and HSV Adjustment.
7. **Image Segmentation:** Threshold-based, Edge-based, and K-Means Clustering.
8. **Image Compression:** JPEG Compression Simulation & RLE/Quantization.
9. **Histogram Analysis:** Interactive and real-time image color distribution graphs.
10. **AI Object Detection:** Smart object detection using our custom CNN architecture **YOPSBOX-TI4C** backed by the *Non-Maximum Suppression (NMS)* algorithm. Accurately detects and draws bounding boxes around 20 different object categories (people, cars, animals, etc.).

## 🛠️ Tech Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Lucide Icons.
- **Backend:** Python, FastAPI, Uvicorn, OpenCV (cv2), NumPy.
- **Machine Learning:** TensorFlow, OpenCV DNN Module.

## 🚀 How to Run Locally

**System Requirements:**
- Node.js installed on your machine.
- Python 3.10 or higher installed on your machine.

**Installation & Execution Steps:**
1. Open the `citra digital` project folder in your Terminal or Command Prompt.
2. Install the required modules (only needed once):
   ```bash
   npm install
   ```
3. Run the application using this ultimate command:
   ```bash
   npm run dev
   ```
4. The application will start automatically!
   - Open **`http://localhost:3000`** in your browser to view the User Interface.
   - The Backend API server runs silently at `http://localhost:8000`.

## 📄 License

This project is licensed under the **MIT License**. You are free to use, copy, modify, and distribute this code for any purpose, provided that you include the original copyright credit to the developers.
See the [LICENSE](LICENSE) file for full details.

---
*Developed with ❤️ by Class TI-4C — 2026*
