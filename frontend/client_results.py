# import tkinter and all its functions
from tkinter import *
from backend.interview_semantic import positive_negative
from PIL import ImageTk, Image

root = Tk() # create root window
root.title("Find your next challenge") # title of the GUI window
root.geometry("1000x600") #Width x Height
root.config(bg="#92a8d1") # specify background color

# Create left and right frames
left_frame = Frame(root, width=1900, height=600, bg='#99CCCC')
left_frame.grid(row=0, column=0, padx=17, pady=5)
middle_frame = Frame(root, width=200, height=200, bg='grey')
middle_frame.grid(row=0, column=1, padx=10, pady=5)
right_frame = Frame(root, width=1000, height=1000, bg='grey')
right_frame.grid(row=0, column=2, padx=10, pady=5)
image_path= positive_negative.get_output()

Label(right_frame, text="bbb Image").grid(row=1, column=1, padx=5, pady=5)

# Create frames and labels in left_frame
Label(left_frame, text="Original Image").grid(row=0, column=0, padx=5, pady=5)

# load image to be "edited"
image=Image.open(image_path)
image = image.resize((200, 200), Image.ANTIALIAS)
img = ImageTk.PhotoImage(image)
Label(left_frame, image=img).grid(row=1, column=0, padx=5, pady=5)

# Display image in right_frame
Label(right_frame, image=img).grid(row=0,column=1, padx=5, pady=5)

# Create tool bar frame
tool_bar = Frame(left_frame, width=180, height=185)
tool_bar.grid(row=2, column=0, padx=5, pady=5)

# Example labels that serve as placeholders for other widgets
Label(tool_bar, text="Tools", relief=RAISED).grid(row=0, column=0, padx=5, pady=3, ipadx=10) # ipadx is padding inside the Label widget
Label(tool_bar, text="Filters", relief=RAISED).grid(row=0, column=1, padx=5, pady=3, ipadx=10)

# Example labels that could be displayed under the "Tool" menu
Label(tool_bar, text="Select").grid(row=1, column=0, padx=5, pady=5)
Label(tool_bar, text="Crop").grid(row=2, column=0, padx=5, pady=5)
Label(tool_bar, text="Rotate & Flip").grid(row=3, column=0, padx=5, pady=5)
Label(tool_bar, text="Resize").grid(row=4, column=0, padx=5, pady=5)
Label(tool_bar, text="Exposure").grid(row=5, column=0, padx=5, pady=5)

root.mainloop()