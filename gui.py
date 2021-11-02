from tkinter import *
import os
import time

# checking if the path is correct
def check_path(p):
    folderPath = p

    if not os.path.exists(folderPath):
        ans = "Error! Podany folder nie istnieje. Spróbuj ponownie."
        display_text(ans)
        time.sleep(3)
        folderPath = check_path()
    ans = "Wszystko jest ok."
    display_text(ans)
    # requiaredFiles = ["StoreCountryGroup.csv", "GradeCutOff.csv", "GradeSellOff.csv", "DSParam.csv"]
    # for file in requiaredFiles:
    #     while not(os.path.isfile(folderPath + file)):
    #         print("Error! Umieść w folderze plik ", file, " i zatwierdź.")
    #         input()
    #
    #     print("Plik ", file, " jest.")
    #
    # return folderPath

def display_text(content):
    T = Text(root, bg='white', width=20, height=5.5, font=10, padx=10, pady=10)
    T.place(relx=0.65, rely=0.65)
    T.insert(1.0, content)
    T.tag_configure("center", justify="center")
    T.tag_add("center", 1.0, "end")

root = Tk()
root.geometry('800x500')
root.title("Lost Sales Model")

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
Radiobutton(root, text="Yes", padx = 5, variable=var, value=1).place(x=235, y=230)
Radiobutton(root, text="No", padx = 20, variable=var, value=2).place(x=290, y=230)

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

help_btn = Button(root, text="Instruction", width=20, bg='light grey', fg='black') # command=query
help_btn.place(relx=0.5, rely=0.7, anchor='center')

root.mainloop()