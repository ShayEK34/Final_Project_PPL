
import tkinter as tk
import tkinter.messagebox
from PIL import ImageTk, Image
from backend.interview_sentiment import positive_negative
from backend.interview_topic_modeling import LDA as model_LDA

BACKGROUND_COLOR= "#92a8d1"

class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.details=[]
        self.screen_id= "StartPage"
        self.switch_frame(StartPage, self.screen_id ,self.details)

    def switch_frame(self, frame_class, screen_id, details):
        if screen_id=="StartPage":
            new_frame = frame_class(self)
            if self._frame is not None:
                self._frame.destroy()
            self._frame = new_frame
            self._frame.pack()

        elif screen_id=="PageOne":
            if( details['company_name'].get()=="choose ..." or  details['job_title'].get()=="choose ..." or details['location'].get()=="choose ..."):
                tk.messagebox.showinfo("warning", "you must fill all entries fields")
                self.switch_frame(StartPage, "StartPage" ,"")
            else:
                new_frame = frame_class(self , details)
                if self._frame is not None:
                    self._frame.destroy()
                self._frame = new_frame
                self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.configure(bg="#92a8d1")  # specify background color

        fname = "office.jpg"
        self.image = Image.open(fname)
        self.image = self.image.resize((750, 340), Image.ANTIALIAS)
        self.bg_image = ImageTk.PhotoImage(self.image)
        self.w = self.bg_image.width()
        self.h = self.bg_image.height()
        master.geometry('750x340')

        self.cv = tk.Canvas(self, width=self.w, height=self.h)
        self.cv.pack(side='top', fill='both', expand='yes')

        self.cv.create_image(0, 0, image=self.bg_image, anchor='nw')
        tk.Label(self.cv, text="JobMe", bg="#92a8d1", font=('Helvetica', 20, "bold")).pack(pady=(50,0))


        self.details={}

        self.details['company_name'] = tk.StringVar(self)
        self.details['company_name'] .set("choose ...")

        self.details['location'] = tk.StringVar(self)
        self.details['location'].set("choose ...")

        self.details['job_title'] = tk.StringVar(self)
        self.details['job_title'].set("choose ...")

        up_frame = tk.Frame(self.cv)
        up_frame.pack(side="top", pady=(75, 0))
        tk.Label(up_frame, text="Company name", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
        tk.OptionMenu(up_frame, self.details['company_name'], "google", "apple", "microsoft").pack(side="left")

        first_middle_frame = tk.Frame(self.cv)
        first_middle_frame.pack(side="top", pady=(10, 0))
        tk.Label(first_middle_frame, text="Location", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
        tk.OptionMenu(first_middle_frame, self.details['location'], "Tel aviv").pack(side="left")

        second_middle_frame = tk.Frame(self.cv)
        second_middle_frame.pack(side="top", pady=(10, 0))
        tk.Label(second_middle_frame, text="Job title", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")
        tk.OptionMenu(second_middle_frame, self.details['job_title'], "software engineer").pack(side="left")

        down_frame = tk.Frame(self.cv)
        down_frame.pack(side="top", pady=(26, 0))
        tk.Button(down_frame, text="help me to find my new challenge !", font=("Helvetica", 10),
                  command=lambda: master.switch_frame(detailsPage, "PageOne", self.details)).pack()

        most_down = tk.Frame(self.cv)
        most_down.pack(side="top", padx=(380, 380))
        tk.Label(most_down, text="good lack", font=("Helvetica", 14), bg=BACKGROUND_COLOR).pack(side="left")



class detailsPage(tk.Frame):
    def __init__(self, master, details):
        tk.Frame.__init__(self, master)
        self.config(bg=BACKGROUND_COLOR)
        tk.Button(self, text="Go back to start page",
                  command=lambda: master.switch_frame(StartPage,"StartPage", "")).pack(side="top", fill="both" )

        self.left_inner_frame = tk.Frame(self)
        self.left_inner_frame.configure(bg=BACKGROUND_COLOR)
        self.id_var = tk.StringVar(self)
        tk.Label(self.left_inner_frame, bg=BACKGROUND_COLOR, text=details['company_name'].get(), font=('Helvetica', 30, "bold")).pack(pady=15)

        self.image_company_path= "../frontend/resurces/" + str(details['company_name'].get()).lower() + ".jpg"
        self.image=Image.open(self.image_company_path)
        self.image = self.image.resize((150, 150 ), Image.ANTIALIAS)
        self.img = ImageTk.PhotoImage(self.image)
        tk.Label(self.left_inner_frame, image=self.img).pack(padx=(13,0))

        self.left_inner_frame.pack(side="left")
        self.middle_inner_frame = tk.Frame(self)
        self.middle_inner_frame.configure(bg=BACKGROUND_COLOR)

        # Create tool bar frame
        self.tool_bar = tk.Frame(self.middle_inner_frame, bg=BACKGROUND_COLOR, width=300, height=185)
        self.tool_bar.pack(padx=24)

        # Example labels that serve as placeholders for other widgets
        tk.Label(self.tool_bar, text="most relevant Topics:", font=('Helvetica', 13, "bold"), bg=BACKGROUND_COLOR).pack(pady=(30,5))

        # Example labels that could be displayed under the "Tool" menu
        self.lda= model_LDA.LDA()
        path=''
        if(str(details['company_name'].get()).lower()=='google'):
            path= r'../backend/scrape_interviews/scraper_output/Google_softwareJobs_interviews.csv'
        elif (str(details['company_name'].get()).lower()=='apple'):
            path = r'../backend/scrape_interviews/scraper_output/apple_softwareJobs_interviews.csv'
        else:
            path = r'../backend/scrape_interviews/scraper_output/Microsoft_softwareJobs_interviews.csv'

        relevants_topics= self.lda.get_words(path)
        for idx, val in enumerate(relevants_topics):
            tk.Label(self.tool_bar,bg=BACKGROUND_COLOR, text=val).pack()

        self.right_inner_frame = tk.Frame(self)
        self.right_inner_frame.configure(bg=BACKGROUND_COLOR)

        sentiment= positive_negative.Sentiment()
        self.image_pos_neg_path= sentiment.get_output(details['company_name'].get())
        self.image_pos_neg = Image.open(self.image_pos_neg_path)
        self.image_pos_neg = self.image_pos_neg.resize((220, 220), Image.ANTIALIAS)
        self.img_pos_neg = ImageTk.PhotoImage(self.image_pos_neg)
        tk.Label(self.right_inner_frame, bg=BACKGROUND_COLOR).pack(side="top")
        tk.Label(self.right_inner_frame, bg=BACKGROUND_COLOR, text="General feeling from interviews:", font=('Helvetica', 13,  "bold")).pack(side="top")
        tk.Label(self.right_inner_frame, image=self.img_pos_neg).pack(side="top")


        self.right_inner_frame.pack(side="right", fill="both")
        self.middle_inner_frame.pack(side="right", fill="both")



if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()