import os
import threading
import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image
import io
import platform

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

ctk.set_widget_scaling(1.4)  
ctk.set_window_scaling(1.4)

class RDR2ConverterFinal(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎮 RDR2 Photo Converter Pro")
        self.geometry("1100x850")
        self.minsize(900, 700)
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.source_folder = tk.StringVar()
        self.dest_folder = tk.StringVar()
        self.save_mode = tk.StringVar(value="same")
        self.export_format = tk.StringVar(value="jpg")
        self.rename_mode = tk.StringVar(value="Numbered Sequence")
        self.log_visible = False
        
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dest_folder.set(desktop)

        self.main_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.main_scroll.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.main_scroll.grid_columnconfigure(0, weight=1)

        self.bind_mouse_scroll(self.main_scroll)

        self.create_header()
        self.create_folder_selection()
        self.create_save_location()
        self.create_options()
        self.create_console()
        self.create_footer()

    def bind_mouse_scroll(self, scroll_frame):
        def _on_mousewheel(event):
            if platform.system() == "Windows":
                scroll_frame._parent_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif platform.system() == "Darwin":
                scroll_frame._parent_canvas.yview_scroll(int(-1*event.delta), "units")
            else:
                if event.num == 4:
                    scroll_frame._parent_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    scroll_frame._parent_canvas.yview_scroll(1, "units")

        self.bind_all("<MouseWheel>", _on_mousewheel)
        self.bind_all("<Button-4>", _on_mousewheel)
        self.bind_all("<Button-5>", _on_mousewheel)

    def create_header(self):
        header = ctk.CTkFrame(self.main_scroll, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        header.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
                
        title = ctk.CTkLabel(header, text="🎮 RDR2 PHOTO CONVERTER", 
                             font=("Impact", 42), text_color="#FF6B35")
        title.pack(pady=(20, 5), padx=20)
        
        subtitle = ctk.CTkLabel(header, text="Professional High-DPI Extraction Tool", 
                                font=("Arial", 16, "bold"), text_color="#888888")
        subtitle.pack(pady=(0, 20))

    def create_folder_selection(self):
        frame = ctk.CTkFrame(self.main_scroll, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        lbl_header = ctk.CTkLabel(frame, text="📂 STEP 1: SELECT SOURCE FOLDER", 
                                  font=("Arial", 20, "bold"), text_color="#FF6B35")
        lbl_header.pack(pady=(20, 15))

        src_container = ctk.CTkFrame(frame, fg_color="transparent")
        src_container.pack(fill="x", padx=25, pady=(0, 20))

        self.entry_src = ctk.CTkEntry(
            src_container, 
            textvariable=self.source_folder,
            placeholder_text="Select your PRDR files folder...",
            height=60,
            font=("Arial", 16),
            border_width=2,
            border_color="#FF6B35"
        )
        self.entry_src.pack(side="left", fill="x", expand=True, padx=(0, 15))

        btn_src = ctk.CTkButton(
            src_container,
            text="📁 BROWSE",
            width=180,
            height=60,
            fg_color="#FF6B35",
            hover_color="#FF8C5A",
            font=("Arial", 16, "bold"),
            command=self.select_source
        )
        btn_src.pack(side="right")
        
        self.count_label = ctk.CTkLabel(frame, text="No files detected", font=("Arial", 16, "italic"), text_color="#888888")
        self.count_label.pack(pady=(0, 20))

    def create_save_location(self):
        frame = ctk.CTkFrame(self.main_scroll, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")

        lbl_header = ctk.CTkLabel(frame, text="💾 STEP 2: CHOOSE SAVE LOCATION", 
                                  font=("Arial", 20, "bold"), text_color="#2CC985")
        lbl_header.pack(pady=(20, 15))

        btn_container = ctk.CTkFrame(frame, fg_color="transparent")
        btn_container.pack(fill="x", padx=25, pady=(0, 20))

        self.btn_same = ctk.CTkButton(
            btn_container,
            text="📍 SAME AS SOURCE",
            height=65,
            font=("Arial", 15, "bold"),
            fg_color="#2CC985",
            text_color="black",
            border_width=3,
            border_color="white",
            command=lambda: self.set_save_mode("same")
        )
        self.btn_same.pack(side="left", expand=True, padx=(0, 10))

        self.btn_custom = ctk.CTkButton(
            btn_container,
            text="🗺️ CHOOSE ELSEWHERE",
            height=65,
            font=("Arial", 15, "bold"),
            fg_color="#333333",
            command=lambda: self.set_save_mode("custom")
        )
        self.btn_custom.pack(side="left", expand=True, padx=(10, 0))

        self.custom_container = ctk.CTkFrame(frame, fg_color="transparent")
        
        self.entry_dest = ctk.CTkEntry(
            self.custom_container,
            textvariable=self.dest_folder,
            height=60,
            font=("Arial", 16),
            border_width=2,
            border_color="#2CC985"
        )
        self.entry_dest.pack(side="left", fill="x", expand=True, padx=(25, 15), pady=20)

        btn_dest = ctk.CTkButton(
            self.custom_container,
            text="📂 BROWSE",
            width=150,
            height=60,
            fg_color="#2CC985",
            text_color="black",
            font=("Arial", 15, "bold"),
            command=self.select_dest
        )
        btn_dest.pack(side="right", padx=(0, 25), pady=20)

    def set_save_mode(self, mode):
        self.save_mode.set(mode)
        if mode == "same":
            self.btn_same.configure(fg_color="#2CC985", text_color="black", border_width=3)
            self.btn_custom.configure(fg_color="#333333", text_color="white", border_width=0)
            self.custom_container.pack_forget()
        else:
            self.btn_custom.configure(fg_color="#2CC985", text_color="black", border_width=3)
            self.btn_same.configure(fg_color="#333333", text_color="white", border_width=0)
            self.custom_container.pack(fill="x")

    def create_options(self):
        frame = ctk.CTkFrame(self.main_scroll, fg_color=("#2b2b2b", "#1a1a1a"), corner_radius=15)
        frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        ctk.CTkLabel(frame, text="⚙️ STEP 3: OPTIONS", font=("Arial", 20, "bold"), text_color="#4A90E2").pack(pady=15)

        opt_grid = ctk.CTkFrame(frame, fg_color="transparent")
        opt_grid.pack(fill="x", padx=25, pady=(0, 20))

        fmt_box = ctk.CTkFrame(opt_grid, fg_color="#252525", corner_radius=10)
        fmt_box.pack(side="left", fill="both", expand=True, padx=(0, 10))
        ctk.CTkLabel(fmt_box, text="FORMAT", font=("Arial", 15, "bold")).pack(pady=10)
        ctk.CTkRadioButton(fmt_box, text="JPG", variable=self.export_format, value="jpg", font=("Arial", 14)).pack(pady=5)
        ctk.CTkRadioButton(fmt_box, text="PNG", variable=self.export_format, value="png", font=("Arial", 14)).pack(pady=5)

        name_box = ctk.CTkFrame(opt_grid, fg_color="#252525", corner_radius=10)
        name_box.pack(side="right", fill="both", expand=True, padx=(10, 0))
        ctk.CTkLabel(name_box, text="NAMING", font=("Arial", 15, "bold")).pack(pady=10)
        ctk.CTkOptionMenu(name_box, variable=self.rename_mode, height=40, font=("Arial", 14),
                          values=["Numbered Sequence", "Date Taken", "Keep Original"]).pack(pady=10, padx=20)

    def create_console(self):
        self.console_container = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        self.console_container.grid(row=4, column=0, padx=20, pady=10, sticky="ew")

        self.btn_toggle_log = ctk.CTkButton(
            self.console_container, 
            text="▼ SHOW ACTIVITY LOG", 
            fg_color="#333333", 
            height=40,
            command=self.toggle_log
        )
        self.btn_toggle_log.pack(fill="x")

        self.log_box = ctk.CTkTextbox(
            self.console_container, 
            font=("Consolas", 14), 
            height=250, 
            fg_color="black", 
            border_width=2, 
            border_color="#FF6B35"
        )

    def toggle_log(self):
        if not self.log_visible:
            self.log_box.pack(fill="x", pady=(10, 0))
            self.btn_toggle_log.configure(text="▲ HIDE ACTIVITY LOG")
            self.log_visible = True
        else:
            self.log_box.pack_forget()
            self.btn_toggle_log.configure(text="▼ SHOW ACTIVITY LOG")
            self.log_visible = False

    def create_footer(self):
        footer = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        footer.grid(row=5, column=0, padx=20, pady=30, sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(footer, height=25, progress_color="#FF6B35")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 20))

        self.btn_convert = ctk.CTkButton(
            footer,
            text="PLEASE SELECT SOURCE FOLDER",
            height=90,
            font=("Arial", 28, "bold"),
            fg_color="#444444",
            state="disabled",
            command=self.start_thread,
            corner_radius=15
        )
        self.btn_convert.pack(fill="x")

    def log_message(self, msg):
        self.log_box.configure(state="normal")
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{ts}] {msg}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def select_source(self):
        path = filedialog.askdirectory()
        if path:
            self.source_folder.set(path)
            if self.save_mode.get() == "same":
                self.dest_folder.set(path)
            files = [f for f in os.listdir(path) if f.startswith("PRDR")]
            count = len(files)
            if count > 0:
                self.count_label.configure(text=f"✅ {count} photos detected!", text_color="#2CC985")
                self.btn_convert.configure(state="normal", fg_color="#C80000", text=f"🚀 START CONVERTING {count} PHOTOS")
                self.log_message(f"Found {count} files.")
            else:
                self.count_label.configure(text="❌ No PRDR files found", text_color="#FF4444")
                self.btn_convert.configure(state="disabled", fg_color="#444444", text="NO FILES FOUND")

    def select_dest(self):
        path = filedialog.askdirectory()
        if path:
            self.dest_folder.set(path)

    def start_thread(self):
        self.btn_convert.configure(state="disabled", text="CONVERTING...")
        t = threading.Thread(target=self.run_conversion)
        t.start()

    def run_conversion(self):
        src, dst = self.source_folder.get(), self.dest_folder.get()
        out_dir = os.path.join(dst, "Extracted_RDR2_Photos")
        os.makedirs(out_dir, exist_ok=True)
        
        files = [f for f in os.listdir(src) if f.startswith("PRDR")]
        total = len(files)
        
        self.log_message(f"Starting extraction to: {out_dir}")

        for i, filename in enumerate(files):
            try:
                with open(os.path.join(src, filename), "rb") as f:
                    f.seek(300)
                    data = f.read()

                name = filename
                if self.rename_mode.get() == "Numbered Sequence":
                    name = f"Photo_{i+1:03d}"
                elif self.rename_mode.get() == "Date Taken":
                    ts = os.path.getmtime(os.path.join(src, filename))
                    name = f"RDR2_{datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d_%H%M%S')}_{i}"

                ext = self.export_format.get()
                out_path = os.path.join(out_dir, f"{name}.{ext}")
                
                if ext == "jpg":
                    with open(out_path, "wb") as f: f.write(data)
                else:
                    Image.open(io.BytesIO(data)).save(out_path, "PNG")

                self.progress_bar.set((i + 1) / total)
                self.log_message(f"Converted: {name}.{ext}")
            except Exception as e:
                self.log_message(f"Error: {str(e)}")

        self.btn_convert.configure(state="normal", text="DONE! CONVERT AGAIN?")
        messagebox.showinfo("Success", f"Extraction Complete!\nFolder: {out_dir}")

if __name__ == "__main__":
    app = RDR2ConverterFinal()
    app.mainloop()