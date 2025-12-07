import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import threading
import os
import subprocess
import sys
import re
import locale
from downloader import VideoDownloader

# Translation Dictionary
TRANSLATIONS = {
    "en": {
        "title": "Ultimate Video Downloader",
        "header": "Video Downloader & Player",
        "download_frame": "Download",
        "url_label": "Video URL:",
        "paste": "Paste",
        "filename_label": "Filename (opt.):",
        "start_download": "Start Download",
        "waiting": "Waiting...",
        "downloaded_frame": "Downloaded Videos",
        "refresh": "Refresh",
        "open_folder": "Open Folder",
        "play": "Play",
        "col_name": "Filename",
        "col_size": "Size",
        "error": "Error",
        "error_url": "Please enter a URL!",
        "downloading": "Downloading...",
        "stopping": "Stopping and deleting...",
        "processing": "Processing / Converting...",
        "starting_conv": "Starting conversion...",
        "done": "Download successful, file ready!",
        "success": "Success",
        "error_download": "Error during download:",
        "ui_lang": "Language:",
        "restart_req": "(Restart required)",
        "download_prefix": "Download:",
        "converting": "Converting",
        "error_occurred": "Error occurred",
        "error_details": "Error during download:\n",
        "delete": "Delete",
        "confirm_delete": "Confirm Delete",
        "delete_confirm_msg": "Are you sure you want to delete this file?"
    },
    "hu": {
        "title": "Ultimate Video Letöltő",
        "header": "Video Letöltő & Lejátszó",
        "download_frame": "Letöltés",
        "url_label": "Videó URL:",
        "paste": "Beillesztés",
        "filename_label": "Fájlnév (opc.):",
        "start_download": "Letöltés Indítása",
        "waiting": "Várakozás...",
        "downloaded_frame": "Letöltött Videók",
        "refresh": "Frissítés",
        "open_folder": "Mappa Megnyitása",
        "play": "Lejátszás",
        "col_name": "Fájlnév",
        "col_size": "Méret",
        "error": "Hiba",
        "error_url": "Kérlek adj meg egy URL-t!",
        "downloading": "Letöltés folyamatban...",
        "stopping": "Leállítás és törlés...",
        "processing": "Feldolgozás / Konvertálás...",
        "starting_conv": "Konvertálás indítása...",
        "done": "Sikeres letöltés, kész a fájl!",
        "success": "Siker",
        "error_download": "Hiba történt a letöltés során:",
        "ui_lang": "Nyelv:",
        "restart_req": "(Újraindítás szükséges)",
        "download_prefix": "Letöltés:",
        "converting": "Konvertálás",
        "error_occurred": "Hiba történt",
        "error_details": "Hiba történt a letöltés során:\n",
        "delete": "Törlés",
        "confirm_delete": "Törlés megerősítése",
        "delete_confirm_msg": "Biztosan törölni szeretné ezt a fájlt?"
    },
    "de": {
        "title": "Ultimativer Video-Downloader",
        "header": "Video-Downloader & Player",
        "download_frame": "Herunterladen",
        "url_label": "Video-URL:",
        "paste": "Einfügen",
        "filename_label": "Dateiname (opt.):",
        "start_download": "Download starten",
        "waiting": "Warten...",
        "downloaded_frame": "Heruntergeladene Videos",
        "refresh": "Aktualisieren",
        "open_folder": "Ordner öffnen",
        "play": "Abspielen",
        "col_name": "Dateiname",
        "col_size": "Größe",
        "error": "Fehler",
        "error_url": "Bitte geben Sie eine URL ein!",
        "downloading": "Wird heruntergeladen...",
        "stopping": "Stoppen und löschen...",
        "processing": "Verarbeitung / Konvertierung...",
        "starting_conv": "Konvertierung starten...",
        "done": "Fertig!",
        "success": "Erfolg",
        "error_download": "Fehler beim Herunterladen:",
        "ui_lang": "Sprache:",
        "restart_req": "(Neustart erforderlich)",
        "download_prefix": "Download:",
        "converting": "Konvertierung",
        "error_occurred": "Fehler aufgetreten",
        "error_details": "Fehler beim Herunterladen:\n",
        "delete": "Löschen",
        "confirm_delete": "Löschen bestätigen",
        "delete_confirm_msg": "Möchten Sie diese Datei wirklich löschen?"
    },
    "ru": {
        "title": "Ultimate Video Downloader",
        "header": "Загрузчик и плеер видео",
        "download_frame": "Загрузка",
        "url_label": "URL видео:",
        "paste": "Вставить",
        "filename_label": "Имя файла (опц.):",
        "start_download": "Начать загрузку",
        "waiting": "Ожидание...",
        "downloaded_frame": "Загруженные видео",
        "refresh": "Обновить",
        "open_folder": "Открыть папку",
        "play": "Воспроизвести",
        "col_name": "Имя файла",
        "col_size": "Размер",
        "error": "Ошибка",
        "error_url": "Пожалуйста, введите URL!",
        "downloading": "Загрузка...",
        "stopping": "Остановка и удаление...",
        "processing": "Обработка / Конвертация...",
        "starting_conv": "Начало конвертации...",
        "done": "Готово!",
        "success": "Успех",
        "error_download": "Ошибка при загрузке:",
        "ui_lang": "Язык:",
        "restart_req": "(Требуется перезапуск)",
        "download_prefix": "Загрузка:",
        "converting": "Конвертация",
        "error_occurred": "Произошла ошибка",
        "error_details": "Ошибка при загрузке:\n",
        "delete": "Удалить",
        "confirm_delete": "Подтвердить удаление",
        "delete_confirm_msg": "Вы уверены, что хотите удалить этот файл?"
    },
    # Add other languages similarly (simplified for brevity, defaulting missing to English)
}

# Ensure all requested languages exist (fallback to English if not fully defined above)
SUPPORTED_LANGS = ["en", "hu", "de", "ru", "sv", "no", "it", "es", "fr", "sk", "ro", "hr", "tr", "el"]
for lang in SUPPORTED_LANGS:
    if lang not in TRANSLATIONS:
        TRANSLATIONS[lang] = TRANSLATIONS["en"] # Fallback

class VideoDownloaderApp(tb.Window):
    def __init__(self):
        super().__init__(themename="darkly")
        
        # Language Detection
        self.current_lang = self.detect_language()
        self.t = TRANSLATIONS.get(self.current_lang, TRANSLATIONS["en"])

        self.title(self.t["title"])
        self.geometry("900x650")
        
        self.downloader = VideoDownloader()
        self.download_folder = os.path.join(os.getcwd(), "Downloads")
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # State variables for clean exit
        self.is_downloading = False
        self.aborting = False
        self.current_filename = None
        
        # Handle window closing
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.create_widgets()
        self.refresh_file_list()

    def detect_language(self):
        try:
            # Avoid DeprecationWarning: locale.getdefaultlocale()
            sys_lang = os.environ.get('LANG')
            if not sys_lang:
                sys_lang = locale.getlocale()[0]

            if sys_lang:
                code = sys_lang.split('_')[0]
                if code in SUPPORTED_LANGS:
                    return code
        except:
            pass
        return "en"

    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=BOTH, expand=YES)

        # Header
        lbl_header = ttk.Label(main_frame, text=self.t["header"], font=("Helvetica", 24, "bold"), bootstyle="primary")
        lbl_header.pack(pady=(0, 20))

        # URL Input Area
        input_frame = ttk.LabelFrame(main_frame, text=self.t["download_frame"], padding=10)
        input_frame.pack(fill=X, pady=10)

        url_frame = ttk.Frame(input_frame)
        url_frame.pack(fill=X)
        
        ttk.Label(url_frame, text=self.t["url_label"]).pack(side=LEFT, padx=(0, 10))
        self.url_var = tk.StringVar()
        self.entry_url = ttk.Entry(url_frame, textvariable=self.url_var)
        self.entry_url.pack(side=LEFT, fill=X, expand=YES, padx=(0, 10))
        self.setup_context_menu(self.entry_url)
        
        btn_paste = ttk.Button(url_frame, text=self.t["paste"], command=self.paste_url, bootstyle="secondary-outline")
        btn_paste.pack(side=LEFT)

        # Filename Input Area (Optional)
        name_frame = ttk.Frame(input_frame)
        name_frame.pack(fill=X, pady=(10, 0))
        
        ttk.Label(name_frame, text=self.t["filename_label"]).pack(side=LEFT, padx=(0, 10))
        self.filename_var = tk.StringVar()
        self.entry_filename = ttk.Entry(name_frame, textvariable=self.filename_var)
        self.entry_filename.pack(side=LEFT, fill=X, expand=YES)
        self.setup_context_menu(self.entry_filename)
        ttk.Label(name_frame, text=".mp4").pack(side=LEFT)

        # Options Area
        opts_frame = ttk.Frame(input_frame)
        opts_frame.pack(fill=X, pady=(10, 0))

        # Action Buttons
        btn_frame = ttk.Frame(input_frame)
        btn_frame.pack(fill=X, pady=10)
        
        self.btn_download = ttk.Button(btn_frame, text=self.t["start_download"], command=self.start_download, bootstyle="success")
        self.btn_download.pack(side=RIGHT)
        
        self.lbl_status = ttk.Label(btn_frame, text=self.t["waiting"], bootstyle="info")
        self.lbl_status.pack(side=LEFT, padx=5)

        # Progress Bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(input_frame, variable=self.progress_var, maximum=100, bootstyle="success-striped")
        self.progress_bar.pack(fill=X, pady=10)

        # File List / Player Area
        list_frame = ttk.LabelFrame(main_frame, text=self.t["downloaded_frame"], padding=10)
        list_frame.pack(fill=BOTH, expand=YES, pady=10)

        # Toolbar for list
        toolbar = ttk.Frame(list_frame)
        toolbar.pack(fill=X, pady=(0, 5))
        
        ttk.Button(toolbar, text=self.t["refresh"], command=self.refresh_file_list, bootstyle="info-outline").pack(side=LEFT, padx=2)
        ttk.Button(toolbar, text=self.t["open_folder"], command=self.open_folder, bootstyle="secondary-outline").pack(side=LEFT, padx=2)
        ttk.Button(toolbar, text=self.t["play"], command=self.play_video, bootstyle="warning").pack(side=RIGHT, padx=2)
        ttk.Button(toolbar, text=self.t["delete"], command=self.delete_video, bootstyle="danger-outline").pack(side=RIGHT, padx=2)

        # Treeview for files
        columns = ("name", "size")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("name", text=self.t["col_name"])
        self.tree.heading("size", text=self.t["col_size"])
        self.tree.column("name", width=500)
        self.tree.column("size", width=100, anchor="e")
        
        scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=LEFT, fill=BOTH, expand=YES)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.tree.bind("<Double-1>", lambda e: self.play_video())

    def setup_context_menu(self, widget):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label=self.t["paste"], command=lambda: widget.event_generate("<<Paste>>"))
        
        def show_menu(event):
            menu.tk_popup(event.x_root, event.y_root)
            
        widget.bind("<Button-3>", show_menu)

    def paste_url(self):
        try:
            self.url_var.set(self.clipboard_get())
        except:
            pass

    def start_download(self):
        url = self.url_var.get()
        custom_name = self.filename_var.get().strip()
        
        if not url:
            messagebox.showwarning(self.t["error"], self.t["error_url"])
            return

        self.btn_download.config(state=DISABLED)
        self.lbl_status.config(text=self.t["downloading"])
        self.progress_var.set(0)
        
        # Reset state
        self.is_downloading = True
        self.aborting = False
        self.current_filename = None

        thread = threading.Thread(target=self.run_download, args=(url, custom_name))
        thread.start()

    def run_download(self, url, custom_name=None):
        # Define a thread-safe hook that runs in the download thread
        def thread_hook(d):
            if self.aborting:
                raise Exception("ABORT_BY_USER")
            # Schedule GUI update on main thread
            self.after(0, lambda: self.update_progress(d))

        self.downloader.download(
            url, 
            self.download_folder, 
            custom_filename=custom_name,
            progress_hook=thread_hook,
            completion_hook=self.queue_finished
        )

    def queue_finished(self, success, message):
        """Thread-safe wrapper for download_finished"""
        self.after(0, lambda: self.download_finished(success, message))

    def update_progress(self, d):
        # Capture filename for cleanup
        if d.get('filename'):
            self.current_filename = d['filename']

        # Download phase
        if d.get('status') == 'downloading':
            self.progress_bar.configure(bootstyle="primary-striped") # Blue
            
            percent = 0
            got_percent = False
            
            try:
                # 1. Try calculating from bytes (most accurate)
                if d.get('total_bytes') and d.get('downloaded_bytes'):
                    percent = d['downloaded_bytes'] / d['total_bytes'] * 100
                    got_percent = True
                # 2. Try calculating from estimate
                elif d.get('total_bytes_estimate') and d.get('downloaded_bytes'):
                    percent = d['downloaded_bytes'] / d['total_bytes_estimate'] * 100
                    got_percent = True
                # 3. Fallback to string parsing
                else:
                    p_str = d.get('_percent_str', '').replace('%','')
                    # Remove ANSI codes
                    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                    p_str = ansi_escape.sub('', p_str)
                    # Extract number
                    match = re.search(r"(\d+\.?\d*)", p_str)
                    if match:
                        percent = float(match.group(1))
                        got_percent = True
            except Exception:
                pass

            if got_percent:
                self.progress_bar.stop()
                self.progress_bar.configure(mode='determinate')
                self.progress_var.set(percent)
                
                eta = d.get('_eta_str', '?')
                speed = d.get('_speed_str', '?')
                # Clean up strings
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                if isinstance(eta, str): eta = ansi_escape.sub('', eta)
                if isinstance(speed, str): speed = ansi_escape.sub('', speed)
                
                self.lbl_status.config(text=f"{self.t['download_prefix']} {percent:.1f}% - {eta} ({speed})")
            else:
                # Unknown progress (e.g. HLS stream without size)
                self.progress_bar.configure(mode='indeterminate')
                self.progress_bar.start(10)
                speed = d.get('_speed_str', '')
                ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
                if isinstance(speed, str): speed = ansi_escape.sub('', speed)
                self.lbl_status.config(text=f"{self.t['downloading']} {speed}")
        
        # Download finished, starting post-processing
        elif d.get('status') == 'finished':
            self.progress_bar.stop()
            self.progress_bar.configure(mode='determinate', bootstyle="danger-striped") # Red
            self.progress_var.set(100)
            self.lbl_status.config(text=self.t["processing"])
            # If this is a post-processor hook
            if 'postprocessor' in d:
                self.lbl_status.config(text=f"{self.t['converting']} ({d.get('postprocessor')})...")

        # Post-processor started
        elif d.get('status') == 'started':
            self.progress_bar.configure(bootstyle="danger-striped") # Red
            self.lbl_status.config(text=self.t["starting_conv"])
            self.progress_bar.configure(mode='indeterminate')
            self.progress_bar.start(10) # Indeterminate animation for conversion

    def download_finished(self, success, message):
        self.is_downloading = False
        self.progress_bar.stop() # Stop animation if running
        
        if self.aborting:
            self.cleanup_and_close()
            return

        self.after(0, lambda: self._finish_gui(success, message))

    def on_closing(self):
        if self.is_downloading:
            # If downloading, trigger abort
            self.aborting = True
            self.lbl_status.config(text=self.t["stopping"], bootstyle="danger")
            
            # Force kill aria2c to unblock yt-dlp immediately
            try:
                subprocess.run(["pkill", "aria2c"], check=False)
            except:
                pass

            # Schedule force exit to ensure window closes
            self.after(1000, self.force_close)
        else:
            self.destroy()
            sys.exit(0)

    def force_close(self):
        """Forces the application to close and cleanup."""
        self.cleanup_files()
        self.destroy()
        os._exit(0) # Force kill process and threads

    def cleanup_and_close(self):
        """Called by download thread when abort is successful."""
        self.cleanup_files()
        self.destroy()
        sys.exit(0)

    def cleanup_files(self):
        """Deletes partial files."""
        if self.current_filename:
            try:
                # Try to remove the main file
                if os.path.exists(self.current_filename):
                    os.remove(self.current_filename)
                
                # Try to remove temporary files (.part, .aria2, .temp)
                for ext in ['.part', '.aria2', '.temp', '.ytdl']:
                    f = self.current_filename + ext
                    if os.path.exists(f):
                        os.remove(f)
            except Exception as e:
                print(f"Cleanup error: {e}")

    def _finish_gui(self, success, message):
        self.btn_download.config(state=NORMAL)
        if success:
            self.lbl_status.config(text=self.t["done"], bootstyle="success")
            self.progress_bar.configure(bootstyle="success") # Green
            
            # No popup for success, just status update
            
            self.url_var.set("")
            self.progress_var.set(100)
            self.refresh_file_list()
        else:
            self.lbl_status.config(text=self.t["error_occurred"], bootstyle="danger")
            self.progress_bar.configure(bootstyle="danger")
            messagebox.showerror(self.t["error"], f"{self.t['error_details']}\n{message}")

    def refresh_file_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        if not os.path.exists(self.download_folder):
            return

        for f in os.listdir(self.download_folder):
            if f.lower().endswith(('.mp4', '.mkv', '.webm', '.avi', '.mp3', '.m4a')):
                path = os.path.join(self.download_folder, f)
                size_mb = os.path.getsize(path) / (1024 * 1024)
                self.tree.insert("", END, values=(f, f"{size_mb:.1f} MB"))

    def open_folder(self):
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", self.download_folder])
        elif sys.platform == 'win32':
            os.startfile(self.download_folder)
        elif sys.platform == 'darwin':
            subprocess.call(["open", self.download_folder])

    def play_video(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        filename = self.tree.item(selected[0])['values'][0]
        filepath = os.path.join(self.download_folder, filename)
        
        if sys.platform == 'linux':
            subprocess.call(["xdg-open", filepath])
        elif sys.platform == 'win32':
            os.startfile(filepath)
        elif sys.platform == 'darwin':
            subprocess.call(["open", filepath])

    def delete_video(self):
        selected = self.tree.selection()
        if not selected:
            return
        
        filename = self.tree.item(selected[0])['values'][0]
        filepath = os.path.join(self.download_folder, filename)
        
        if messagebox.askyesno(self.t["confirm_delete"], f"{self.t['delete_confirm_msg']}\n{filename}"):
            try:
                if os.path.exists(filepath):
                    os.remove(filepath)
                self.refresh_file_list()
            except Exception as e:
                messagebox.showerror(self.t["error"], str(e))

if __name__ == "__main__":
    app = VideoDownloaderApp()
    app.mainloop()
