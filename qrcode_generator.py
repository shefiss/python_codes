import os
from tkinter import *
from tkinter import simpledialog
from tkinter.filedialog import askdirectory
import qrcode
from PIL import Image, ImageTk


def submit(event):
    data=data_var.get()
    
    #qr code generator
    img = qrcode.make(data)
    img.save("img.png")

    #qr code image load
    img = Image.open("img.png")
    img = ImageTk.PhotoImage(img)
    img_label.config(image=img)
    img_label.pack()
    os.remove("img.png")
    root.mainloop()
    
    
#method for saving files
def save(event):
    savename = simpledialog.askstring(title="QR code", prompt="Name the file:")
    savefile = askdirectory()
    
    data=data_var.get()
    img = qrcode.make(data)
    try:
        print(savefile + "/" + savename + ".png")
        img.save(savefile + "/" + savename + ".png", format="PNG", quality=90)
        
    except:
        pass
    
#window inicialization
root = Tk()
root.resizable(False,False)
root.title("QR code generator")

data_var = StringVar()

img_label = Label(root)
data_label = Label(root, text="Data: ", font=("Arial", 12))
data_entry = Entry(root, textvariable=data_var, font=("Arial", 12))
btn_sub = Button(root, text="Submit")
btn_sub.bind("<Button-1>", submit)
btn_save = Button(root, text="Save")
btn_save.bind("<Button-1>", save)

#default image load (but you have to have the default img)
try:
    data=data_var.get()
    img = Image.open("qr-code.png")
    img = ImageTk.PhotoImage(img)
    img_label = Label(root, image=img)

except:
    pass

data_label.pack()
data_entry.pack(fill=X)
btn_sub.pack()
btn_save.pack()
img_label.pack()

root.mainloop()


