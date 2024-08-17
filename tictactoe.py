#make tic tac toe game gui
from tkinter import * #import tkinter module
root = Tk() #create a root window
root.title("cookies vs cream") #set title of the window
root.geometry("400x400") #set the size of the window
#initialize the game board
board = [["" for i in range(3)] for j in range(3)]
#initialize the current player
current_player = "cookies"
#initialize the winner
winner = None
#initialize the game over flag
game_over = False
#initialize the number of turns
turns = 0

#function to check if the game is over
def check_game_over():
    global game_over
    global winner
    #check rows
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            winner = board[i][0]
            game_over = True
    #check columns
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            winner = board[0][i]
            game_over = True
    #check diagonals
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        winner = board[0][0]
        game_over = True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        winner = board[0][2]
        game_over = True
    #check for a tie
    if turns == 9 and winner == None:
        game_over = True

#function to handle the button click event

def button_click(row, col):
    global current_player
    global board
    global turns
    global game_over
    if board[row][col] == "" and not game_over:
        board[row][col] = current_player
        button = Button(root, text=current_player, state=DISABLED)
        button.grid(row=row, column=col, ipadx=40, ipady=40)
        turns += 1
        check_game_over()
        if not game_over:
            if current_player == "cookies":
                current_player = "cream"
            else:
                current_player = "cookies"
        if game_over:
            if winner == None:
                label.config(text="It's a tie!")
            else:
                label.config(text=winner + " wins!")
    else:
        label.config(text="Invalid move!")

#initialize the buttons
buttons = [[Button(root, text="", command=lambda row=i, col=j: button_click(row, col)) for j in range(3)] for i in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i, column=j, ipadx=40, ipady=40)

#initialize the label
label = Label(root, text="")
label.grid(row=3, columnspan=3)

root.mainloop() #run the main loop