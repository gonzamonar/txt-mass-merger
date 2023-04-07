import tkinter as tk
from tkinter import PhotoImage
from tkinter.filedialog import askdirectory
import json
import os
import requests
import threading


def main_execution():
    root = txt_folder.get()
    massmerge(root)


def massmerge(root: str):
    DIVISION = "*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$*$"
    dest_file = "mass_merged.txt"
    dest_path = os.path.join(root, dest_file)
    c = 0
    update_log("Merge in progress...")

    with open(dest_path, "w", encoding="utf-8") as merged:
        merged.write("List of Files in Folder:\n")
        for _, _, files in os.walk(root):
            for filename in files:
                if filename == dest_file or not filename.endswith(".txt"):
                    continue
                merged.write(filename + "\n")
                c += 1

        for path, _, files in os.walk(root):
            for filename in files:
                if filename == dest_file or not filename.endswith(".txt"):
                    continue
                update_progress(f"Merging file {filename}")
                filepath = os.path.join(path, filename)
                merged.write("\n\n")
                merged.write(DIVISION)
                merged.write("\n\n")
                merged.write(filename)
                merged.write("\n\n")
                merged.write(DIVISION)
                merged.write("\n\n")

                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    merged.write(content)
    
    update_log(f"Merge finished.")
    update_progress(f"[{c} files merged]")


def explore_folder():
    txt_folder.delete(0, 'end')
    tk.Tk().withdraw()
    dirpath = askdirectory()
    txt_folder.insert(0, dirpath)


def update_log(log: str):
    lbl_log.config(text=log)


def update_progress(log: str):
    lbl_progress.config(text=log)


def create_json_config():
    with open("config.json", "w", encoding="utf-8") as jsonfile:
        jsonfile.write(
    """
    {
        "window_icon_name" : "merge-icon.ico",
        "window_icon_url" : "https://raw.githubusercontent.com/gonzamonar/Resources/master/merge-icon.ico",
        "explorer_img_name" : "file-explorer.png",
        "explorer_img_url" : "https://raw.githubusercontent.com/gonzamonar/Resources/master/file-explorer.png",
        "window_size" : "500x220"
    }
    """
    )


def read_json_config():
    with open("config.json", "r", encoding="utf-8") as jsonfile:
        config = json.load(jsonfile)
    return config


def fetch_file(filename: str, url: str):
    if not os.path.exists(filename):
        try:
            content = requests.get(url).content
            with open(filename, 'wb') as handler:
                handler.write(content)
        except:
            pass


def update_jsonconfig(key: str, value: str):
    config[key] = value
    json_obj = json.dumps(config)
    with open("config.json", "w", encoding="utf-8") as jsonfile:
        jsonfile.write(json_obj)


def program_exit():
    window.quit()
    window.destroy()


###################################### USER INTERFACE ######################################
FONT = ("", "9", "bold")

## LOADING & VERIFYING RESOURCES ##
if not os.path.exists("config.json"):
    create_json_config()

try:
    config = read_json_config()
except FileNotFoundError:
    create_json_config()
    try:
        config = read_json_config()
    except FileNotFoundError:
        normal_init = False


fetch_file(config["window_icon_name"], config["window_icon_url"])
fetch_file(config["explorer_img_name"], config["explorer_img_url"])


### WINDOW INIT ###
window = tk.Tk()
window.title("Txt Mass Merger")
window.geometry(config["window_size"])
window.resizable(False, False)

try:
    window.iconbitmap(config["window_icon_name"])
except tk.TclError:
    pass

if os.path.exists(config["explorer_img_name"]):
    img_explorer = PhotoImage(file=config["explorer_img_name"])
else:
    img_explorer = None


### FRAME 1 - FILE SELECTION ###
frame1 = tk.Frame(window)
frame1.grid(row=0, columnspan=2)

lbl_section1 = tk.Label(frame1, text="Folder selection", font=FONT)
lbl_section1.grid(row=0, columnspan=3, padx=5, pady=(10, 0))

lbl_folder = tk.Label(frame1, text="Folder path: ")
lbl_folder.grid(row=1, column=0, padx=5, pady=5, sticky="e")
txt_folder = tk.Entry(frame1, width=60, state="normal")
txt_folder.grid(row=1, column=1, padx=5, pady=5)

    #· EXPLORER BTN IMG ·#
btn_folder_explorer = tk.Button(frame1, image=img_explorer, command=explore_folder, borderwidth=0, state="normal")
btn_folder_explorer.grid(row=1, column=2, padx=5, pady=5)

### SECTION 2 - LOGGER ###
lbl1_section2 = tk.Label(window, text="Progress status:", font=FONT, anchor="e")
lbl1_section2.grid(row=1, column=0, padx=5, pady=(15, 5))
lbl2_section2 = tk.Label(window, text="Files status:", font=FONT, anchor="e")
lbl2_section2.grid(row=1, column=1, padx=5, pady=(15, 5))
lbl_log = tk.Label(window, text="", width=30, bg="#FFFFFF", anchor="w")
lbl_log.grid(row=2, column=0, padx=10, pady=(0, 5))
lbl_progress = tk.Label(window, text="", width=30, bg="#FFFFFF", anchor="w")
lbl_progress.grid(row=2, column=1, padx=10, pady=(0, 5))


### SECTION 3 - SUBMIT ###
btn_submit = tk.Button(window, text="MERGE", width=60, bg="#FFFFFF", command= lambda : threading.Thread(target=main_execution).start() )
btn_submit.grid(row=3, columnspan=2, padx=10, pady=25)


## MAIN LOOP ##
window.protocol("WM_DELETE_WINDOW", program_exit)
window.mainloop()
