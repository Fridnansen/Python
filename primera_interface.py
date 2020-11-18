from tkinter import *

raiz=Tk()

raiz.title("Ventana de pruebas")

raiz.resizable(True,True)

raiz.iconbitmap("MASTERDREZ.ico")

raiz.geometry("850x650")

raiz.config(bg="BLUE")

raiz.config(bd=35)

raiz.config(relief="sunken")

raiz.config(cursor="hand2")

miFrame=Frame()


#miFrame.pack(side="left", anchor="n")

miFrame.pack(fill="y", expand="True")


miFrame.config(bg="red")

miFrame.config(width="650", height="350")

miFrame.config(bd=35)

miFrame.config(relief="sunken")

miFrame.config(cursor="hand2")

miFrame.config(cursor="pirate")

raiz.mainloop()

