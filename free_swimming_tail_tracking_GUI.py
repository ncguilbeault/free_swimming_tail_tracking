import tkinter as tk
import tkinter.filedialog as tkfd
import free_swimming_tail_tracking as tr

class MainWindow:

    def __init__(self, master):
        self.master = master
        self.initUI()
        # self.button = self.add_button()

    def initUI(self):
        self.master.state('zoomed')
        self.master.title('Free Swimming Tail Tracking GUI')
        self.open_video_file_button = tk.Button(self.master, text="Open Video File", command=self.open_video_file)
        # self.open_video_file_button.pack()
        self.create_layout()

    def open_video_file(self):
        self.video_filename = tkfd.askopenfilename()
        self.print_video_filename()

    def print_video_filename(self):
        print("Video file selected: {0}".format(self.video_filename))

    def create_layout(self):
        self.open_video_file_button.grid(row=0, column=0)
        # self.layout = tkinter.Canvas(self.master)
        # self.canvas.grid(column=0, row=0)
        # self.populate_canvas()

    # def populate_canvas(self):
        # self.greet_button.grid(column=0, row=0)

if __name__ == '__main__':
    root = tk.Tk()
    gui = MainWindow(root)
    root.mainloop()
