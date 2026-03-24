import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True
import os
import csv
from datetime import datetime

# ==========================================================
# Configurable parameters
# ==========================================================
GRID_ROWS = 7
GRID_COLS = 3
IMAGE_DISPLAY_SIZE = (576, 324)  # (width, height)

# Dark theme colors
DARK_BG = "#1c1c1c"     # near-black
DARK_BG2 = "#2b2b2b"    # dark gray
LIGHT_TEXT = "#e0e0e0"  # soft white text
ACCENT = "#3a7bd5"

INITIAL_EXPERIMENTS = ["Default"]


# ==========================================================
# Helper: parse camera number + timestamp from filename
# ==========================================================
def parse_timestamp_from_filename(fname):
    base = os.path.splitext(fname)[0]
    parts = base.split("_")
    if len(parts) < 3:
        return None, None
    camera_part = parts[0]
    cam_num = None
    if camera_part.lower().startswith("camera"):
        try:
            cam_num = int(camera_part[6:])
        except:
            pass

    date_str = parts[1] + parts[2]
    try:
        ts = datetime.strptime(date_str, "%Y%m%d%H%M%S")
    except:
        ts = None

    return cam_num, ts

def crop_center_percent(img, keep_x=0.5, keep_y=0.8):
    w, h = img.size

    crop_w = int(w * keep_x)
    crop_h = int(h * keep_y)

    left = (w - crop_w) // 2
    top = (h - crop_h) // 2

    return img.crop((
        left,
        top,
        left + crop_w,
        top + crop_h
    ))

# ==========================================================
# SeedGrid
# ==========================================================
class SeedGrid(tk.Frame):
    def __init__(self, parent, grid_name, callback_record):
        super().__init__(parent, bg=DARK_BG)
        self.grid_name = grid_name
        self.callback_record = callback_record
        self.buttons = {}

        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                b = tk.Button(
                    self,
                    text="",
                    width=2,
                    height=1,
                    bg=DARK_BG2,
                    fg=LIGHT_TEXT,
                    activebackground="#555",
                    activeforeground="white",
                    relief="ridge",
                    command=lambda rr=r, cc=c: self._clicked(rr, cc)
                )
                b.grid(row=r, column=c, padx=2, pady=2)
                self.buttons[(r, c)] = b

    def _clicked(self, r, c):
        timestamp = self.callback_record(self.grid_name, r, c)
        btn = self.buttons[(r, c)]
        if timestamp:
            btn.config(text=str(timestamp), fg="#ffd65b")  # yellow highlight


# ==========================================================
# ImagePanel
# ==========================================================
class ImagePanel(tk.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, bg=DARK_BG)

        tk.Label(
            self, text=title, font=("Arial", 14),
            bg=DARK_BG, fg=LIGHT_TEXT
        ).pack(pady=4)

        self.canvas = tk.Canvas(
            self,
            width=IMAGE_DISPLAY_SIZE[0],
            height=IMAGE_DISPLAY_SIZE[1],
            bg=DARK_BG2,
            highlightthickness=0
        )
        self.canvas.pack()

        self.label = tk.Label(
            self,
            text="No images loaded",
            bg=DARK_BG,
            fg=LIGHT_TEXT
        )
        self.label.pack(pady=4)

        self.photo = None
        self.images = []
        self.index = 0

    def load_images(self, image_list):
        self.images = image_list
        self.index = 0
        if self.images:
            self.display(0)
        else:
            self.canvas.delete("all")
            self.label.config(text="No images found")

    def display(self, idx):
        if not self.images:
            return

        idx = max(0, min(idx, len(self.images) - 1))
        self.index = idx

        path, ts = self.images[idx]

        # 1) Load original image
        img = Image.open(path)

        # 2) HARD crop (pixel removal only)
        img = crop_center_percent(
            img,
            keep_x=1.0,  # zoom factor controlled here
            keep_y=1.0
        )

        # 3) UNIFORM SCALE (zoom) — no distortion
        cw, ch = img.size
        dw, dh = IMAGE_DISPLAY_SIZE

        scale = max(dw / cw, dh / ch)  # fill display → zoom in
        new_size = (
            int(cw * scale),
            int(ch * scale)
        )

        img = img.resize(new_size, Image.Resampling.LANCZOS)

        # 4) Center in canvas
        self.photo = ImageTk.PhotoImage(img)
        self.canvas.delete("all")

        x = (dw - new_size[0]) // 2
        y = (dh - new_size[1]) // 2

        self.canvas.create_image(
            x, y,
            anchor="nw",
            image=self.photo
        )

        fname = os.path.basename(path)
        self.label.config(
            text=f"{fname}\n({idx + 1}/{len(self.images)})",
            fg=LIGHT_TEXT,
            bg=DARK_BG
        )

    def next(self):
        self.display(self.index + 1)

    def prev(self):
        self.display(self.index - 1)

    def get_current_timestamp(self):
        if not self.images:
            return None
        path, ts = self.images[self.index]
        return ts

    def get_current_frame(self):
        return self.index + 1

# ==========================================================
# Main App
# ==========================================================
class SeedAnnotationApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Seed Germination Annotation Tool — Dark Mode")
        self.geometry("1500x1000")
        self.configure(bg=DARK_BG)

        # Style ttk widgets (Combobox)
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground=DARK_BG2,
                        background=DARK_BG2,
                        foreground=LIGHT_TEXT)
        style.map("TCombobox",
                  fieldbackground=[("readonly", DARK_BG2)],
                  selectbackground=[("readonly", DARK_BG2)],
                  selectforeground=[("readonly", LIGHT_TEXT)])

        # -------------------- Top Controls --------------------
        top = tk.Frame(self, bg=DARK_BG)
        top.pack(fill="x", pady=6)

        load_btn = tk.Button(
            top, text="Load Image Folder", command=self.load_folder,
            bg=DARK_BG2, fg=LIGHT_TEXT, activebackground="#444"
        )
        load_btn.pack(side="left", padx=6)

        tk.Label(top, text="Experiment:", bg=DARK_BG, fg=LIGHT_TEXT)\
            .pack(side="left", padx=(15, 3))

        self.experiment_var = tk.StringVar()
        self.experiment_combo = ttk.Combobox(
            top, textvariable=self.experiment_var,
            state="readonly"
        )
        self.experiment_combo["values"] = INITIAL_EXPERIMENTS.copy()
        self.experiment_combo.current(0)
        self.experiment_combo.pack(side="left")

        tk.Label(top, text="Add:", bg=DARK_BG, fg=LIGHT_TEXT)\
            .pack(side="left", padx=(10, 3))

        self.add_entry = tk.Entry(top, width=20,
                                  bg=DARK_BG2, fg=LIGHT_TEXT,
                                  insertbackground=LIGHT_TEXT)
        self.add_entry.pack(side="left")

        tk.Button(top, text="Add", command=self.add_experiment,
                  bg=DARK_BG2, fg=LIGHT_TEXT, activebackground="#444")\
            .pack(side="left", padx=3)

        # -------------------- Middle Layout --------------------
        mid = tk.Frame(self, bg=DARK_BG)
        mid.pack(pady=10)

        # --- Camera 1 ----
        cam1_block = tk.Frame(mid, bg=DARK_BG)
        cam1_block.grid(row=0, column=0, padx=20)

        self.camera1_panel = ImagePanel(cam1_block, "Camera 1")
        self.camera1_panel.pack(pady=5)

        self.grid_cam1 = SeedGrid(cam1_block, "camera1", self.record_time)
        self.grid_cam1.pack(pady=5)

        # --- Buttons in Center ---
        button_block = tk.Frame(mid, bg=DARK_BG)
        button_block.grid(row=0, column=1, padx=20)

        tk.Button(button_block, text="← Prev", command=self.prev, width=12,
                  bg=DARK_BG2, fg=LIGHT_TEXT, activebackground="#444")\
            .pack(pady=10)

        tk.Button(button_block, text="Next →", command=self.next, width=12,
                  bg=DARK_BG2, fg=LIGHT_TEXT, activebackground="#444")\
            .pack(pady=10)

        tk.Button(button_block, text="Export CSV", command=self.export_csv, width=12,
                  bg=DARK_BG2, fg=LIGHT_TEXT, activebackground="#444")\
            .pack(pady=10)

        # --- Camera 2 ----
        cam2_block = tk.Frame(mid, bg=DARK_BG)
        cam2_block.grid(row=0, column=2, padx=20)

        self.camera2_panel = ImagePanel(cam2_block, "Camera 2")
        self.camera2_panel.pack(pady=5)

        self.grid_cam2 = SeedGrid(cam2_block, "camera2", self.record_time)
        self.grid_cam2.pack(pady=5)

        # -------------------- Status --------------------
        self.status = tk.Label(
            self, text="Annotations: 0",
            bg=DARK_BG, fg=LIGHT_TEXT
        )
        self.status.pack(pady=6)

        # Annotation storage
        self.annotations = {}

    # ------------------------------ Loading images ------------------------------
    def load_folder(self):
        folder = filedialog.askdirectory()
        if not folder:
            return

        cam1, cam2 = [], []

        for fname in os.listdir(folder):
            if not fname.lower().endswith(".png"):
                continue

            cam_num, ts = parse_timestamp_from_filename(fname)
            if cam_num not in (1, 2) or ts is None:
                continue

            full = os.path.join(folder, fname)
            if cam_num == 1:
                cam1.append((full, ts))
            else:
                cam2.append((full, ts))

        cam1.sort(key=lambda x: x[1])
        cam2.sort(key=lambda x: x[1])

        self.camera1_panel.load_images(cam1)
        self.camera2_panel.load_images(cam2)

        self.annotations.clear()
        self.update_status()

    # ------------------------------ Navigation ------------------------------
    def next(self):
        self.camera1_panel.next()
        self.camera2_panel.next()

    def prev(self):
        self.camera1_panel.prev()
        self.camera2_panel.prev()

    # ------------------------------ Experiments ------------------------------
    def add_experiment(self):
        name = self.add_entry.get().strip()
        if not name:
            return
        vals = list(self.experiment_combo["values"])
        if name not in vals:
            vals.append(name)
            self.experiment_combo["values"] = vals
            self.experiment_combo.set(name)
        self.add_entry.delete(0, tk.END)

    # ------------------------------ Annotation ------------------------------
    def record_time(self, grid_name, r, c):
        if grid_name == "camera1":
            ts = self.camera1_panel.get_current_timestamp()
            frame = self.camera1_panel.get_current_frame()
        else:
            ts = self.camera2_panel.get_current_timestamp()
            frame = self.camera2_panel.get_current_frame()

        if ts is None:
            return None

        key = (grid_name, r, c)

        self.annotations.setdefault(key, []).append(
            (ts.strftime("%Y-%m-%d %H:%M:%S"), frame)
        )

        self.update_status()
        return ts.strftime("%H:%M:%S")

    def update_status(self):
        total = sum(len(v) for v in self.annotations.values())
        self.status.config(text=f"Annotations: {total}")

    # ------------------------------ Export CSV ------------------------------
    def export_csv(self):
        if not self.annotations:
            if not messagebox.askyesno("Export", "No annotations recorded. Export empty CSV?"):
                return

        exp = self.experiment_var.get()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default = f"{exp}_{timestamp}.csv"

        path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            initialfile=default,
            filetypes=[("CSV", "*.csv")]
        )
        if not path:
            return

        with open(path, "w", newline="") as f:
            w = csv.writer(f)
            w.writerow(["Grid", "Row", "Col", "Timestamps", "Frames"])

            for (grid, r, c), entries in sorted(self.annotations.items()):
                times = [t for t, _ in entries]
                frames = [str(f) for _, f in entries]

                w.writerow([
                    grid,
                    r,
                    c,
                    ";".join(times),
                    ";".join(frames)
                ])

        messagebox.showinfo("Export", f"Saved:\n{path}")


# Run
if __name__ == "__main__":
    app = SeedAnnotationApp()
    app.mainloop()
