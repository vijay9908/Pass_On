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

def my_server(display_show,HOST,PORT):
    BUFSIZE = 1024
    ADDR = (HOST, PORT)
    tcpTimeSrvrSock = socket(AF_INET,SOCK_STREAM)
    tcpTimeSrvrSock.bind(ADDR)
    tcpTimeSrvrSock.listen(5)
    currentDT = datetime.datetime.now()

    while True:
        display_show.insert(tk.END,"waiting for connection...")
        display_show.insert(tk.END,"\n")

        tcpTimeClientSock, addr = tcpTimeSrvrSock.accept()

        display_show.insert(tk.END,"connected {}".format(addr))
        display_show.insert(tk.END,"\n")

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

        username_in = tk.Entry(self,show="*")
        password_in = tk.Entry(self, show="*")

        label_username.grid(row=3, column=0, sticky='NSEW',padx=10,pady=10)
        label_password.grid(row=4, column=0, sticky='NSEW',padx=10,pady=10)
        username_in.grid(row=3, column=1,sticky='NSEW',padx=10,pady=10)
        password_in.grid(row=4, column=1,sticky='NSEW',padx=10,pady=10)

        checkbox = tk.Checkbutton(self, text="Keep me logged in")
        checkbox.grid(row=5, column=1,sticky='NSEW',padx=10,pady=10)

        logbtn = tk.Button(self, text="Login", background="white", foreground="Black",command=lambda: login_clicked())
        logbtn.grid(row=6, column=1,sticky='NSEW', padx=10, pady=10)

        def login_clicked():
            username = username_in.get()
            password = password_in.get()

            if len(username) and len(password) > 2:
                if username == "admin" and password == "1234":
                    controller.show_frame(SendPage)
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

        def time_stamp():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,time_stamp)
        time_stamp()

        label = tk.Label(self, text="Sender Software ", font=('Georgia', 14),bg="#ed1135",fg="white")
        label.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        Label_host=tk.Label(self,text="Enter Host")
        Label_host.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")

        host_id=tk.Entry(self)
        host_id.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        host_id.insert(tk.END,'127.0.0.1')


        l_port=tk.Label(self,text="Enter Port")
        l_port.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")

        port_no=tk.Entry(self)
        port_no.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        port_no.insert(tk.END,1700)

        message_label=tk.Label(self,text="Receiver Message",font=("Georgia,12"))
        message_label.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")

        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=5, column=3,rowspan=6)

        display_show=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        display_show.grid(row=6, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        b_connect=tk.Button(self,text=" Connect",command=lambda: connect())
        b_connect.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")

        b_disconnect=tk.Button(self,text=" disconnect",command=lambda: disconnect_sys())
        b_disconnect.grid(row=14,column=1,padx=10,pady=10,sticky="nsew")


        def runner():
            global secs
            secs += 1
            if secs % 2 == 0:  # every other second
                v1=host_id.get()
                port_v2=int(port_no.get())

        def connect():
            v1= "0.0.0.0"  #host_id.get()
            port_v2=int(port_no.get())
            _thread.start_new_thread(my_server,(display_show,v1,port_v2))
            global secs
            secs = 0
        
        def disconnect_sys():
            global after_id
            print("Disconnected ")
            sys.exit(0)

app = Page()
app.mainloop()