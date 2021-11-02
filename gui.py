from tkinter import *
import os

# displaying a text in a TextBox
def display_text(content):
    T = Text(root, bg='white', width=30, height=9, font=("Helvetica", 10)) # , padx=8, pady=8
    T.place(relx=0.65, rely=0.6)
    T.insert(1.0, content)
    # T.tag_configure("center", justify="center")
    T.tag_add("center", 1.0, "end")
    return T

def check_path(p):
    folderPath = p

    if not os.path.exists(folderPath):
        display_text("Error! \n\nThe chosen directory does not exist \n\nPlease try type the folder path again")
        folderPath = check_path()

    requiaredFiles = ["StoreCountryGroup.csv", "GradeCutOff.csv", "GradeSellOff.csv", "DS_PARAM.csv"]
    text1 = ""

    for file in requiaredFiles:
        if not(os.path.isfile(folderPath + file)):
            text1 = text1 + file + ', \n'
    if text1 == "":
        display_text("\nEverything looks fine. \n\nYou can click on \n'Submit' button")
    else:
        display_text(f"Missing files: \n\n{text1}")

    return folderPath
# Instruction
model_description = "'Folder path': \nWhere do you keep input files.\n" \
                    "Example: 'c:\Mariusz\MyProjects\LostSales\input files'\n\n" \
                    "'Database file name': \nA name of the database file\n" \
                    "Example: 'StockAndSales_PQ1.zip'\n\n" \
                    "'Download db': \nDo you have a .csv database file or you are going to download a new one?\n\n" \
                    "'check' button: \nThe button is checking whether the chosen path is correct and if it contains all of the necessary files"

root = Tk()
root.geometry('800x500')
root.title("Lost Sales Model")

def setTextInput(text):
    entry_4.delete(0,"end")
    entry_4.insert(0, text)

#TITLE##############
label_0 = Label(root, text="Lost Sales", width=20, font=("bold", 20))
label_0.place(relx=0.5, rely=0.1, anchor='center') # label_0.place(x=120,y=53)

#LABEL 1############
label_1 = Label(root, text="Folder path", width=20, anchor='e', font=("bold", 10))
label_1.place(x=65,y=130)
entry_1 = Entry(root, width=60)
entry_1.place(x=240, y=130)
btn_1 = Button(root, text="check", width=6, bg='light grey', fg='black', command=lambda:check_path(entry_1.get())) # command=query
btn_1.place(x=610, y=127)

#LABEL 2############
label_2 = Label(root, text="Database file name", width=20, anchor='e', font=("bold", 10))
label_2.place(x=65,y=180)
entry_2 = Entry(root, width=60)
entry_2.place(x=240, y=180)

#LABEL 3############
label_3 = Label(root, text="Download db", width=20, anchor='e', font=("bold", 10))
label_3.place(x=70,y=230)
var = IntVar()
Radiobutton(root, text="Yes", padx = 5, variable=var, value=1, command=lambda:setTextInput("Please type here a date you choose. (Eg.: 'Y2021W01', 'Y2021W04')")).place(x=235, y=230)
Radiobutton(root, text="No", padx = 20, variable=var, value=2, command=lambda:setTextInput("No need a date")).place(x=290, y=230)

label_4 = Label(root, text="Database dates", width=20, anchor='e', font=("bold", 10))
label_4.place(x=65, y=280)
entry_4 = Entry(root, textvariable='Yes', width=60)
entry_4.place(x=240, y=280)

# label_4 = Label(root, text="country",width=20,font=("bold", 10))
# label_4.place(x=70,y=280)
#
# list1 = ['Canada','India','UK','Nepal','Iceland','South Africa'];
# c=StringVar()
# droplist=OptionMenu(root,c, *list1)
# droplist.config(width=15)
# c.set('select your country')
# droplist.place(x=240,y=280)
#
# label_4 = Label(root, text="Programming",width=20,font=("bold", 10))
# label_4.place(x=85,y=330)
# var1 = IntVar()
# Checkbutton(root, text="java", variable=var1).place(x=235,y=330)
# var2 = IntVar()
# Checkbutton(root, text="python", variable=var2).place(x=290,y=330)

# Create Buttons
submit_btn = Button(root, text='Submit', width=20, bg='brown', fg='white')
submit_btn.place(relx=0.5, rely=0.8, anchor='center') # x=180,y=380

help_btn = Button(root, text="Instruction", width=20, bg='light grey', fg='black', command=lambda:[display_text(model_description)]) # command=query
help_btn.place(relx=0.5, rely=0.7, anchor='center')


root.mainloop()