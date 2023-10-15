import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import shutil
import ctypes

# Definitions
EXTENSIONS = {
    'Audio': ['.aif', '.cda', '.mid', '.midi', '.mp3', '.mpa', '.ogg', '.wav', '.wma', '.wpl'],
    'Compressed': ['.7z', '.arj', '.deb', '.pkg', '.rar', '.rpm', '.tar.gz', '.z', '.zip'],
    'Disc': ['.bin', '.dmg', '.iso', '.toast', '.vcd'],
    'Database': ['.db', '.dbf', '.mdb', '.pdb', '.sql'],
    'Executable': ['.apk', '.bat', '.bin', '.cgi', '.com', '.exe', '.gadget', '.jar', '.py', '.wsf'],
    'Font': ['.fnt', '.fon', '.otf', '.ttf'],
    'Image': ['.ai', '.bmp', '.gif', '.ico', '.jpeg', '.jpg', '.png', '.ps', '.psd', '.svg', '.tif', '.tiff'],
    'Internet': ['.asp', '.aspx', '.cer', '.cfm', '.css', '.htm', '.html', '.js', '.jsp', '.part', '.php', '.rss', '.xhtml'],
    'Presentation': ['.key', '.odp', '.pps', '.ppt', '.pptx'],
    'Programming': ['.c', '.class', '.cpp', '.cs', '.h', '.java', '.pl', '.sh', '.swift', '.vb'],
    'Spreadsheet': ['.ods', '.xlr', '.xls', '.xlsx'],
    'System': ['.bak', '.cab', '.cfg', '.cpl', '.cur', '.dll', '.dmp', '.drv', '.icns', '.ini', '.lnk', '.msi', '.sys', '.tmp'],
    'Video': ['.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv'],
    'Word Processor': ['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wpd'],
    'Other': []
}

LOG_FILENAME = ".organization_log.txt"

def organize_files(directory):
    if not os.path.exists(directory):
        return

    if os.path.exists(os.path.join(directory, LOG_FILENAME)):
        os.remove(os.path.join(directory, LOG_FILENAME))

    handled_files = set()

    for category, extensions in EXTENSIONS.items():
        for ext in extensions:
            for file in os.listdir(directory):
                if file == LOG_FILENAME:  # Skip the log file
                    continue
                if file.endswith(ext):
                    dest_folder = os.path.join(directory, category)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                    
                    source = os.path.join(directory, file)
                    dest = os.path.join(dest_folder, file)

                    shutil.move(source, dest)
                    handled_files.add(file)
                    with open(os.path.join(directory, LOG_FILENAME), 'a') as log_file:
                        log_file.write(f"{source} -> {dest}\n")

    for file in os.listdir(directory):
        if file not in handled_files and not file.endswith(LOG_FILENAME) and not os.path.isdir(os.path.join(directory, file)):
            dest_folder = os.path.join(directory, 'Other')
            if not os.path.exists(dest_folder):
                os.makedirs(dest_folder)
            
            source = os.path.join(directory, file)
            dest = os.path.join(dest_folder, file)

            shutil.move(source, dest)
            with open(os.path.join(directory, LOG_FILENAME), 'a') as log_file:
                log_file.write(f"{source} -> {dest}\n")

    messagebox.showinfo("Info", "Files organized successfully!")


def undo_organization(directory):
    if not os.path.exists(os.path.join(directory, LOG_FILENAME)):
        messagebox.showerror("Error", "Cannot find organization log!")
        return
    
    with open(os.path.join(directory, LOG_FILENAME), 'r') as log_file:
        lines = log_file.readlines()
        for line in reversed(lines):
            source, dest = line.strip().split(" -> ")
            if os.path.exists(dest):
                shutil.move(dest, source)
            folder = os.path.dirname(dest)
            if not os.listdir(folder):
                os.rmdir(folder)

    os.remove(os.path.join(directory, LOG_FILENAME))
    messagebox.showinfo("Info", "Organization has been undone!")

# GUI improvements
class ButtonEnhancedFileOrganizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("500x300")
        self.configure(bg="#2C3E50")
        
        # Create and place widgets
        self.create_widgets()

    def create_widgets(self):
        self.header_label = ttk.Label(self, text="File Organizer", font=("Arial", 20, "bold"), background="#2C3E50", foreground="#ECF0F1")
        self.header_label.pack(pady=20)
        
        self.dir_frame = ttk.Frame(self, padding="10 30")
        self.dir_frame.pack(pady=20, fill="x", expand=True)
        self.dir_var = tk.StringVar()

        lbl = ttk.Label(self.dir_frame, text="Select Directory:", foreground="#000000")
        lbl.pack(side="left", padx=(50, 0))
        self.entry = ttk.Entry(self.dir_frame, textvariable=self.dir_var, width=30)
        self.entry.pack(side="left", padx=10)
        btn_browse = ttk.Button(self.dir_frame, text="Browse", command=self.select_directory, style='TButton')
        btn_browse.pack(side="left")

        btn_organize = ttk.Button(self, text="Organize", command=self.confirm_organize, style='TButton')
        btn_organize.pack(pady=10, padx=50, fill="x")
        btn_undo = ttk.Button(self, text="Undo", command=self.confirm_undo, style='TButton')
        btn_undo.pack(pady=10, padx=50, fill="x")

    def select_directory(self):
        directory = filedialog.askdirectory()
        self.dir_var.set(directory)
        self.entry.delete(0, tk.END)
        self.entry.insert(0, directory)

    def confirm_organize(self):
        confirm = messagebox.askyesno("Confirm", "This will organize the files in the selected directory. Continue?")
        if confirm:
            organize_files(self.dir_var.get())

    def confirm_undo(self):
        confirm = messagebox.askyesno("Confirm", "This will undo the organization in the selected directory. Continue?")
        if confirm:
            undo_organization(self.dir_var.get())

# Running the GUI

# Running the GUI
if __name__ == "__main__":
    app = ButtonEnhancedFileOrganizerGUI()

    # GUI Styling
    style = ttk.Style()
    style.configure('TButton', 
                    
                    foreground='black', 
                    font=('Arial', 8), 
                    borderwidth=0,
                    relief="solid",
                    padding=3)
    
    

    app.mainloop()
