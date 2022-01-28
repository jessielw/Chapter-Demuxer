# Import the required libraries
from tkinter import filedialog, StringVar, ttk, messagebox, PhotoImage, Menu, LabelFrame, E, N, S, W, Label, \
    Entry, DISABLED, NORMAL, END, Frame, Spinbox, CENTER, Checkbutton, HORIZONTAL, Toplevel, SUNKEN, OptionMenu, \
    Button

from TkinterDnD2 import *
import subprocess, pathlib
from pymediainfo import MediaInfo

chap_extract_win = TkinterDnD.Tk()  # Main loop with DnD.Tk() module (for drag and drop)
chap_extract_win.title('Chapter-Extracting-Tool 1.0')  # Sets the version of the program
chap_extract_win.configure(background="#434547")  # Sets gui background color
window_height = 250  # Gui window height
window_width = 446  # Gui window width
screen_width = chap_extract_win.winfo_screenwidth()  # down
screen_height = chap_extract_win.winfo_screenheight()  # down
x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
chap_extract_win.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # opens window center

chap_extract_win.rowconfigure(3, weight=1)
chap_extract_win.grid_columnconfigure(2, weight=1)


mkvextract = r'"Apps\mkvextract\mkvextract.exe"'
mp4box = r'"Apps\mp4box\mp4box.exe"'


# Hover over button theme ---------------------------------------
class HoverButton(Button):
    def __init__(self, master, **kw):
        Button.__init__(self, master=master, **kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground


# --------------------------------------- Hover over button theme
chapter_extract = LabelFrame(chap_extract_win, text=' Chapter Extraction ')
chapter_extract.grid(row=0, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))
chapter_extract.configure(fg="white", bg="#434547", bd=4)

chapter_extract.grid_columnconfigure(0, weight=1)
chapter_extract.grid_rowconfigure(0, weight=1)


def input_button_commands():  # Open file block of code (non drag and drop)
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output, detect_video_fps, \
        fps_entry, output_quoted, extension_type
    source_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                              filetypes=[("Supported Formats", ('.mp4', '.mkv'))])
    chap_input_entry.configure(state=NORMAL)
    chap_input_entry.delete(0, END)
    chapter_source_input = source_input
    media_info = MediaInfo.parse(pathlib.Path(chapter_source_input))
    for track in media_info.tracks:
        if track.track_type == 'General':
            detect_chapters = track.count_of_menu_streams
    if detect_chapters is None:
        messagebox.showerror(title='Error', message='Input has no chapters')
    elif detect_chapters is not None:
        if chapter_source_input.endswith(('.mp4', '.mkv')):
            if chapter_source_input.endswith('.mp4'):
                extension_type = '.mp4'
            if chapter_source_input.endswith('.mkv'):
                extension_type = '.mkv'
            autofilesave_file_path = pathlib.Path(chapter_source_input)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
            VideoInputQuoted = '"' + str(pathlib.Path(chapter_source_input)) + '"'
            chap_input_entry.insert(0, pathlib.Path(str(chapter_source_input)))
            chap_input_entry.configure(state=DISABLED)
            filename = pathlib.Path(chapter_source_input)
            chapt_input_filename = filename.with_suffix('')
            autosavefilename = str(chapt_input_filename.name) + '.Extracted_Chapters'
            autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.txt'))
            output = str(autosave_file_dir)
            output_quoted = '"' + output + '"'
            chap_output_entry.configure(state=NORMAL)
            chap_output_entry.delete(0, END)
            chap_output_entry.insert(0, str(autosave_file_dir))
            chap_output_entry.configure(state=DISABLED)
            extract_button.configure(state=NORMAL)
            status_label.configure(text='Select Extract')
        else:
            messagebox.showinfo(title='Input Not Supported', message='Try again with a supported file!\n\n' +
                                                                     'Unsupported file extension "' +
                                                                     str(pathlib.Path(chapter_source_input).suffix) +
                                                                     '"')
            extract_button.configure(state=DISABLED)


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def video_drop_input(event):  # Drag and drop function
    input_dnd.set(event.data)


def update_file_input(*args):  # Drag and drop block of code
    global chapter_source_input, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename, output_quoted, extension_type
    chap_input_entry.configure(state=NORMAL)
    chap_input_entry.delete(0, END)
    chapter_source_input = str(input_dnd.get()).replace("{", "").replace("}", "")
    media_info = MediaInfo.parse(pathlib.Path(chapter_source_input))
    for track in media_info.tracks:
        if track.track_type == 'General':
            detect_chapters = track.count_of_menu_streams
    if detect_chapters is None:
        messagebox.showerror(title='Error', message='Input has no chapters')
    elif detect_chapters is not None:
        if chapter_source_input.endswith(('.mp4', '.mkv')):
            if chapter_source_input.endswith('.mp4'):
                extension_type = '.mp4'
            if chapter_source_input.endswith('.mkv'):
                extension_type = '.mkv'
            autofilesave_file_path = pathlib.Path(chapter_source_input)  # Command to get file input location
            autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
            VideoInputQuoted = '"' + str(pathlib.Path(chapter_source_input)) + '"'
            chap_input_entry.insert(0, pathlib.Path(str(input_dnd.get()).replace("{", "").replace("}", "")))
            chap_input_entry.configure(state=DISABLED)
            filename = pathlib.Path(chapter_source_input)
            chapt_input_filename = filename.with_suffix('')
            autosavefilename = str(chapt_input_filename.name) + '.Extracted_Chapters'
            autosave_file_dir = pathlib.Path(str(f'{autofilesave_dir_path}\\') + str(autosavefilename + '.txt'))
            output = str(autosave_file_dir)
            output_quoted = '"' + output + '"'
            chap_output_entry.configure(state=NORMAL)
            chap_output_entry.delete(0, END)
            chap_output_entry.insert(0, str(autosave_file_dir))
            chap_output_entry.configure(state=DISABLED)
            extract_button.configure(state=NORMAL)
            status_label.configure(text='Select Extract')
        else:
            messagebox.showinfo(title='Input Not Supported', message='Try again with a supported file!\n\n' +
                                                                     'Unsupported file extension "' +
                                                                     str(pathlib.Path(chapter_source_input).suffix) +
                                                                     '"')
            extract_button.configure(state=DISABLED)


# --------------------------------------------------------------------------------------------- Drag and Drop Functions

input_dnd = StringVar()
input_dnd.trace('w', update_file_input)
chap_input_button = HoverButton(chapter_extract, text='Input', command=input_button_commands, foreground='white',
                                background='#23272A', borderwidth='3', activebackground='grey', width=15)
chap_input_button.grid(row=0, column=0, columnspan=1, padx=(10, 5), pady=5, sticky=W + E)
chap_input_button.drop_target_register(DND_FILES)
chap_input_button.dnd_bind('<<Drop>>', video_drop_input)

chap_input_entry = Entry(chapter_extract, borderwidth=4, background='#CACACA', state=DISABLED, width=30)
chap_input_entry.grid(row=0, column=1, columnspan=2, padx=(5, 10), pady=5, sticky=W + E)
chap_input_entry.drop_target_register(DND_FILES)
chap_input_entry.dnd_bind('<<Drop>>', video_drop_input)


def output_button_commands():
    global output, output_quoted
    output_window = filedialog.asksaveasfilename(defaultextension=".txt", initialdir=autofilesave_dir_path,
                                                 title="Select a Save Location", initialfile=autosavefilename,
                                                 filetypes=[("ogg.txt", "*.txt")])

    if output_window:
        chap_output_entry.configure(state=NORMAL)
        chap_output_entry.delete(0, END)
        output_quoted = '"' + str(pathlib.Path(output_window)) + '"'
        output = pathlib.Path(output_window)
        chap_output_entry.insert(0, output)
        chap_output_entry.configure(state=DISABLED)


chap_output_button = HoverButton(chapter_extract, text='Output', command=output_button_commands, foreground='white',
                                 background='#23272A', borderwidth='3', activebackground='grey', width=15)
chap_output_button.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=(40, 5), sticky=W + E)
chap_output_entry = Entry(chapter_extract, borderwidth=4, background='#CACACA', state=DISABLED, width=30)
chap_output_entry.grid(row=1, column=1, columnspan=2, padx=(5, 10), pady=(40, 5), sticky=W + E)


def start_job():
    global output
    output_quoted = f'"{output}"'

    if extension_type == '.mp4':
        finalcommand = '"' + mp4box + ' ' + f'"{chapter_source_input}"' + ' -dump-chap-ogg -out ' + output_quoted + '"'
    elif extension_type == '.mkv':
        finalcommand = '"' + mkvextract + ' ' + f'"{chapter_source_input}"' + ' ' + 'chapters -s ' + output_quoted + '"'

    subprocess.check_output('cmd /c ' + finalcommand, universal_newlines=True,
                            creationflags=subprocess.CREATE_NO_WINDOW)

    if pathlib.Path(output).is_file():
        status_label.configure(text='Completed!')


extract_button = HoverButton(chap_extract_win, text='Extract', command=start_job, foreground='white',
                             background='#23272A', borderwidth='3', activebackground='grey', width=15, state=DISABLED)
extract_button.grid(row=2, column=2, columnspan=1, padx=(20, 20), pady=(20, 5), sticky=W + E)

status_label = Label(chap_extract_win, text='Select "Input" or drag and drop a MKV or MP4 file to begin...',
                     bd=4, relief=SUNKEN, anchor=E, background='#717171', foreground="white")
status_label.grid(column=0, row=3, columnspan=4, sticky=W + E, pady=(0, 2), padx=5)

chap_extract_win.mainloop()
