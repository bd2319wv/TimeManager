__author__ = 'Andre'

from tkinter import messagebox
from tkinter import *
import sqlite3

# create a connection to the newly made database
cxn = sqlite3.connect('GymDB')
# initialize a cursor object to run execute commands on the connected database.
cur = cxn.cursor()

#Class for searching for instructors, times, or classes
class Search:

    #myMainWindowClass = MainWindow(empName)
    def __init__(self, master):
        #creates master window for calculation window, changes title, and sets size
        self.master = master
        self.master.title("Search")
        self.master.geometry("250x200")

        #Sets the string variable and checkBox variables
        self.userSearchInput = StringVar()
        self.chkVar1 = IntVar()
        self.chkVar2 = IntVar()
        self.chkVar3 = IntVar()
        self.chkVar4 = IntVar()

        #Widgets
        self.chkBtnInstructorName = Checkbutton(self.master, text="Instructor Last Name", variable=self.chkVar1, justify=LEFT)
        self.chkBtnClassName = Checkbutton(self.master, text="Class Name", variable=self.chkVar2, justify=LEFT)
        self.chkBtnClassDay = Checkbutton(self.master, text="Class Day", variable=self.chkVar3, justify=LEFT)
        self.chkBtnAllClassStudent = Checkbutton(self.master, text="Student class registers", variable=self.chkVar4, justify=LEFT)
        self.lblSearchInformation = Label(self.master, text="Search For Instructor, Classes, or schedules")
        self.lblSearch = Label(self.master, text="Search: ")
        self.txtBoxSearch = Entry(self.master, textvariable=self.userSearchInput)

        #Search Button
        self.btnSearch = Button(self.master, text="Search", width=12, command=self.searchQuery)
        #Close Button
        self.btnClose = Button(self.master, text="Close", width=12, command=self.quit)

        #Aligns the labels using the grid
        self.lblSearchInformation.grid(row=1, columnspan=1, sticky=W)
        self.chkBtnInstructorName.grid(row=2, columnspan=1, sticky=W)
        self.chkBtnClassName.grid(row=3, columnspan=1, sticky=W)
        self.chkBtnClassDay.grid(row=4, columnspan=1, sticky=W)
        self.chkBtnAllClassStudent.grid(row=5, columnspan=1, sticky=W)
        self.lblSearch.grid(row=6, columnspan=1, sticky=W)
        self.txtBoxSearch.grid(row=7, columnspan=1, sticky=W)
        self.btnSearch.grid(row=8, columnspan=1, sticky=W)
        self.btnClose.grid(row=9, columnspan=1, sticky=W)

    #Searh Query Function
    def searchQuery(self):
        self.userSearchCriteria = self.userSearchInput.get()

        if(self.userSearchCriteria == ""):
            messagebox.showerror("Entry Error", "Textbox cannot be empty")
        else:
            try:
                #TODO: Example for output not in tuple, aply to rest, make multiples possible
                #Gets the state of the checkboxes and then searches with the user input
                if(self.chkVar1.get()):
                    instructorlist = []
                    cur.execute("SELECT * FROM Instructor WHERE lastName LIKE ?", (self.userSearchCriteria,))
                    for info in cur.fetchall():
                        instructor = "ID: " + str(info[0]) + " Name: " + info[1] + " " + info[2] + " Address: " + info[3]
                        instructorlist.append(instructor)
                    msg = "\n".join(instructorlist)
                    messagebox._show("Query Results", msg)

                elif(self.chkVar2.get()):
                    cur.execute("SELECT * FROM Class WHERE code LIKE ?", (self.userSearchCriteria,))
                    messagebox.showwarning("Query Results", cur.fetchall())

                elif(self.chkVar3.get()):
                    cur.execute("SELECT * FROM Schedule WHERE Day LIKE ?", (self.userSearchCriteria,))
                    messagebox.showwarning("Query Results", cur.fetchall())

                elif(self.chkVar4.get()):
                    register = []
                    cur.execute("SELECT * FROM ClassStudent")
                    for info in cur.fetchall():
                        instructor = "Code: " + str(info[0]) + " Sequence: " + str(info[1]) + " Student ID:" + str(info[2]) +"\n"
                        register.append(instructor)
                    msg = "\n".join(register)
                    messagebox._show("Query Results", msg)

            except sqlite3.IntegrityError:
                messagebox.showwarning("Search Error", "No matches could be found")

            finally:
                cxn.commit()

    def quit(self):
        self.master.destroy()
