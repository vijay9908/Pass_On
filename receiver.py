import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import time
import datetime
import socket
import time, tqdm
from time import ctime
import sys
import os
from tkinter import PhotoImage,BitmapImage

Format = "utf-8"

class Page(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        #this is container
        box = tk.Frame(self)

        box.pack(side="top", fill="both", expand = True)

        box.grid_rowconfigure(0, weight=1)
        box.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (clientloginPage, ReceivePage):

            frame = F(box, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(clientloginPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class clientloginPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        logo = Image.open('passon_logo.png')
        logo=logo.resize((100, 71), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)

        l_logo=tk.Label(self, image=logo)
        l_logo.image = logo
        l_logo.grid(row=0,column=1,columnspan=3, sticky="NSEW",padx=10,pady=20)

        l_title=tk.Label(self, text="Receiver Software",font=('Georgia',13),bg="#20bebe")
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
            username = entry_username.get()
            password = entry_password.get()

            if len(username) and len(password) > 2:
                if username == "admin" and password == "1234":
                    controller.show_frame(ReceivePage)
                else:
                    messagebox.showinfo(self,"Incorrect credentials! ")

            else:
                messagebox.showinfo(self,"Enter Login Details")

class ReceivePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        logo = Image.open('passon_logo.png')
        logo=logo.resize((100, 71), Image.ANTIALIAS)
        logo = ImageTk.PhotoImage(logo)
        
        #l_logo.grid(column=0, row=0, columnspan=3)
        l_title=tk.Label(self, image=logo)
        l_title.image = logo
        l_title.grid(row=0,column=0,columnspan=3, sticky="NSEW",padx=10,pady=20)

        clock = tk.Label(self, font=('times', 15, 'bold'), bg='black',fg="white")
        clock.grid(row=1,column=2,padx=6,pady=6) #sticky="NSNESWSE"

        def timenow():
            time2=time.strftime('%H:%M:%S')
            clock.config(text=time2)
            clock.after(200,timenow)
        timenow()

        label = tk.Label(self, text="Receiver Software ", font=('Georgia', 13) ,bg="#20bebe",fg="black")
        label.grid(row=1, column=0, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")

        l_host=tk.Label(self,text="Enter Host Name")
        l_host.grid(row=2, column=0, padx=8, pady=8, sticky="NSNESWSE")


        e_host=tk.Entry(self)
        e_host.grid(row=2, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_host.insert(tk.END,'127.0.0.1')


        l_port=tk.Label(self,text="Enter Port")
        l_port.grid(row=3, column=0, padx=8, pady=8, sticky="NSNESWSE")

        e_port=tk.Entry(self)
        e_port.grid(row=3, column=1, columnspan=2, padx=8, pady=8, sticky="NSNESWSE")
        e_port.insert(tk.END,1700)

        message_label=tk.Label(self,text="Sender Message",font=("Georgia,12"))
        message_label.grid(row=4,column=0,columnspan=3,padx=10,pady=10,sticky="NSEW")


        scrollbar_y = tk.Scrollbar(self)
        scrollbar_y.grid(row=5, column=3,rowspan=6)

        show_1=tk.Text(self,height=8, width=35, yscrollcommand=scrollbar_y.set,
                       bg="Grey",fg="White")
        show_1.grid(row=5, column=0,rowspan=3,columnspan=3,sticky="NSEW")

        accept_button=tk.Button(self,text="Accept",command=lambda: my_server())
        accept_button.grid(row=14,column=0,padx=10,pady=10,sticky="nsew")

        quit=tk.Button(self,text="Quit",command=lambda: quit())
        quit.grid(row=14,column=3,padx=10,pady=10,sticky="NSEW")

        e_data=tk.Entry(self)
        e_data.grid(row=14,column=1,padx=10,pady=10,sticky="nsew")


        def my_server():
            e_data_v = e_data.get()
            e_host_v = "192.168.0.138"            #e_host.get()
            e_port_v=int(e_port.get())


            HOST, PORT = e_host_v, e_port_v
            data = e_data_v

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.sendall(bytes(data + "\n", "utf-8"))

                #file_size = 0
                #progress = tqdm.tqdm(range(file_size), "Receiving file", unit="B", unit_scale=True, unit_divisor=1024)

                with open('received_file.png','wb') as f:
                    print('file opened')
                    show_1.insert(tk.END,'File Opened !')
                    show_1.insert(tk.END,'\n')

                    while True:
                        data = s.recv(1024)
                        #progress.update(len(data))
                        print('data=%s',(data))
                        show_1.insert(tk.END,'DATA {}'.format(data))
                        if not data:
                            break
                        else:
                            f.write(data)
                f.close()
            s.close()
        
        def quit():
            print("Quitting...")
            sys.exit(0)


app = Page()
app.mainloop()
