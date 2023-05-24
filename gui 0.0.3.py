"""
Author: Nathan Brightup
Date: May 23, 2023
Description: GUI for Scarp project
"""
import tkinter
import customtkinter
from tkinter import *
from customtkinter import *
from spinbox import Spinbox
from PIL import Image, ImageTk
import cv2

# Set intended appearance for the overall background
customtkinter.set_appearance_mode("dark")  # Other available options: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Other available themes: blue (default), dark-blue, green

# Create and size main window, but allow the user to resize it. Initialized to 889x500 to maintain 16:9 aspect ratio (same as 1920x1080)
mainwin = customtkinter.CTk()
mainwin.title("Overall GUI")
mainwin.geometry("889x500")
mainwin.resizable(True, True)
mainwin.minsize(width=889, height=500)

# Create internal frames
frame_1 = Frame(mainwin, bg='grey')
frame_1.grid(row=0, column=0, sticky="nsew")

frame_2 = Frame(mainwin, bg='grey')
frame_2.grid(row=0, column=1, sticky="nsew")

camframe = Frame(mainwin, bg='grey')
camframe.grid(row=0, column=2, sticky="nsew")

# Configure column weights for main window
mainwin.grid_columnconfigure(0, weight=1)
mainwin.grid_columnconfigure(1, weight=1)
mainwin.grid_columnconfigure(2, weight=1)

# Fill internal frames, starting with the leftmost frame 'Tuning'
Tuning = Label(frame_1, bg='grey', text="Tuning", font=("Arial Bold", 40))
Tuning.grid(row=0, column=0)

Conf_Thresh = Label(frame_1, bg='grey', text="Confidence Threshold:", font=("Arial Bold", 12))
Conf_Thresh.grid(row=1, column=0)
NMS_Thresh = Label(frame_1, bg='grey', text="NMS Threshold:", font=("Arial Bold", 12))
NMS_Thresh.grid(row=3, column=0)

spinbox_1 = Spinbox(frame_1, width=120, height=40, step_size=1)
spinbox_1.set(50)
spinbox_1.grid(row=2, column=0, pady=5)

spinbox_2 = Spinbox(frame_1, width=120, height=40, step_size=1)
spinbox_2.set(50)
spinbox_2.grid(row=4, column=0, pady=5)

# Now we'll fill another frame to the right 'Model'
Model = Label(frame_2, bg='grey', text="Model", font=("Arial Bold", 40))
Model.grid(row=0, column=0)

res_label = Label(frame_2, bg='grey', text="Resolution", font=("Arial Bold", 18))
res_label.grid(row=3, column=0, pady=10)

res_frame = Frame(frame_2, bg='grey')
res_frame.grid(row=4, column=0, sticky="nsew")

res_width = Label(res_frame, bg='grey', text="Width", font=("Arial Bold", 12))
res_width.grid(row=0, column=0)

spinbox_resw = Spinbox(res_frame, width=150, height=40, step_size=1)
spinbox_resw.set(889)
spinbox_resw.grid(row=1, column=0)

res_height = Label(res_frame, bg='grey', text="Height", font=("Arial Bold", 12))
res_height.grid(row=2, column=0)

spinbox_resh = Spinbox(res_frame, width=150, height=40, step_size=1)
spinbox_resh.set(500)
spinbox_resh.grid(row=3, column=0)

# Now fill another frame to the right of 'Model' with the camera output
cam = Label(camframe)
cam.grid(row=0, column=0)
calc_disp = Label(camframe, bg='grey', text="Output Information: (x, y, area)", font=("Arial Bold", 12))
calc_disp.grid(row=1, column=0, pady=10)

# Create Dropdowns
def filter_option_selected(selected_option):
    """Output to the terminal when the filter dropdown is changed"""
    print("Filter Mode: ", selected_option)

filter_type = Label(frame_1, bg='grey', text="Filter mode: ", font=("Arial Bold", 12))
filter_type.grid(row=5, column=0, pady=10)
selected_option = tkinter.StringVar(mainwin)
selected_option.set("Closest")  # Set default option
Filter_Options = ["Closest", "Highest Confidence"]
Filter = OptionMenu(frame_1, selected_option, *Filter_Options, command=filter_option_selected)
Filter.grid(row=6, column=0, pady=10)

def model_option_selected(selected_option):
    """Output to the terminal when the model dropdown is changed"""
    print("Model: ", selected_option)

model_type = Label(frame_2, bg='grey', text="Model: ", font=("Arial Bold", 12))
model_type.grid(row=1, column=0)
selected_option = tkinter.StringVar(mainwin)
selected_option.set("1")  # Set default option
Model_Options = ["1", "2", "3", "4"]
Model = OptionMenu(frame_2, selected_option, *Model_Options, command=model_option_selected)
Model.grid(row=2, column=0)

# Store video to a variable in preparation for conversion
cap = cv2.VideoCapture(0)

# Define function to show frame
def show_frames():
    # Get the latest frame and convert into Image
    cv2image = cv2.cvtColor(cap.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2.flip(cv2image, 1))
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    cam.imgtk = imgtk
    cam.configure(image=imgtk)
    # Repeat after an interval to capture continuously
    cam.after(1, show_frames)

show_frames()

def resize(event):
    # Adjust the size of the frames to fit the window
    mainwin.grid_columnconfigure(0, weight=1)
    mainwin.grid_columnconfigure(1, weight=1)
    mainwin.grid_columnconfigure(2, weight=1)

    mainwin.grid_rowconfigure(0, weight=1)

mainwin.bind("<Configure>", resize)

mainwin.mainloop()