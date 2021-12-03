import tkinter
from tkinter import *
import functions as f
from PIL import Image, ImageTk

import daxDownloader as dd
import daxQueries as dq

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
label_title = Label(root, text="Lost Sales", width=20, font=("bold", 20))
label_title.place(relx=0.5, rely=0.3, anchor='center') # label_0.place(x=120,y=53)

#LABEL 1############
label_download = Label(root, text="Download db", width=20, anchor='e', font=("bold", 10)) # 180
label_download.place(x=65, y=180)
var = IntVar()
Radiobutton(root, text="Yes", padx = 5, variable=var, value=1, command=lambda:f.setTextInput(entry_dates, entry_fileName, infoField, 1)).place(x=235, y=180)
Radiobutton(root, text="No", padx = 20, variable=var, value=2, command=lambda:f.setTextInput(entry_dates, entry_fileName, infoField, 2)).place(x=290, y=180)

#LABEL 2############
label_path = Label(root, text="Folder path", width=20, anchor='e', font=("bold", 10)) #230
label_path.place(x=65, y=230)
entry_path = Entry(root, width=60)
entry_path.place(x=240, y=230)

#LABEL 2############
label_fileName = Label(root, text="Database file name", width=20, anchor='e', font=("bold", 10)) #280
label_fileName.place(x=65, y=280)
entry_fileName = Entry(root, width=60)
entry_fileName.place(x=240, y=280)

#LABEL 4############
label_dates = Label(root, text="Database dates", width=20, anchor='e', font=("bold", 10)) # 330
label_dates.place(x=65, y=330)
entry_dates = Entry(root, textvariable='Yes', width=60, fg='grey')
entry_dates.place(x=240, y=330)

#Information Field##
infoField = Text(root, bg='light grey', width=50, height=6, font=("Helvetica", 10))  # , padx=8, pady=8
infoField.place(relx=0.4, rely=0.75)
infoField.insert(1.0, "Hello in the Lost Sales Model\n\nPlease fill in the above fields")
infoField.tag_configure("tag_name", justify="center")
infoField.tag_add("tag_name", 1.0, "end")

# Create Buttons
check_button = Button(root, text="Check Path", width=20, bg='light grey', fg='black', command=lambda:f.check_path(root, entry_path.get(), entry_fileName.get())) # command=query
check_button.place(relx=0.25, rely=0.78, anchor='center')

submit_btn = Button(root, text='Submit', width=20, bg='brown', fg='white', command=lambda:f.calculation(entry_path.get(), entry_fileName.get(), entry_dates.get(), var.get()))
submit_btn.place(relx=0.25, rely=0.92, anchor='center') # x=180,y=380

help_btn = Button(root, text="Instruction", width=20, bg='light grey', fg='black', command=lambda:[f.display_text(root, f.model_description)]) # command=query
help_btn.place(relx=0.25, rely=0.85, anchor='center')

temp_btn = Button(root, text="Temporary", width=20, bg='light grey', fg='black', command=lambda:[dd.dataFrameFromTabular(dq.stockAndSales('202109'))]) # command=query Y2021W01
temp_btn.place(relx=0.25, rely=0.98, anchor='center')



root.mainloop()