import os
import urllib.request
from tkinter import filedialog, messagebox

import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageOpsMixin:
    def load_image(self):
        # Membuka file gambar dari disk.
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.bmp *.jpeg")])
        if path:
            self.cv_img_orig = cv2.imread(path)
            self.current_image = self.cv_img_orig.copy()
            self.update_display(original=True, edited=True)

    def save_image(self):
        # Menyimpan hasil edit ke file.
        if self.current_image is not None:
            path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")]
            )
            if path:
                cv2.imwrite(path, self.current_image)
                messagebox.showinfo("Success", "Image saved successfully!")

    def reset_image(self):
        # Mengembalikan ke gambar asli.
        if self.cv_img_orig is not None:
            self.current_image = self.cv_img_orig.copy()
            self.update_display(edited=True)

    def update_display(self, original=False, edited=False):
        # Konversi OpenCV -> Tkinter agar bisa ditampilkan.
        def cv2_to_tk(cv_img):
            if len(cv_img.shape) == 3:
                img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            else:
                img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_GRAY2RGB)

            h, w = img_rgb.shape[:2]
            max_size = 480
            scale = max_size / max(h, w)
            new_w, new_h = int(w * scale), int(h * scale)
            img_rgb = cv2.resize(img_rgb, (new_w, new_h))

            im_pil = Image.fromarray(img_rgb)
            return ImageTk.PhotoImage(im_pil)

        if original and self.cv_img_orig is not None:
            self.tk_orig = cv2_to_tk(self.cv_img_orig)
            self.lbl_orig.config(image=self.tk_orig, text="")

        if edited and self.current_image is not None:
            self.tk_edit = cv2_to_tk(self.current_image)
            self.lbl_edit.config(image=self.tk_edit, text="")
            self.update_histogram()

    def update_histogram(self):
        # Menggambar histogram sebelum dan sesudah.
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.set_facecolor(self.colors["panel"])
        self.ax2.set_facecolor(self.colors["panel"])

        if self.cv_img_orig is not None:
            gray_orig = cv2.cvtColor(self.cv_img_orig, cv2.COLOR_BGR2GRAY) if len(self.cv_img_orig.shape) == 3 else self.cv_img_orig
            self.ax1.hist(gray_orig.ravel(), 256, [0, 256], color=self.colors["accent"], alpha=0.75)
            self.ax1.set_title("Histogram Original (Grayscale)", color=self.colors["text"], fontsize=9)

        if self.current_image is not None:
            gray_edit = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY) if len(self.current_image.shape) == 3 else self.current_image
            self.ax2.hist(gray_edit.ravel(), 256, [0, 256], color=self.colors["accent2"], alpha=0.75)
            self.ax2.set_title("Histogram Edited (Grayscale)", color=self.colors["text"], fontsize=9)

        for ax in (self.ax1, self.ax2):
            ax.tick_params(axis="both", colors=self.colors["muted"], labelsize=8)
            for spine in ax.spines.values():
                spine.set_color(self.colors["border"])

        self.canvas.draw()

    # --- 2. Peningkatan ---
    def apply_brightness_contrast(self):
        if self.current_image is None:
            return
        b = self.scale_bright.get()
        c = self.scale_contrast.get()

        alpha = (c + 100) / 100.0
        beta = b
        self.current_image = cv2.convertScaleAbs(self.cv_img_orig, alpha=alpha, beta=beta)
        self.update_display(edited=True)

    def apply_hist_eq(self):
        if self.current_image is None:
            return
        if len(self.current_image.shape) == 3:
            img_yuv = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2YUV)
            img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
            self.current_image = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
        else:
            self.current_image = cv2.equalizeHist(self.current_image)
        self.update_display(edited=True)

    def apply_sharpen(self):
        if self.current_image is None:
            return
        kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
        self.current_image = cv2.filter2D(self.current_image, -1, kernel)
        self.update_display(edited=True)

    def apply_filter(self, ftype):
        if self.current_image is None:
            return
        if ftype == "blur":
            self.current_image = cv2.blur(self.current_image, (5, 5))
        elif ftype == "gaussian":
            self.current_image = cv2.GaussianBlur(self.current_image, (5, 5), 0)
        elif ftype == "median":
            self.current_image = cv2.medianBlur(self.current_image, 5)
        self.update_display(edited=True)

    # --- 3. Transformasi Geometri ---
    def apply_rotate(self):
        if self.current_image is None:
            return
        angle = self.scale_rotate.get()
        h, w = self.current_image.shape[:2]
        mtx = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
        self.current_image = cv2.warpAffine(self.cv_img_orig, mtx, (w, h))
        self.update_display(edited=True)

    def apply_flip(self, mode):
        if self.current_image is None:
            return
        self.current_image = cv2.flip(self.current_image, mode)
        self.update_display(edited=True)

    def apply_crop(self):
        if self.current_image is None:
            return
        h, w = self.current_image.shape[:2]
        y1, y2 = int(h * 0.25), int(h * 0.75)
        x1, x2 = int(w * 0.25), int(w * 0.75)
        self.current_image = self.current_image[y1:y2, x1:x2]
        self.update_display(edited=True)

    def apply_resize(self):
        if self.current_image is None:
            return
        scale = self.scale_resize.get() / 100.0
        w = int(self.cv_img_orig.shape[1] * scale)
        h = int(self.cv_img_orig.shape[0] * scale)
        self.current_image = cv2.resize(self.cv_img_orig, (w, h), interpolation=cv2.INTER_LINEAR)
        self.update_display(edited=True)

    def apply_translation(self):
        if self.current_image is None:
            return
        tx = self.scale_tx.get()
        ty = self.scale_ty.get()
        h, w = self.current_image.shape[:2]
        mtx = np.float32([[1, 0, tx], [0, 1, ty]])
        self.current_image = cv2.warpAffine(self.cv_img_orig, mtx, (w, h))
        self.update_display(edited=True)

    # --- 5. Tepi / Biner ---
    def apply_threshold(self):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY) if len(self.current_image.shape) == 3 else self.current_image
        _, self.current_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        self.update_display(edited=True)

    def apply_edge(self, etype):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY) if len(self.current_image.shape) == 3 else self.current_image

        if etype == "canny":
            self.current_image = cv2.Canny(gray, 100, 200)
        elif etype == "sobel":
            sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            self.current_image = cv2.convertScaleAbs(np.sqrt(sobelx ** 2 + sobely ** 2))
        elif etype == "prewitt":
            kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]])
            kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]])
            px = cv2.filter2D(gray, -1, kernelx)
            py = cv2.filter2D(gray, -1, kernely)
            self.current_image = cv2.addWeighted(px, 0.5, py, 0.5, 0)
        elif etype == "robert":
            kernelx = np.array([[1, 0], [0, -1]])
            kernely = np.array([[0, 1], [-1, 0]])
            rx = cv2.filter2D(gray, -1, kernelx)
            ry = cv2.filter2D(gray, -1, kernely)
            self.current_image = cv2.addWeighted(rx, 0.5, ry, 0.5, 0)
        elif etype == "laplacian":
            self.current_image = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))
        elif etype == "log":
            blur = cv2.GaussianBlur(gray, (3, 3), 0)
            self.current_image = cv2.convertScaleAbs(cv2.Laplacian(blur, cv2.CV_64F))

        self.update_display(edited=True)

    def apply_morph(self, mtype):
        if self.current_image is None:
            return
        kernel = np.ones((5, 5), np.uint8)
        if mtype == "erosion":
            self.current_image = cv2.erode(self.current_image, kernel, iterations=1)
        elif mtype == "dilation":
            self.current_image = cv2.dilate(self.current_image, kernel, iterations=1)
        self.update_display(edited=True)

    # --- 6. Pemrosesan Warna ---
    def apply_grayscale(self):
        if self.current_image is None:
            return
        if len(self.current_image.shape) == 3:
            self.current_image = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        self.update_display(edited=True)

    def split_channel(self, channel):
        if self.current_image is None or len(self.current_image.shape) != 3:
            return
        b, g, r = cv2.split(self.current_image)
        if channel == 0:
            self.current_image = b
        elif channel == 1:
            self.current_image = g
        elif channel == 2:
            self.current_image = r
        self.update_display(edited=True)

    def apply_hsv(self):
        if self.current_image is None or len(self.current_image.shape) != 3:
            return
        hsv = cv2.cvtColor(self.cv_img_orig, cv2.COLOR_BGR2HSV).astype(np.int16)
        hsv[:, :, 0] += self.scale_hue.get()
        hsv[:, :, 1] += self.scale_sat.get()
        hsv[:, :, 0] = np.clip(hsv[:, :, 0], 0, 179)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1], 0, 255)
        self.current_image = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        self.update_display(edited=True)

    # --- 7. Segmentasi ---
    def apply_kmeans(self):
        if self.current_image is None:
            return
        img_temp = self.current_image.copy()
        if len(img_temp.shape) == 2:
            img_temp = cv2.cvtColor(img_temp, cv2.COLOR_GRAY2BGR)
        z_values = img_temp.reshape((-1, 3))
        z_values = np.float32(z_values)
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = 4
        _, label, center = cv2.kmeans(z_values, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
        center = np.uint8(center)
        res = center[label.flatten()]
        self.current_image = res.reshape((img_temp.shape))
        self.update_display(edited=True)

    def apply_edge_segmentation(self):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY) if len(self.current_image.shape) == 3 else self.current_image
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blur, 50, 150)
        contours, _ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if len(self.cv_img_orig.shape) == 3:
            res = self.cv_img_orig.copy()
        else:
            res = cv2.cvtColor(self.cv_img_orig, cv2.COLOR_GRAY2BGR)

        cv2.drawContours(res, contours, -1, (0, 255, 0), 2)
        self.current_image = res
        self.update_display(edited=True)

    # --- 8. Kompresi ---
    def simulate_jpeg(self):
        if self.current_image is None:
            return
        q = int(self.scale_jpeg.get())
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), q]
        _, encimg = cv2.imencode(".jpg", self.current_image, encode_param)
        self.current_image = cv2.imdecode(encimg, 1)
        self.update_display(edited=True)

    def simulate_rle(self):
        if self.current_image is None:
            return
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY) if len(self.current_image.shape) == 3 else self.current_image
        flat = gray.flatten()
        if len(flat) == 0:
            return

        segments = 1
        for i in range(1, len(flat)):
            if flat[i] != flat[i - 1]:
                segments += 1

        orig_size = len(flat)
        comp_size = segments * 2  # (nilai, jumlah)

        messagebox.showinfo(
            "RLE Statistics",
            f"Original Size: {orig_size} bytes\n"
            f"RLE Compressed Size (est): {comp_size} bytes\n"
            f"Total Segments Found: {segments}\n"
            f"Compression Ratio: {orig_size / comp_size if comp_size > 0 else 0:.2f}x"
        )

    def simulate_quantization(self):
        if self.current_image is None:
            return
        factor = 256 / 8  # 8 level
        self.current_image = np.uint8(np.floor(self.current_image / factor) * factor)
        self.update_display(edited=True)

    # --- 11. Deteksi Objek CNN ---
    def download_model(self):
        prototxt = "MobileNetSSD_deploy.prototxt"
        model = "MobileNetSSD_deploy.caffemodel"

        # URL model dari GitHub (coba beberapa lokasi agar tidak 404).
        url_proto_candidates = [
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/voc/MobileNetSSD_deploy.prototxt",
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.prototxt"
        ]
        url_model_candidates = [
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/voc/MobileNetSSD_deploy.caffemodel",
            "https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/master/MobileNetSSD_deploy.caffemodel"
        ]

        def needs_download(path):
            return (not os.path.exists(path)) or os.path.getsize(path) == 0

        def download_first(urls, target):
            last_exc = None
            for url in urls:
                try:
                    urllib.request.urlretrieve(url, target)
                    return None
                except Exception as exc:
                    last_exc = exc
            return last_exc

        try:
            if needs_download(prototxt):
                err = download_first(url_proto_candidates, prototxt)
                if err:
                    raise err
            if needs_download(model):
                err = download_first(url_model_candidates, model)
                if err:
                    raise err
            messagebox.showinfo("Success", "Model weights downloaded successfully!")
        except Exception as exc:
            messagebox.showerror("Error", f"Failed to download model: {exc}")

    def detect_objects(self):
        if self.current_image is None:
            return

        prototxt = "MobileNetSSD_deploy.prototxt"
        model = "MobileNetSSD_deploy.caffemodel"

        if not os.path.exists(prototxt) or not os.path.exists(model):
            messagebox.showwarning(
                "Warning",
                "Model files not found! Please click 'Download Model Weights' first in the CNN tab."
            )
            return

        classes = [
            "background", "aeroplane", "bicycle", "bird", "boat",
            "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
            "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
            "sofa", "train", "tvmonitor"
        ]

        net = cv2.dnn.readNetFromCaffe(prototxt, model)

        image = self.current_image.copy()
        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        (h, w) = image.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.4:
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (start_x, start_y, end_x, end_y) = box.astype("int")

                label = f"{classes[idx]}: {confidence * 100:.2f}%"
                cv2.rectangle(image, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)
                y = start_y - 15 if start_y - 15 > 15 else start_y + 15
                cv2.putText(image, label, (start_x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        self.current_image = image
        self.update_display(edited=True)
