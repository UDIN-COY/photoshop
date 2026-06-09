import os
import tensorflow as tf

print("Mendownload arsitektur dan bobot ResNet50 (ImageNet)...")
# Load model ResNet50 bawaan Keras yang sudah dilatih dengan ImageNet
model = tf.keras.applications.ResNet50(weights='imagenet')

# Pastikan folder models ada
os.makedirs("models", exist_ok=True)

# Simpan modelnya ke file .h5 agar kamu punya file fisiknya
model_path = "models/YOPS.h5"
model.save(model_path)

print(f"Selesai! Model berhasil disimpan secara fisik di: {model_path}")
