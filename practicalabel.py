from tkinter import *

root=Tk()

miFrame=Frame(root, width=500, height=400)

miFrame.pack()

miImage=PhotoImage(file="coca-cola.png")

Label(miFrame, text= "Hola alumnos de python", fg="red", font=("Comic Sans MS", 18)).place(x=100, y=200)

Label(miFrame, image= miImage).place(x=100, y=20)

root.mainloop()