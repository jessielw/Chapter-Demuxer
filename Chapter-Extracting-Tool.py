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
window_height = 276  # Gui window height
window_width = 446  # Gui window width
screen_width = chap_extract_win.winfo_screenwidth()  # down
screen_height = chap_extract_win.winfo_screenheight()  # down
x_coordinate = int((screen_width / 2) - (window_width / 2))  # down
y_coordinate = int((screen_height / 2) - (window_height / 2))  # down
chap_extract_win.geometry(f'{window_width}x{window_height}+{x_coordinate}+{y_coordinate}')  # opens window center

chap_extract_win.rowconfigure(3, weight=1)
chap_extract_win.grid_columnconfigure(2, weight=1)


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


audio_title_entrybox_label = Label(chap_extract_win, text='Chapter Extractor Tool (MKV and MP4)', anchor=CENTER,
                                   background='#434547', foreground='green')
audio_title_entrybox_label.grid(row=0, column=2, columnspan=1, padx=20, pady=(5, 0), sticky=W + E)
audio_title_entrybox_label.config(font=('Arial Black', 11))

chapter_extract = LabelFrame(chap_extract_win, text=' Chapter Extraction ')
chapter_extract.grid(row=1, columnspan=3, sticky=E + W + N + S, padx=20, pady=(5, 0))
chapter_extract.configure(fg="white", bg="#434547", bd=4)

chapter_extract.grid_columnconfigure(0, weight=1)
chapter_extract.grid_rowconfigure(0, weight=1)


def input_button_commands():  # Open file block of code (non drag and drop)
    global VideoInput, autosavefilename, autofilesave_dir_path, VideoInputQuoted, output, detect_video_fps, \
        fps_entry, output_quoted
    source_input = filedialog.askopenfilename(initialdir="/", title="Select A File",
                                              filetypes=[("Supported Formats", ('.mp4', '.mkv'))])
    chap_input_entry.configure(state=NORMAL)
    chap_input_entry.delete(0, END)
    chapter_source_input = source_input
    if chapter_source_input.endswith(('.mp4', '.mkv')):
        if chapter_source_input.endswith('.mp4'):
            extension_type = '.mp4'
        if chapter_source_input.endswith('.mkv'):
            extension_type = '.mkv'
        autofilesave_file_path = pathlib.Path(chapter_source_input)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(chapter_source_input)) + '"'
        chap_input_entry.insert(0, str(chapter_source_input))
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
    else:
        messagebox.showinfo(title='Input Not Supported', message='Try again with a supported file!\n\n' +
                                                                 'Unsupported file extension "' +
                                                                 str(pathlib.Path(chapter_source_input).suffix) + '"')
        extract_button.configure(state=DISABLED)


# ---------------------------------------------------------------------------------------------- Input Functions Button

# Drag and Drop Functions ---------------------------------------------------------------------------------------------
def video_drop_input(event):  # Drag and drop function
    input_dnd.set(event.data)


def update_file_input(*args):  # Drag and drop block of code
    global chapter_source_input, autofilesave_dir_path, VideoInputQuoted, output, autosavefilename, output_quoted
    chap_input_entry.configure(state=NORMAL)
    chap_input_entry.delete(0, END)
    chapter_source_input = str(input_dnd.get()).replace("{", "").replace("}", "")
    if chapter_source_input.endswith(('.mp4', '.mkv')):
        if chapter_source_input.endswith('.mp4'):
            extension_type = '.mp4'
        if chapter_source_input.endswith('.mkv'):
            extension_type = '.mkv'
        autofilesave_file_path = pathlib.Path(chapter_source_input)  # Command to get file input location
        autofilesave_dir_path = autofilesave_file_path.parents[0]  # Final command to get only the directory
        VideoInputQuoted = '"' + str(pathlib.Path(chapter_source_input)) + '"'
        chap_input_entry.insert(0, str(input_dnd.get()).replace("{", "").replace("}", ""))
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
    else:
        messagebox.showinfo(title='Input Not Supported', message='Try again with a supported file!\n\n' +
                                                                 'Unsupported file extension "' +
                                                                 str(pathlib.Path(chapter_source_input).suffix) + '"')
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
        output = output_window
        chap_output_entry.insert(0, output)
        chap_output_entry.configure(state=DISABLED)


chap_output_button = HoverButton(chapter_extract, text='Output', command=output_button_commands, foreground='white',
                            background='#23272A', borderwidth='3', activebackground='grey', width=15)
chap_output_button.grid(row=1, column=0, columnspan=1, padx=(10, 5), pady=(40, 5), sticky=W + E)
chap_output_entry = Entry(chapter_extract, borderwidth=4, background='#CACACA', state=DISABLED, width=30)
chap_output_entry.grid(row=1, column=1, columnspan=2, padx=(5, 10), pady=(40, 5), sticky=W + E)

extract_button = HoverButton(chap_extract_win, text='Extract', command=input_button_commands, foreground='white',
                        background='#23272A', borderwidth='3', activebackground='grey', width=15, state=DISABLED)
extract_button.grid(row=2, column=2, columnspan=1, padx=(20, 20), pady=(40, 10), sticky=W + E)

# mp4box = r"C:\Users\jlw_4\Desktop\mp4box.exe"
#
# file1 = r"C:\Users\jlw_4\Desktop\The.Blue.Lagoon.1980.REPACK.BluRay.720p.DD.2.0.x264-BHDStudio.mp4"
#
# finalcommand = '"' + mp4box + ' ' + file1 + ' -dump-chap-ogg -std"'
# finalcommand2 = '"' + mp4box + ' ' + file1 + ' -dump-chap-ogg"'
# job = subprocess.Popen('cmd /c ' + finalcommand2, universal_newlines=True,
#                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
#                        creationflags=subprocess.CREATE_NO_WINDOW)
# auto_chapter_input = job.communicate()
# test = auto_chapter_input[0]
# temp_chapter = open(r'C:\Users\jlw_4\Desktop\TESTCHAPTER.txt', 'w')
# temp_chapter.write(test)
# temp_chapter.close()
# print(test)


# mkv extract command = C:\Users\jlw_4\Desktop\mkvtoolnix\mkvextract.exe "\\Jlwserver\h\Futurama\Futurama.S01.NTSC.DVD.DD.2.0.MPEG-2.REMUX-RPG\Futurama - 1x01 - Space Pilot 3000.mkv" chapters -s C:\Users\jlw_4\Desktop\mkvchapters.txt


chap_extract_win.mainloop()
