from tkinter import *
from PIL import ImageTk, Image
from os import walk


def next_img(img_num):
    global label
    global btn_back
    global btn_next

    label.grid_forget()
    label = Label(image=)


def back_img(img_num):
    global label
    global btn_back
    global btn_next


root = Tk()
root.title("Image")
root.iconbitmap(
    "C:/Users/athiruj/Desktop/img-processing/Python_GUI/img/pc.ico")
img_list = []
imgs = []
path = "C:/Users/athiruj/Desktop/img-processing/Python_GUI/img/"
for (dirpath, dirnames, filenames) in walk(path):
    img_list.extend(filenames)
for img in img_list:
    temp = ImageTk.PhotoImage(Image.open(path+img))
    imgs.append(temp)


img = ImageTk.PhotoImage(Image.open(path+img_list[0]))

label = Label(image=img)
label.grid(row=0, column=0, columnspan=3)

btn_back = Button(root, text="<<", command=lambda: back_img())
btn_exit = Button(root, text="Exit", command=root.quit)
btn_next = Button(root, text=">>", command=lambda: next_img(2))

btn_back.grid(row=1, column=0)
btn_exit.grid(row=1, column=1)
btn_next.grid(row=1, column=2)


root.mainloop()
