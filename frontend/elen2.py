
import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
from backend.interview_semantic import positive_negative
from backend.interview_topic_modeling import LDA

BACKGROUND_COLOR= "#92a8d1"




class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.id_var=""
        self.screen_id= "StartPage"
        self.switch_frame(StartPage, self.screen_id ,self.id_var)

    def switch_frame(self, frame_class, screen_id, id_var):
        if screen_id=="StartPage":
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()

        elif screen_id=="PageOne":
            new_frame = frame_class(self , id_var)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("Find your next challenge")  # title of the GUI window
        master.geometry("750x340")  # Width x Height
        master.configure(bg="#92a8d1")  # specify background color
        tk.Label(master, text="Find your next challenge")

        self.inner_frame = tk.Frame(self)
        self.inner_frame.configure(bg=BACKGROUND_COLOR)
        # self.id_var = tk.StringVar(self)
        self.company_name = tk.StringVar(self)
        self.company_name.set("choose ...")

        tk.Label(self.inner_frame,bg="#92a8d1", font=('Helvetica', 20, "bold")).grid(row=1, column=1)
        tk.Label(self.inner_frame, text="JobMe",bg="#92a8d1", font=('Helvetica', 20, "bold")).grid(row=2, column=0)
        tk.Label(self.inner_frame,bg="#92a8d1", font=('Helvetica', 20, "bold")).grid(row=3, column=1)

        tk.Label(self.inner_frame, text="company name", font=("David", 16), bg=BACKGROUND_COLOR).grid(row=4, column=0)
        tk.OptionMenu(self.inner_frame, self.company_name, "google", "apple", "microsoft").grid(row=4, column=1, padx=10,
                                                                                          pady=10)
        # tk.Entry(self.inner_frame, width="60", textvariable=self.id_var).pack()
        tk.Button(self.inner_frame, text="help me to find my new challenge !" ,
                  command=lambda: master.switch_frame(PageOne, "PageOne", self.company_name.get())).grid(row=5, column=1)

        self.inner_frame.pack(anchor="s", side="top")


class PageOne(tk.Frame):
    def __init__(self, master, id_var):
        tk.Frame.__init__(self, master)

        if str(id_var).lower()=='choose ...':
            tk.tkMessageBox.showinfo("Title", "a Tk MessageBox")

        else:
            self.config(bg=BACKGROUND_COLOR)
            tk.Button(self, text="Go back to start page",
                      command=lambda: master.switch_frame(StartPage,"StartPage", "")).pack(side="top", fill="both" )

            self.left_inner_frame = tk.Frame(self)
            self.left_inner_frame.configure(bg=BACKGROUND_COLOR)
            self.id_var = tk.StringVar(self)
            tk.Label(self.left_inner_frame, bg=BACKGROUND_COLOR, text=id_var, font=('Helvetica', 40, "bold")).pack()

            self.image_company_path= "../frontend/resurces/" + str(id_var).lower() + ".jpg"
            self.image=Image.open(self.image_company_path)
            self.image = self.image.resize((200, 200 ), Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.image)
            tk.Label(self.left_inner_frame, image=self.img).pack()

            self.left_inner_frame.pack(side="left")
            self.middle_inner_frame = tk.Frame(self)
            self.middle_inner_frame.configure(bg=BACKGROUND_COLOR)

            # Create tool bar frame
            self.tool_bar = tk.Frame(self.middle_inner_frame, bg=BACKGROUND_COLOR, width=300, height=185)
            self.tool_bar.pack()

            # Example labels that serve as placeholders for other widgets
            tk.Label(self.tool_bar, text="most relevant Topics:", font=('Helvetica', 15, "bold"), bg=BACKGROUND_COLOR).pack(pady=30)

            # Example labels that could be displayed under the "Tool" menu
            relevants_topics= LDA.get_words();
            for idx, val in enumerate(relevants_topics):
                tk.Label(self.tool_bar,bg=BACKGROUND_COLOR, text=val).pack()

            self.right_inner_frame = tk.Frame(self)
            self.right_inner_frame.configure(bg=BACKGROUND_COLOR)

            self.image_pos_neg_path= positive_negative.get_output(id_var)
            self.image_pos_neg = Image.open(self.image_pos_neg_path)
            self.image_pos_neg = self.image_pos_neg.resize((260, 260), Image.ANTIALIAS)
            self.img_pos_neg = ImageTk.PhotoImage(self.image_pos_neg)
            tk.Label(self.right_inner_frame, bg=BACKGROUND_COLOR, text="General feeling from the interviews:", font=('Helvetica', 10,"bold")).pack(side="top")
            tk.Label(self.right_inner_frame, image=self.img_pos_neg).pack(side="top")


            self.right_inner_frame.pack(side="right", fill="both")
            self.middle_inner_frame.pack(side="right", fill="both")



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()