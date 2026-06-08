import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class UiLayoutMixin:
    def configure_theme(self):
        # Palet warna untuk seluruh UI.
        self.colors = {
            "bg": "#F6F1EB",
            "panel": "#FFFFFF",
            "panel_alt": "#F1E8DE",
            "accent": "#1F7A8C",
            "accent2": "#E76F51",
            "text": "#2E2E2E",
            "muted": "#6B6B6B",
            "border": "#D9CFC3",
            "accent_light": "#C9E4E8",
            "accent2_light": "#F7D6C9",
            "accent_soft": "#E8F0EA"
        }

        # Skema font utama.
        self.font_title = ("Ubuntu", 20, "bold")
        self.font_subtitle = ("Ubuntu", 10)
        self.font_ui = ("Ubuntu", 9)
        self.font_ui_bold = ("Ubuntu", 9, "bold")
        self.font_tab_title = ("Ubuntu", 10, "bold")

        self.root.configure(bg=self.colors["bg"])
        self.root.option_add("*Font", self.font_ui)

        # Konfigurasi gaya ttk.
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TFrame", background=self.colors["bg"])
        style.configure("Sidebar.TFrame", background=self.colors["panel_alt"])
        style.configure("Tab.TFrame", background=self.colors["panel"])
        style.configure("TLabel", background=self.colors["bg"], foreground=self.colors["text"])
        style.configure("Sidebar.TLabel", background=self.colors["panel_alt"], foreground=self.colors["text"], font=self.font_ui_bold)
        style.configure("SidebarMuted.TLabel", background=self.colors["panel_alt"], foreground=self.colors["muted"], font=self.font_ui)
        style.configure("Tab.TLabel", background=self.colors["panel"], foreground=self.colors["text"], font=self.font_ui)
        style.configure("TabTitle.TLabel", background=self.colors["panel"], foreground=self.colors["accent"], font=self.font_tab_title)
        style.configure("TabHint.TLabel", background=self.colors["panel"], foreground=self.colors["muted"], font=self.font_ui)
        style.configure("CardTitle.TLabel", background=self.colors["panel"], foreground=self.colors["accent"], font=self.font_ui_bold)
        style.configure("Header.TLabel", background=self.colors["bg"], foreground=self.colors["text"], font=self.font_title)
        style.configure("Subheader.TLabel", background=self.colors["bg"], foreground=self.colors["muted"], font=self.font_subtitle)

        style.configure(
            "TButton",
            background=self.colors["panel_alt"],
            foreground=self.colors["text"],
            padding=(10, 6),
            font=self.font_ui_bold,
            borderwidth=0
        )
        style.map(
            "TButton",
            background=[("active", self.colors["panel"]), ("pressed", self.colors["panel"])],
            foreground=[("disabled", "#999999")]
        )
        style.configure(
            "Primary.TButton",
            background=self.colors["accent"],
            foreground="white",
            padding=(10, 6),
            font=self.font_ui_bold,
            borderwidth=0
        )
        style.map(
            "Primary.TButton",
            background=[("active", self.colors["accent2"]), ("pressed", self.colors["accent2"])],
            foreground=[("disabled", "#E0E0E0")]
        )

        style.configure("TNotebook", background=self.colors["panel_alt"], borderwidth=0)
        style.configure(
            "Sidebar.TNotebook",
            background=self.colors["panel_alt"],
            borderwidth=0
        )
        style.configure(
            "Sidebar.TNotebook.Tab",
            background=self.colors["panel_alt"],
            foreground=self.colors["text"],
            padding=[10, 6],
            font=self.font_ui_bold
        )
        style.map(
            "Sidebar.TNotebook.Tab",
            background=[("selected", self.colors["panel"])],
            foreground=[("selected", self.colors["accent"])]
        )

        style.configure("TSeparator", background=self.colors["border"])
        style.configure("TScale", background=self.colors["panel"])
        style.configure(
            "Nav.TButton",
            background=self.colors["panel_alt"],
            foreground=self.colors["text"],
            padding=(12, 8),
            font=self.font_ui_bold,
            borderwidth=0
        )
        style.map(
            "Nav.TButton",
            background=[("active", self.colors["panel"]), ("pressed", self.colors["panel"])],
            foreground=[("disabled", "#999999")]
        )
        style.configure(
            "NavActive.TButton",
            background=self.colors["panel"],
            foreground=self.colors["accent"],
            padding=(12, 8),
            font=self.font_ui_bold,
            borderwidth=0
        )

    def draw_header_background(self, event):
        # Ornamen dekoratif di header.
        w = event.width
        h = event.height
        self.header_canvas.delete("all")
        self.header_canvas.create_rectangle(0, 0, w, h, fill=self.colors["bg"], outline="")
        self.header_canvas.create_oval(-80, -60, 140, 160, fill=self.colors["accent_light"], outline="")
        self.header_canvas.create_oval(w - 180, -40, w + 60, 140, fill=self.colors["accent2_light"], outline="")
        self.header_canvas.create_oval(w - 140, 30, w + 160, h + 160, fill=self.colors["accent_soft"], outline="")

    def show_sidebar_panel(self, key):
        # Menampilkan panel sidebar sesuai tombol yang dipilih.
        for panel in self.side_panels.values():
            panel.pack_forget()
        for btn in self.side_buttons.values():
            btn.configure(style="Nav.TButton")

        if key in self.side_panels:
            self.side_panels[key].pack(fill=tk.BOTH, expand=True)
        if key in self.side_buttons:
            self.side_buttons[key].configure(style="NavActive.TButton")

    def setup_ui(self):
        # Menu bar utama.
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open Image", command=self.load_image)
        file_menu.add_command(label="Save Image As...", command=self.save_image)
        file_menu.add_command(label="Reset to Original", command=self.reset_image)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menubar)

        # Header aplikasi.
        self.header = tk.Frame(self.root, bg=self.colors["bg"], height=90)
        self.header.pack(fill=tk.X, side=tk.TOP)
        self.header.pack_propagate(False)

        self.header_canvas = tk.Canvas(self.header, bg=self.colors["bg"], highlightthickness=0)
        self.header_canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.header_canvas.bind("<Configure>", self.draw_header_background)

        self.header_content = tk.Frame(self.header, bg=self.colors["bg"])
        self.header_content.place(relx=0, rely=0, relwidth=1, relheight=1)

        title = tk.Label(
            self.header_content,
            text="Mini Photoshop",
            bg=self.colors["bg"],
            fg=self.colors["text"],
            font=self.font_title
        )
        subtitle = tk.Label(
            self.header_content,
            text="Pengolahan Citra Digital ",
            bg=self.colors["bg"],
            fg=self.colors["muted"],
            font=self.font_subtitle
        )
        title.grid(row=0, column=0, sticky="w", padx=18, pady=(14, 0))
        subtitle.grid(row=1, column=0, sticky="w", padx=18, pady=(0, 14))

        header_actions = tk.Frame(self.header_content, bg=self.colors["bg"])
        header_actions.grid(row=0, column=1, rowspan=2, sticky="e", padx=18)
        ttk.Button(header_actions, text="Open", style="Primary.TButton", command=self.load_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(header_actions, text="Save As", style="TButton", command=self.save_image).pack(side=tk.LEFT, padx=4)
        ttk.Button(header_actions, text="Reset", style="TButton", command=self.reset_image).pack(side=tk.LEFT, padx=4)
        self.header_content.grid_columnconfigure(0, weight=1)

        # Tata letak utama.
        self.body = tk.Frame(self.root, bg=self.colors["bg"])
        self.body.pack(fill=tk.BOTH, expand=True)

        self.left_frame = tk.Frame(self.body, bg=self.colors["panel_alt"], width=320)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(12, 6), pady=12)
        self.left_frame.pack_propagate(False)

        self.right_frame = tk.Frame(self.body, bg=self.colors["bg"])
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(6, 12), pady=12)

        # Header sidebar.
        ttk.Label(self.left_frame, text="Tools", style="Sidebar.TLabel").pack(anchor="w", padx=12, pady=(12, 2))
        ttk.Label(self.left_frame, text="Pilih tab untuk mulai mengedit.", style="SidebarMuted.TLabel").pack(anchor="w", padx=12, pady=(0, 8))

        # Navigasi sidebar dan panel konten.
        self.sidebar_nav = tk.Frame(self.left_frame, bg=self.colors["panel_alt"])
        self.sidebar_nav.pack(fill=tk.X, padx=8, pady=(4, 6))
        self.sidebar_content = tk.Frame(self.left_frame, bg=self.colors["panel_alt"])
        self.sidebar_content.pack(fill=tk.BOTH, expand=True, padx=8, pady=(0, 8))

        self.side_panels = {}
        self.side_buttons = {}

        # Daftar tombol sidebar dan pembuat panel.
        nav_items = [
            ("enhance", "1. Enhance", self.create_enhance_tab),
            ("geometry", "2. Geometry", self.create_geometry_tab),
            ("restore", "3. Restore", self.create_restoration_tab),
            ("edge", "4. Edge / Binary", self.create_edge_tab),
            ("color", "5. Color", self.create_color_tab),
            ("segment", "6. Segment", self.create_segmentation_tab),
            ("compress", "7. Compress", self.create_compression_tab),
            ("cnn", "8. CNN", self.create_cnn_tab)
        ]

        for key, label, builder in nav_items:
            # Tombol sidebar untuk pindah panel.
            btn = ttk.Button(
                self.sidebar_nav,
                text=label,
                style="Nav.TButton",
                command=lambda k=key: self.show_sidebar_panel(k)
            )
            btn.pack(fill=tk.X, pady=3)
            self.side_buttons[key] = btn
            self.side_panels[key] = builder()

        self.show_sidebar_panel("enhance")

        # Area preview.
        self.preview_frame = tk.Frame(self.right_frame, bg=self.colors["bg"])
        self.preview_frame.pack(fill=tk.BOTH, expand=True)
        self.preview_frame.grid_columnconfigure(0, weight=1)
        self.preview_frame.grid_columnconfigure(1, weight=1)
        self.preview_frame.grid_rowconfigure(0, weight=3)
        self.preview_frame.grid_rowconfigure(1, weight=1)

        self.card_orig = tk.Frame(
            self.preview_frame,
            bg=self.colors["panel"],
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        self.card_orig.grid(row=0, column=0, sticky="nsew", padx=(0, 6), pady=(0, 8))
        ttk.Label(self.card_orig, text="Before", style="CardTitle.TLabel").pack(anchor="w", padx=12, pady=(10, 6))
        self.lbl_orig = tk.Label(
            self.card_orig,
            text="Original Image\n(Use File > Open)",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify=tk.CENTER
        )
        self.lbl_orig.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 12))

        self.card_edit = tk.Frame(
            self.preview_frame,
            bg=self.colors["panel"],
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        self.card_edit.grid(row=0, column=1, sticky="nsew", padx=(6, 0), pady=(0, 8))
        ttk.Label(self.card_edit, text="After", style="CardTitle.TLabel").pack(anchor="w", padx=12, pady=(10, 6))
        self.lbl_edit = tk.Label(
            self.card_edit,
            text="Edited Image Preview",
            bg=self.colors["panel"],
            fg=self.colors["muted"],
            justify=tk.CENTER
        )
        self.lbl_edit.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 12))

        self.hist_card = tk.Frame(
            self.preview_frame,
            bg=self.colors["panel"],
            highlightthickness=1,
            highlightbackground=self.colors["border"]
        )
        self.hist_card.grid(row=1, column=0, columnspan=2, sticky="nsew")
        ttk.Label(self.hist_card, text="Histogram (Before vs After)", style="CardTitle.TLabel").pack(anchor="w", padx=12, pady=(10, 6))
        self.hist_frame = tk.Frame(self.hist_card, bg=self.colors["panel"])
        self.hist_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(8, 2.2), facecolor=self.colors["panel"])
        self.fig.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.2, wspace=0.25)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.hist_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def create_enhance_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Enhancement", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Brightness, contrast, and tone", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Label(tab, text="Brightness", style="Tab.TLabel").pack(pady=(12, 0))
        self.scale_bright = ttk.Scale(tab, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.scale_bright.pack(fill=tk.X, padx=10)

        ttk.Label(tab, text="Contrast", style="Tab.TLabel").pack(pady=(10, 0))
        self.scale_contrast = ttk.Scale(tab, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.scale_contrast.pack(fill=tk.X, padx=10)

        ttk.Button(tab, text="Apply Brightness & Contrast", command=self.apply_brightness_contrast).pack(fill=tk.X, padx=10, pady=10)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Button(tab, text="Histogram Equalization", command=self.apply_hist_eq).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Sharpening", command=self.apply_sharpen).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Smoothing (Blur)", command=lambda: self.apply_filter("blur")).pack(fill=tk.X, padx=10, pady=2)

        return tab

    def create_geometry_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Geometry", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Rotate, flip, resize, translate", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Label(tab, text="Rotate (Degrees)", style="Tab.TLabel").pack(pady=(12, 0))
        self.scale_rotate = ttk.Scale(tab, from_=0, to=360, orient=tk.HORIZONTAL)
        self.scale_rotate.pack(fill=tk.X, padx=10)
        ttk.Button(tab, text="Apply Rotation", command=self.apply_rotate).pack(fill=tk.X, padx=10, pady=5)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=5)

        ttk.Button(tab, text="Flip Horizontal", command=lambda: self.apply_flip(1)).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Flip Vertical", command=lambda: self.apply_flip(0)).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Crop Center (50%)", command=self.apply_crop).pack(fill=tk.X, padx=10, pady=2)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=5)

        ttk.Label(tab, text="Resize (%)", style="Tab.TLabel").pack(pady=(5, 0))
        self.scale_resize = ttk.Scale(tab, from_=10, to=200, orient=tk.HORIZONTAL)
        self.scale_resize.set(100)
        self.scale_resize.pack(fill=tk.X, padx=10)
        ttk.Button(tab, text="Apply Resize", command=self.apply_resize).pack(fill=tk.X, padx=10, pady=5)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=5)

        ttk.Label(tab, text="Translate X", style="Tab.TLabel").pack()
        self.scale_tx = ttk.Scale(tab, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.scale_tx.pack(fill=tk.X, padx=10)
        ttk.Label(tab, text="Translate Y", style="Tab.TLabel").pack()
        self.scale_ty = ttk.Scale(tab, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.scale_ty.pack(fill=tk.X, padx=10)
        ttk.Button(tab, text="Apply Translation", command=self.apply_translation).pack(fill=tk.X, padx=10, pady=5)

        return tab

    def create_restoration_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Restoration", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Noise reduction filters", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Button(tab, text="Gaussian Blur", command=lambda: self.apply_filter("gaussian")).pack(fill=tk.X, padx=10, pady=10)
        ttk.Button(tab, text="Median Filter (Noise Removal)", command=lambda: self.apply_filter("median")).pack(fill=tk.X, padx=10, pady=10)

        return tab

    def create_edge_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Edge + Binary", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Thresholding and morphology", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Button(tab, text="Thresholding (Binary)", command=self.apply_threshold).pack(fill=tk.X, padx=10, pady=2)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Button(tab, text="Canny Edge", command=lambda: self.apply_edge("canny")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Sobel Edge", command=lambda: self.apply_edge("sobel")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Prewitt Edge", command=lambda: self.apply_edge("prewitt")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Robert Edge", command=lambda: self.apply_edge("robert")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Laplacian Edge", command=lambda: self.apply_edge("laplacian")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="LoG (Laplacian of Gaussian)", command=lambda: self.apply_edge("log")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Button(tab, text="Morphology Erosion", command=lambda: self.apply_morph("erosion")).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Morphology Dilation", command=lambda: self.apply_morph("dilation")).pack(fill=tk.X, padx=10, pady=2)

        return tab

    def create_color_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Color", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Channels and HSV tuning", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Button(tab, text="Convert to Grayscale", command=self.apply_grayscale).pack(fill=tk.X, padx=10, pady=10)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Button(tab, text="Split Channel (Show Red)", command=lambda: self.split_channel(2)).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Split Channel (Show Green)", command=lambda: self.split_channel(1)).pack(fill=tk.X, padx=10, pady=2)
        ttk.Button(tab, text="Split Channel (Show Blue)", command=lambda: self.split_channel(0)).pack(fill=tk.X, padx=10, pady=2)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Label(tab, text="Hue", style="Tab.TLabel").pack(pady=(5, 0))
        self.scale_hue = ttk.Scale(tab, from_=-90, to=90, orient=tk.HORIZONTAL)
        self.scale_hue.pack(fill=tk.X, padx=10)
        ttk.Label(tab, text="Saturation", style="Tab.TLabel").pack(pady=(5, 0))
        self.scale_sat = ttk.Scale(tab, from_=-100, to=100, orient=tk.HORIZONTAL)
        self.scale_sat.pack(fill=tk.X, padx=10)
        ttk.Button(tab, text="Apply HSV Adjustment", command=self.apply_hsv).pack(fill=tk.X, padx=10, pady=10)

        return tab

    def create_segmentation_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Segmentation", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Threshold, edge, region", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Button(tab, text="Threshold-based Segmentation", command=self.apply_threshold).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(tab, text="Edge-based Segmentation", command=self.apply_edge_segmentation).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(tab, text="Region-based (K-Means)", command=self.apply_kmeans).pack(fill=tk.X, padx=10, pady=5)

        return tab

    def create_compression_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="Compression", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="JPEG quality and quantization", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Label(tab, text="JPEG Quality (1-100)", style="Tab.TLabel").pack(pady=(12, 0))
        self.scale_jpeg = ttk.Scale(tab, from_=1, to=100, orient=tk.HORIZONTAL)
        self.scale_jpeg.set(30)
        self.scale_jpeg.pack(fill=tk.X, padx=10)
        ttk.Button(tab, text="Simulate JPEG Compression", command=self.simulate_jpeg).pack(fill=tk.X, padx=10, pady=5)
        ttk.Separator(tab, orient="horizontal").pack(fill=tk.X, pady=10)

        ttk.Button(tab, text="Simulate RLE (Statistik)", command=self.simulate_rle).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(tab, text="Metode Kuantisasi", command=self.simulate_quantization).pack(fill=tk.X, padx=10, pady=5)

        return tab

    def create_cnn_tab(self):
        tab = ttk.Frame(self.sidebar_content, style="Tab.TFrame")
        ttk.Label(tab, text="CNN", style="TabTitle.TLabel").pack(anchor="w", padx=10, pady=(10, 2))
        ttk.Label(tab, text="Object detection", style="TabHint.TLabel").pack(anchor="w", padx=10, pady=(0, 8))

        ttk.Label(tab, text="Object Detection\n(MobileNet SSD Caffe)", justify=tk.CENTER, style="TabTitle.TLabel").pack(pady=(12, 6))
        ttk.Label(tab, text="Klik tombol Download jika\nfile weights belum ada di PC.", justify=tk.CENTER, style="TabHint.TLabel").pack(pady=(0, 8))

        ttk.Button(tab, text="1. Download Model Weights", command=self.download_model).pack(fill=tk.X, padx=10, pady=5)
        ttk.Button(tab, text="2. Detect Objects in Image", command=self.detect_objects).pack(fill=tk.X, padx=10, pady=5)

        return tab
