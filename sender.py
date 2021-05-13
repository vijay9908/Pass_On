import tkinter as tk
import time
import datetime
import sys,os,tqdm
from tkinter import messagebox
from time import ctime
from socket import *
import _thread
from PIL import Image, ImageTk
from tkinter import filedialog


Format = "utf-8"

def my_server(show_1,HOST,PORT):
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
    currentDT = datetime.datetime.now()

    while True:
        show_1.insert(tk.END,"waiting for connection...")
        show_1.insert(tk.END,"\n")

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        show_1.insert(tk.END,"connected {}".format(addr))
        show_1.insert(tk.END,"\n")

        file = filedialog.askopenfilename(initialdir="/", title="Select the file to Transfer", filetypes = (("png files", "*.png"),("jpg files", "*.jpg"),("txt files", "*.txt")))
        #file_size = os.path.getsize(file)
        #progress = tqdm.tqdm(range(file_size),"Sending the file", unit="B", unit_scale=True, unit_divisor=1024)
        f = open(file,'rb')
        l = f.read(1024)

        while (l):
            tcpTimeClientSock.send(l)
            print('Sent ',repr(l))
            #progress.update(len(l))
            l = f.read(1024)

        f.close()
        print('Done sending')
        tcpTimeClientSock.close()

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (ServerLogin, SendPage):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(ServerLogin)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class ServerLogin(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        #instructions = tk.Label(self, text="A Socket progamming based file share application", font="Raleway")
        #instructions.grid(columnspan=50, column=0, row=1)
        logo = Image.open('passon_logo.png')
        logo=logo.resize((100, 71), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        l_logo=tk.Label(self, image=logo)
        l_logo.image = logo
        l_logo.grid(row=0,column=1,columnspan=3, sticky="NSEW",padx=10,pady=20)

        l_title=tk.Label(self, text="Sender Software",font=('Georgia', 13),bg="#ed1135",fg='white')
        l_title.grid(row=1,column=1,columnspan=3, sticky="NSEW",padx=10,pady=20)

        label_username = tk.Label(self, text="Username")
        label_password = tk.Label(self, text="Password")

        entry_username = tk.Entry(self,show="*")
        entry_password = tk.Entry(self, show="*")

        label_username.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=4, column=0, sticky='NSEW',padx=10,pady=10)
        entry_username.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)
        entry_password.grid(row=4, column=1,sticky='NSEW',padx=10,pady=10)

        checkbox = tk.Checkbutton(self, text="Keep me logged in")
        checkbox.grid(row=5, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", background="white", foreground="Black",command=lambda: login_btn_clicked())
        logbtn.grid(row=6, column=1,sticky='NSEW', padx=10, pady=10)

        def login_btn_clicked():
            # print("Clicked")
            username = entry_username.get()
            password = entry_password.get()

            if len(username) and len(password) > 2:
                # print(username, password)

                if username == "admin" and password == "1234":
                    controller.show_frame(SendPage)
                # display a message if username and password is incorrect!
                else:
                    messagebox.showinfo(self,"Incorrect credentials! ")

            else:
                messagebox.showinfo(self,"Enter Login Details")


class SendPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        flag = True

        logo = Image.open('passon_logo.png')
        logo=logo.resize((100, 71), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        l_logo=tk.Label(self, image=logo)
        l_logo.image = logo
        l_logo.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=10,pady=20)

        clock = tk.Label(self, font=('times', 18, 'bold'), bg='black',fg="white")
        clock.grid(row=1,column=2, sticky="NSNESWSE",padx=6,pady=6)

        def timenow():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,timenow)
        timenow()

        label = tk.Label(self, text="Sender Software ", font=('Georgia', 14),bg="#ed1135",fg="white")
        label.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Enter Host")
        l_host.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_host=tk.Entry(self)
        e_host.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,'127.0.0.1')


        l_port=tk.Label(self,text="Enter Port")
        l_port.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,1700)

        message_label=tk.Label(self,text="Receiver Message",font=("Georgia,12"))
        message_label.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=5, column=3,rowspan=6)

        show_1=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        show_1.grid(row=6, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        b_connect=tk.Button(self,text=" Connect",command=lambda: connect())
        b_connect.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")

        b_disconnect=tk.Button(self,text=" disconnect",command=lambda: disconnec())
        b_disconnect.grid(row=14,column=1,padx=10,pady=10,sticky="nsew")


        def runner():
            global after_id
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                e_host_v=e_host.get()
                e_port_v=int(e_port.get())

        def connect():
            e_host_v= "0.0.0.0"  #e_host.get()
            e_port_v=int(e_port.get())
            _thread.start_new_thread(my_server,(show_1,e_host_v,e_port_v))
            global secs
            secs = 0
        
        def disconnec():
            global after_id
            print("Disconnected ")
            ''' if after_id:
                self.after_cancel(after_id)
                after_id = None '''
            sys.exit(0)

app = Page()
app.mainloop()