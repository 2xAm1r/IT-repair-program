import tkinter as tk
from tkinter import messagebox, filedialog
import requests
import psutil
import pygame.mixer
import os


class DownloadManager:
    def __init__(self, root):
        self.root = root
        self.root.title("IranSlot QC Test create W Amir")

        # Set the scale factor
        self.scale_factor = 1.0

        # Get the current script directory
        self.script_dir = os.path.dirname(os.path.abspath(__file__))

        # Set the window icon
        icon_path = os.path.join(self.script_dir, 'resources', 'icon.png')
        icon_image = tk.PhotoImage(file=icon_path)
        self.root.tk.call('wm', 'iconphoto', self.root._w, icon_image)

        # Logo image
        logo_path = os.path.join(self.script_dir, 'resources', 'logo.png')
        self.logo_image = tk.PhotoImage(file=logo_path)

        # Initialize pygame mixer for audio
        pygame.mixer.init()

        # Load the music file
        music_path = os.path.join(self.script_dir, 'resources', 'music.mp3')
        pygame.mixer.music.load(music_path)

        # Play the music file in an infinite loop (-1)
        pygame.mixer.music.play(loops=-1)

        # Create UI elements
        self.create_widgets()

        # Configure fullscreen button
        self.fullscreen_button = tk.Button(
            self.root, text="Toggle Fullscreen", command=self.toggle_fullscreen, bg="black", fg="white", font=("Arial", 12))
        self.fullscreen_button.pack(side=tk.BOTTOM, pady=10)

        # Track fullscreen state
        self.fullscreen_state = False

        # Bind resize event
        self.root.bind("<Configure>", self.on_resize)

        # Installation log section
        self.installation_log_label = tk.Label(
            self.root, text="Installation Log:", font=("Arial", 12, "bold"), bg="black", fg="white")
        self.installation_log_label.pack(
            side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

        # Installation log text
        self.installation_log_text = tk.Text(
            self.root, width=60, height=5, font=("Arial", 10), bg="black", fg="white")
        self.installation_log_text.pack()

        # Speeds label
        self.speed_label = tk.Label(
            self.root, text="Download: - bytes/second | Upload: - bytes/second", font=("Arial", 12), bg="black", fg="white")
        self.speed_label.pack(anchor=tk.SE, padx=20, pady=10)

        # Track download and upload speeds
        self.download_speed = 0
        self.upload_speed = 0

        # Update speeds every second
        self.root.after(1000, self.update_speeds)

    def create_widgets(self):
        # Set background color to black
        self.root.configure(bg="black")

        # Logo label
        self.logo_label = tk.Label(
            self.root, image=self.logo_image, bg="black")
        self.logo_label.pack(padx=20, pady=20)

        # Welcome message
        self.welcome_label = tk.Label(
            self.root, text="Welcome to IranSlot", font=("Arial", int(20 * self.scale_factor)), bg="black", fg="white")
        self.welcome_label.pack()

        # QC Test message
        self.qc_label = tk.Label(
            self.root, text="QC test", font=("Arial", int(16 * self.scale_factor)), bg="black", fg="white")
        self.qc_label.pack()

        # Listbox to display items
        self.item_listbox = tk.Listbox(
            self.root, width=int(50 * self.scale_factor), height=int(10 * self.scale_factor), font=("Arial", int(14 * self.scale_factor)), bg="black", fg="white")
        self.item_listbox.pack(pady=20)

        # Add items to the list
        self.item_listbox.insert(tk.END, "Hiddify-Windows")  # Item 1
        self.item_listbox.insert(tk.END, "CPU-Z")            # Item 2
        self.item_listbox.insert(tk.END, "Core-Temp")        # Item 3
        self.item_listbox.insert(tk.END, "Winrar")           # Item 4
        self.item_listbox.insert(tk.END, "Hard Disk Sentinel")  # Item 5
        self.item_listbox.insert(tk.END, "GPU-Z")            # Item 6

        # Download button
        self.download_button = tk.Button(
            self.root, text="Download", command=self.download_selected_item, bg="black", fg="white", font=("Arial", int(14 * self.scale_factor)))
        self.download_button.pack(pady=20)

        # Internet connection status label
        self.connection_label = tk.Label(
            self.root, text="", font=("Arial", int(12 * self.scale_factor)), bg="black", fg="white")
        self.connection_label.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)
        self.update_connection_status()

        # Menu bar
        self.menubar = tk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # File menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="EXIT", menu=self.file_menu)
        self.file_menu.add_command(label="Exit", command=self.root.quit)

    def toggle_fullscreen(self):
        if self.fullscreen_state:
            self.root.attributes('-fullscreen', False)
            self.fullscreen_state = False
            self.scale_factor = 1.0  # Reset scale factor
            self.fullscreen_button.config(text="Toggle Fullscreen")
        else:
            self.root.attributes('-fullscreen', True)
            self.fullscreen_state = True
            self.scale_factor = min(self.root.winfo_screenwidth(
                # Adjust scale factor based on screen size
            ) / 800, self.root.winfo_screenheight() / 600)
            self.fullscreen_button.config(text="Exit Fullscreen")

        self.update_ui_scaling()

    def update_ui_scaling(self):
        # Update welcome label font size
        self.welcome_label.configure(
            font=("Arial", int(20 * self.scale_factor)))

        # Update QC test label font size
        self.qc_label.configure(font=("Arial", int(16 * self.scale_factor)))

        # Update item listbox size and font size
        self.item_listbox.configure(width=int(50 * self.scale_factor), height=int(
            10 * self.scale_factor), font=("Arial", int(14 * self.scale_factor)))

        # Update download button font size
        self.download_button.configure(
            font=("Arial", int(14 * self.scale_factor)))

        # Update connection status label font size
        self.connection_label.configure(
            font=("Arial", int(12 * self.scale_factor)))

        # Update installation log font size
        self.installation_log_label.configure(
            font=("Arial", int(12 * self.scale_factor)))
        self.installation_log_text.configure(
            font=("Arial", int(10 * self.scale_factor)))

        # Update speeds label font size
        self.speed_label.configure(font=("Arial", int(12 * self.scale_factor)))

    def on_resize(self, event):
        if self.fullscreen_state:
            self.scale_factor = min(
                self.root.winfo_width() / 800, self.root.winfo_height() / 600)
            self.update_ui_scaling()

    def update_connection_status(self):
        try:
            requests.get("http://www.google.com", timeout=3)
            self.connection_label.config(text="Connected to Internet")
        except requests.ConnectionError:
            self.connection_label.config(text="Not connected to Internet")

    def update_speeds(self):
        try:
            # Retrieve network speeds
            self.download_speed = psutil.net_io_counters().bytes_recv - self.download_speed
            self.upload_speed = psutil.net_io_counters().bytes_sent - self.upload_speed

            # Update labels with formatted speeds
            self.speed_label.config(text=f"Download: {
                                    self.download_speed} bytes/second | Upload: {self.upload_speed} bytes/second")

            # Reset speeds for next iteration
            self.download_speed = psutil.net_io_counters().bytes_recv
            self.upload_speed = psutil.net_io_counters().bytes_sent

            # Schedule the next update
            self.root.after(1000, self.update_speeds)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update speeds: {str(e)}")

    def download_selected_item(self):
        try:
            # Get selected item
            selected_index = self.item_listbox.curselection()
            if not selected_index:
                messagebox.showwarning(
                    "Warning", "Please select an item to download.")
                return

            item_index = selected_index[0]
            item_name = self.item_listbox.get(item_index)

            # Define download links (replace with actual links)
            download_links = {
                "Hiddify-Windows": "https://github.com/hiddify/hiddify-next/releases/download/v1.4.0/Hiddify-Windows-Setup-x64.exe",
                "CPU-Z": "https://download.cpuid.com/cpu-z/cpu-z_2.09-en.exe",
                "Core-Temp": "https://www.alcpu.com/CoreTemp/Core-Temp-setup.exe",
                "Winrar": "https://www.rarlab.com/rar/winrar-x64-602.exe",
                "Hard Disk Sentinel": "https://www.hdsentinel.com/hard_disk_sentinel_trial_setup.zip",
                "GPU-Z": "https://us2-dl.techpowerup.com/files/GPU-Z.2.42.0.exe"
            }

            if item_name not in download_links:
                messagebox.showerror("Error", "Download link not found.")
                return

            download_url = download_links[item_name]

            # Show file dialog to select download location
            file_path = filedialog.asksaveasfilename(
                defaultextension=".exe", initialfile=os.path.basename(download_url))
            if not file_path:
                return

            # Perform the download
            response = requests.get(download_url, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            block_size = 1024  # 1 KB
            downloaded_size = 0

            with open(file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    downloaded_size += len(data)
                    self.update_progress(downloaded_size, total_size)

            self.installation_log_text.insert(
                tk.END, f"Downloaded {item_name} to {file_path}\n")
            messagebox.showinfo(
                "Success", f"{item_name} downloaded successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to download {
                                 item_name}: {str(e)}")

    def update_progress(self, downloaded, total):
        progress = int((downloaded / total) * 100)
        self.root.title(f"Downloading... {progress}%")


if __name__ == "__main__":
    root = tk.Tk()
    download_manager = DownloadManager(root)
    root.mainloop()
