import tkinter
from tkinter import *
import functions as f
from PIL import Image, ImageTk
import os

root = Tk()
root.geometry('800x500')
root.title("Lost Sales Model")

logo = Image.open('pepco-logo2.jpg')
logo = ImageTk.PhotoImage(logo)
logo_label = Label(image=logo)
logo_label.image = logo
logo_label.place(relx=0.5, rely=0.1, anchor='center')

#TITLE##############
label_0 = Label(root, text="Lost Sales", width=20, font=("bold", 20))
label_0.place(relx=0.5, rely=0.3, anchor='center') # label_0.place(x=120,y=53)

#LABEL 1############
label_1 = Label(root, text="Folder path", width=20, anchor='e', font=("bold", 10))
label_1.place(x=65,y=180)
entry_1 = Entry(root, width=60)
entry_1.place(x=240, y=180)

#LABEL 2############
label_2 = Label(root, text="Database file name", width=20, anchor='e', font=("bold", 10))
label_2.place(x=65,y=230)
entry_2 = Entry(root, width=60)
entry_2.place(x=240, y=230)

#LABEL 4############
label_4 = Label(root, text="Database dates", width=20, anchor='e', font=("bold", 10))
label_4.place(x=65, y=280)
entry_4 = Entry(root, textvariable='Yes', width=60, fg='grey')
entry_4.place(x=240, y=280)

#LABEL 3############
label_3 = Label(root, text="Download db", width=20, anchor='e', font=("bold", 10))
label_3.place(x=65,y=330)
var = IntVar()
Radiobutton(root, text="Yes", padx = 5, variable=var, value=1, command=lambda:f.setTextInput("Please type here a date you choose. (Eg.: 'Y2021W01', 'Y2021W04')",entry_4)).place(x=235, y=330)
Radiobutton(root, text="No", padx = 20, variable=var, value=2, command=lambda:f.setTextInput("No need a date", entry_4)).place(x=290, y=330)

#Information Field##
infoField = Text(root, bg='light grey', width=50, height=6, font=("Helvetica", 10))  # , padx=8, pady=8
infoField.place(relx=0.4, rely=0.75)
infoField.insert(1.0, "Hello in the Lost Sales Model\n\nPlease fill in the above fields")
infoField.tag_configure("tag_name", justify="center")
infoField.tag_add("tag_name", 1.0, "end")

# Create Buttons
check_button = Button(root, text="Check Path", width=20, bg='light grey', fg='black', command=lambda:f.check_path(root, entry_1.get(), entry_2.get())) # command=query
check_button.place(relx=0.25, rely=0.78, anchor='center')

submit_btn = Button(root, text='Submit', width=20, bg='brown', fg='white', command=lambda:f.calculation(f.check_path(root, entry_1.get(), entry_2.get())))
submit_btn.place(relx=0.25, rely=0.92, anchor='center') # x=180,y=380

help_btn = Button(root, text="Instruction", width=20, bg='light grey', fg='black', command=lambda:[f.display_text(root, f.model_description)]) # command=query
help_btn.place(relx=0.25, rely=0.85, anchor='center')


root.mainloop()