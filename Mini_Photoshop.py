import tkinter as tk

from image_ops import ImageOpsMixin
from ui_layout import UiLayoutMixin


class MiniPhotoshop(ImageOpsMixin, UiLayoutMixin):
    def __init__(self, root):
        # Konfigurasi awal aplikasi.
        self.root = root
        self.root.title("Mini Photoshop - Pengolahan Citra Digital")
        self.root.geometry("1250x850")
        self.root.minsize(1100, 720)

        self.original_image = None
        self.current_image = None
        self.cv_img_orig = None

        self.configure_theme()
        self.setup_ui()


if __name__ == "__main__":
    # Titik masuk aplikasi.
    root = tk.Tk()
    app = MiniPhotoshop(root)
    root.mainloop()
