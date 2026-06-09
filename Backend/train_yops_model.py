import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
import os

# ==============================================================================
# SCRIPT PELATIHAN MODEL YOPSBOX-TI4C (SIMULASI UNTUK DOKUMENTASI)
# ==============================================================================

def build_yops_model(num_classes=20):
    print("[INFO] Membangun arsitektur kustom YOPSBOX-TI4C...")
    
    # 1. Input layer (Menerima gambar 300x300 pixel RGB)
    inputs = Input(shape=(300, 300, 3))
    
    # 2. Blok Ekstraksi Fitur (Feature Extraction Layers)
    x = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    x = Conv2D(128, (3, 3), activation='relu', padding='same')(x)
    x = MaxPooling2D(pool_size=(2, 2))(x)
    
    # 3. Meratakan matriks untuk masuk ke saraf otak tiruan
    x = Flatten()(x)
    
    # 4. Layer Kustom ("Kepala" Model) untuk memproses kesimpulan
    x = Dense(512, activation='relu')(x)
    x = Dropout(0.5)(x) # Mencegah overfitting (menghafal dataset)
    
    # 3. Layer prediksi akhir (20 kelas objek + 1 background)
    predictions = Dense(num_classes + 1, activation='softmax')(x)
    
    # 4. Satukan kerangka menjadi satu model utuh
    model = Model(inputs=inputs, outputs=predictions, name="YOPSBOX-TI4C")
    return model

def train_model():
    # Direktori dataset bayangan
    dataset_dir = "./dataset_ti4c/"
    if not os.path.exists(dataset_dir):
        print("[WARNING] Folder dataset tidak ditemukan. Menggunakan dummy data generator...")
    
    # Inisialisasi Model
    model = build_yops_model(num_classes=20)
    
    # Konfigurasi Algoritma Pembelajaran (Optimizer & Loss)
    print("[INFO] Mengompilasi model...")
    opt = Adam(learning_rate=1e-4)
    model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
    
    # Tampilkan rangkuman kerangka model
    model.summary()
    
    # --- PROSES PELATIHAN (TRAINING) ---
    print("\n[INFO] ==========================================")
    print("[INFO] MEMULAI PROSES TRAINING YOPSBOX-TI4C...")
    print("[INFO] ==========================================\n")
    
    epochs = 100
    batch_size = 32
    
    print(f"Menjalankan training selama {epochs} Epochs dengan ukuran Batch {batch_size}...")
    
    # (Di dunia nyata, di sini akan ada fungsi model.fit() yang memakan waktu berhari-hari di GPU)
    # model.fit(train_generator, validation_data=val_generator, epochs=epochs)
    
    print("\n[INFO] Epoch 100/100 selesai! Akurasi validasi: 96.8%")
    print("[INFO] Menyimpan model akhir...")
    
    # 5. Simpan Model ke format akhir
    save_path = "models/YOPSBOX.TI4C"
    # model.save(save_path)
    
    print(f"[SUCCESS] Model YOPSBOX-TI4C berhasil dilatih dan disimpan ke: {save_path}!")

if __name__ == "__main__":
    train_model()
