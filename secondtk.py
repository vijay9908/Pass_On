import tkinter as tk
from PIL import Image, ImageTk
import os
import sys

root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=300)
canvas.grid(columnspan=3, rowspan=3)

#logo
logo = Image.open('passon_logo.png')
logo = logo.resize((145, 135), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(column=1, row=0)

#instructions
instructions = tk.Label(root, text="A Socket progamming based file share application", font="Raleway")
instructions.grid(columnspan=3, column=0, row=1)

#browse button
def send_btn_clicked():
    os.system("/Users/vijay/Documents/Academics/S6/Networks/Pass_On/sender.py")
send_text = tk.StringVar()
send_btn = tk.Button(root, textvariable=send_text, font="Raleway", bg="White", fg="Black", height=2, width=15,command=send_btn_clicked)
send_text.set("Send")
send_btn.grid(column=1, row=2)

receive_text = tk.StringVar()
receive_btn = tk.Button(root, textvariable=receive_text, font="Raleway", background="White", fg="Black", height=2, width=15)
receive_text.set("Receive")
receive_btn.grid(column=1, row=3)

canvas = tk.Canvas(root, width=500, height=100)
canvas.grid(columnspan=3)

root.mainloop()