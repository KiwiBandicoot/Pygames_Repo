#create a hello world gui
from tkinter import * #import tkinter module
root = Tk() #create a root window
root.title("CLARKSONS COOKIE CLICKER") #set title of the window
root.geometry("200x200") #set the size of the window
label = Label(root, text="COOKIE CLICKER") #create a label
label.pack() #pack the label


#add a stopwatch that starts at 0 as soon as app is opened
stopwatch = 0
stopwatch_label = Label(root, text="Stopwatch: " + str(stopwatch))
stopwatch_label.pack()


def start_stopwatch():
    increment_stopwatch()

def increment_stopwatch():
    global stopwatch
    stopwatch += 1
    stopwatch_label.config(text="Stopwatch: " + str(stopwatch))
    #delay of 1000ms
    root.after(1000, increment_stopwatch)

#have a label called cookies that starts at 0
cookies = 0
cookie_label = Label(root, text="Cookies: " + str(cookies))
cookie_label.pack()

#add a button that increments the cookies label by 1 when clicked that looks like a cookie
def increment_cookies():
    global cookies
    if(stopwatch > 0):
        cookies += 1
    cookie_label.config(text="Cookies: " + str(cookies))

cookie_button = Button(root, text="Cookie?", command=increment_cookies)
cookie_button.pack()

#add a button that starts the stopwatch and shows the cookie button
start_button = Button(root, text="Start", command=start_stopwatch)
start_button.pack()


root.mainloop() #run the main loop

