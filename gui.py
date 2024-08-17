#create a hello world gui
from tkinter import * #import tkinter module
root = Tk() #create a root window
root.title("CLARKSONS COOKIE CLICKER") #set title of the window
root.geometry("300x200") #set the size of the window
label = Label(root, text="COOKIE CLICKER") #create a label
label.pack() #pack the label



#have a label called cookies that starts at 0
cookies = 0
cookie_label = Label(root, text="Cookies: " + str(cookies))
cookie_label.pack()

#add a button that increments the cookies label by 1 when clicked that looks like a cookie
def increment_cookies():
    global cookies
    cookies += 1
    cookie_label.config(text="Cookies: " + str(cookies))

cookie_button = Button(root, text="Cookie?", command=increment_cookies)
cookie_button.pack()

root.mainloop() #run the main loop
