
import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title('background image')
BACKGROUND_COLOR= "#92a8d1"


details={}

details['company_name'] = tk.StringVar()
details['company_name'] .set("choose ...")

details['location'] = tk.StringVar()
details['location'].set("choose ...")

details['job_title'] = tk.StringVar()
details['job_title'].set("choose ...")


fname = "office.jpg"
image= Image.open(fname)
image = image.resize((750, 340), Image.ANTIALIAS)
bg_image = ImageTk.PhotoImage(image)
w = bg_image.width()
h = bg_image.height()
root.geometry("%dx%d+50+30" % (w, h))


cv = tk.Canvas(width=w, height=h)
cv.pack(side='top', fill='both', expand='yes')

cv.create_image(0, 0, image=bg_image, anchor='nw')
cv.create_text(330, 85, text="JobMe",  font=('Helvetica', 20, "bold"),fill="purple", anchor='nw')

# inner_frame = tk.Frame(cv)
# inner_frame.pack(anchor="s", side="top", padx=15, pady=35)
# inner_frame.configure(bg=BACKGROUND_COLOR)

up_frame=  tk.Frame(cv)
up_frame.pack(side="top", pady=(135, 0))
tk.Label(up_frame, text="Company name", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
tk.OptionMenu(up_frame, details['company_name'], "google", "apple", "microsoft").pack(side="left")

first_middle_frame=  tk.Frame(cv)
first_middle_frame.pack(side="top", pady=(10, 0))
tk.Label(first_middle_frame, text="Location", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
tk.OptionMenu(first_middle_frame, details['location'], "Tel aviv").pack(side="left")

second_middle_frame=  tk.Frame(cv)
second_middle_frame.pack(side="top", pady=(10, 0))
tk.Label(second_middle_frame, text="Job title", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
tk.OptionMenu(second_middle_frame, details['company_name'], "software engineer").pack(side="left")

down_frame= tk.Frame(cv)
down_frame.pack(side="top", pady=(26, 0))
tk.Button(down_frame, text="help me to find my new challenge !", font=("Helvetica", 10)).pack()

# now add some button widgets


root.mainloop()