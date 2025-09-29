from tkinter import *

root = Tk()
root.title("X vs O")
root.geometry("225x300")

board = [["" for _ in range(3)] for _ in range(3)]
current_player = "X"
turns = 0
game_over = False

def check_winner():
    lines = (
        board +
        [list(col) for col in zip(*board)] +
        [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    )
    for line in lines:
        if line[0] and line.count(line[0]) == 3:
            return line[0]
    return None

def button_click(row, col):
    global current_player, turns, game_over

    if board[row][col] or game_over:
        label.config(text="Invalid move!" if not game_over else label.cget("text"))
        return

    board[row][col] = current_player
    buttons[row][col].config(text=current_player, state=DISABLED)
    turns += 1

    winner = check_winner()
    if winner:
        label.config(text=f"{winner} wins!")
        game_over = True
    elif turns == 9:
        label.config(text="It's a tie!")
        game_over = True
    else:
        current_player = "O" if current_player == "X" else "X"

def restart_game():
    global board, current_player, turns, game_over
    board = [["" for _ in range(3)] for _ in range(3)]
    current_player = "X"
    turns = 0
    game_over = False
    label.config(text="")

    for i in range(3):
        for j in range(3):
            buttons[i][j].config(text="", state=NORMAL, width=8, height=4)

buttons = [[Button(root, text="", width=8, height=4,
                   command=lambda r=i, c=j: button_click(r, c))
            for j in range(3)] for i in range(3)]
for i in range(3):
    for j in range(3):
        buttons[i][j].grid(row=i, column=j)

label = Label(root, text="Tic Tac Toe", font=("Arial", 16))
label = Label(root, text="X vs O", font=("Arial", 16))
label.grid(row=3, columnspan=3, pady=10)

restart_btn = Button(root, text="Restart", command=restart_game)
restart_btn.grid(row=4, columnspan=3, pady=10)

root.mainloop()