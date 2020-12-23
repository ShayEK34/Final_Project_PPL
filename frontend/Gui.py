from tkinter import *
import tkinter as tk
from backend.interview_semantic import positive_negative
from backend.interview_topic_modeling import LDA
from functools import partial
from PIL import ImageTk, Image
import os

def raise_frame(frame):
    if (company_name.get() == "google"):
        print("hi")
    frame.tkraise()

WIDTH=750
HEIGTH=540

root = Tk()
root.title("Find your next challenge") # title of the GUI window
root.geometry("750x540") #Width x Height
root.config(bg="#92a8d1") # specify background color

f1 = Frame(root)
f1.name= "search"
f2 = Frame(root)
f2.name= "results"

company_name = tk.StringVar(root)
location= tk.StringVar(root)
job_title= tk.StringVar(root)

for frame in (f1, f2):
    frame.grid(row=0, column=0, padx=17, pady=15, sticky='news' )

    image = Image.open("office.jpg")
    image=image.resize((750, 540), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    back_ground = Label(frame, image=photo)
    back_ground.image = photo
    back_ground.place(x=0, y=0)

    if(frame.name== "search"):
        for i in range(5):
            Label(back_ground).grid()

        l= Label(back_ground, text="ready for your new challenge?", bg='#99CCCC')
        l.config(font=("Courier", 12))
        l.grid(row=3, column=1)

        for i in range(7):
            Label(back_ground).grid()

        Label(back_ground, text="company name", bg="#92a8d1").grid(row=15, column=0)
        Label(back_ground, text="location", bg="#92a8d1").grid(row=16,column=0)
        Label(back_ground, text="job title", bg="#92a8d1").grid(row=17,column=0)

        e1 = Entry(back_ground,  textvariable = company_name ,width="101").grid(row=15, column=1)
        location = Entry(back_ground,width="101").grid(row=16, column=1)
        job_title = Entry(back_ground,width="101").grid(row=17, column=1)

        for i in range(4):
            Label(back_ground).grid()

        b= Button(back_ground, text='Help me get ready...', command=lambda: raise_frame(f2))
        b.config(font=("Courier", 12))
        b.grid(column=1)
        Label(back_ground).grid()
        Label(back_ground).grid()

    # f2
    else:
        left_frame = Frame(f2, width=1900, height=600, bg='#99CCCC')
        left_frame.grid(row=0, column=0, padx=17, pady=5)
        middle_frame = Frame(f2, width=200, height=200, bg='grey')
        middle_frame.grid(row=0, column=1, padx=10, pady=5)
        right_frame = Frame(f2, width=1000, height=1000, bg='grey')
        right_frame.grid(row=0, column=2, padx=10, pady=5)
        image_path= positive_negative.get_output()

        Label(right_frame, textvariable=company_name).grid(row=1, column=1, padx=5, pady=5)
        but= Button(f2, text='Back', command=lambda:raise_frame(f1))
        but.grid(row=1, column=2, padx=5, pady=3, ipadx=10)

        # Create frames and labels in left_frame
        Label(left_frame, textvariable=company_name , bg="#99CCCC").grid(row=0, column=0, padx=5, pady=5)

        # load image to be "edited"
        image=Image.open(image_path)
        image = image.resize((200, 200), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(image)
        Label(left_frame,image=img).grid(row=1, column=0, padx=5, pady=5)

        # Display image in right_frame
        Label(right_frame, image=img).grid(row=0,column=1, padx=5, pady=5)

        # Create tool bar frame
        tool_bar = Frame(left_frame, width=180, height=185)
        tool_bar.grid(row=2, column=0, padx=5, pady=5)

        # Example labels that serve as placeholders for other widgets
        Label(tool_bar, text="most relevant Topics").grid(row=0, column=0, padx=5, pady=3, ipadx=10) # ipadx is padding inside the Label widget

        # Example labels that could be displayed under the "Tool" menu
        relevants_topics= LDA.get_words();
        for idx, val in enumerate(relevants_topics):
            Label(tool_bar, text=val).grid(row=idx+1, column=0, padx=5, pady=5)

raise_frame(f1)
root.mainloop()