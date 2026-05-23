import sys

import pygame


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480

BOARD_SIZE = 360
GRID_SIZE = 3
CELL_SIZE = BOARD_SIZE // GRID_SIZE
FPS = 60

HUD_BG = (245, 248, 250)
PLAYFIELD_BG = (255, 255, 255)
PLAYFIELD_BORDER = (160, 170, 180)
TEXT_COLOR = (20, 20, 20)
GRID_COLOR = (95, 105, 115)
X_COLOR = (25, 25, 25)
O_COLOR = (30, 170, 90)
WIN_LINE_COLOR = (190, 30, 45)
BUTTON_BG = (228, 234, 238)
BUTTON_BORDER = (150, 162, 170)


BOARD_LEFT = (WINDOW_WIDTH - BOARD_SIZE) // 2
BOARD_TOP = (WINDOW_HEIGHT - BOARD_SIZE) // 2
STATUS_Y = BOARD_TOP - 28
RESTART_BUTTON_RECT = pygame.Rect(WINDOW_WIDTH - 130, 16, 110, 36)


def create_board():
    return [["" for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]


def draw_board(surface):
    board_rect = pygame.Rect(BOARD_LEFT, BOARD_TOP, BOARD_SIZE, BOARD_SIZE)
    pygame.draw.rect(surface, PLAYFIELD_BG, board_rect)
    pygame.draw.rect(surface, PLAYFIELD_BORDER, board_rect, width=2)

    for i in range(1, GRID_SIZE):
        x = BOARD_LEFT + (i * CELL_SIZE)
        y = BOARD_TOP + (i * CELL_SIZE)
        pygame.draw.line(surface, GRID_COLOR, (x, BOARD_TOP), (x, BOARD_TOP + BOARD_SIZE), 2)
        pygame.draw.line(surface, GRID_COLOR, (BOARD_LEFT, y), (BOARD_LEFT + BOARD_SIZE, y), 2)


def draw_marks(surface, board):
    padding = 24
    stroke = 8

    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            value = board[row][col]
            if value == "":
                continue

            cell_left = BOARD_LEFT + (col * CELL_SIZE)
            cell_top = BOARD_TOP + (row * CELL_SIZE)
            center = (cell_left + (CELL_SIZE // 2), cell_top + (CELL_SIZE // 2))

            if value == "X":
                pygame.draw.line(
                    surface,
                    X_COLOR,
                    (cell_left + padding, cell_top + padding),
                    (cell_left + CELL_SIZE - padding, cell_top + CELL_SIZE - padding),
                    stroke,
                )
                pygame.draw.line(
                    surface,
                    X_COLOR,
                    (cell_left + CELL_SIZE - padding, cell_top + padding),
                    (cell_left + padding, cell_top + CELL_SIZE - padding),
                    stroke,
                )
            else:
                radius = (CELL_SIZE // 2) - padding
                pygame.draw.circle(surface, O_COLOR, center, radius, stroke)


def find_winner(board):
    for row in range(GRID_SIZE):
        if board[row][0] != "" and board[row][0] == board[row][1] == board[row][2]:
            return board[row][0], ((0, row), (2, row))

    for col in range(GRID_SIZE):
        if board[0][col] != "" and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col], ((col, 0), (col, 2))

    if board[0][0] != "" and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0], ((0, 0), (2, 2))

    if board[0][2] != "" and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2], ((2, 0), (0, 2))

    return None, None


def draw_win_line(surface, line_cells):
    if line_cells is None:
        return

    (start_col, start_row), (end_col, end_row) = line_cells
    start_x = BOARD_LEFT + (start_col * CELL_SIZE) + (CELL_SIZE // 2)
    start_y = BOARD_TOP + (start_row * CELL_SIZE) + (CELL_SIZE // 2)
    end_x = BOARD_LEFT + (end_col * CELL_SIZE) + (CELL_SIZE // 2)
    end_y = BOARD_TOP + (end_row * CELL_SIZE) + (CELL_SIZE // 2)

    pygame.draw.line(surface, WIN_LINE_COLOR, (start_x, start_y), (end_x, end_y), 7)


def board_cell_from_mouse(pos):
    x, y = pos
    if not (BOARD_LEFT <= x < BOARD_LEFT + BOARD_SIZE and BOARD_TOP <= y < BOARD_TOP + BOARD_SIZE):
        return None

    col = (x - BOARD_LEFT) // CELL_SIZE
    row = (y - BOARD_TOP) // CELL_SIZE
    return row, col


def board_full(board):
    return all(cell != "" for row in board for cell in row)


def draw_restart_button(surface, font):
    pygame.draw.rect(surface, BUTTON_BG, RESTART_BUTTON_RECT, border_radius=7)
    pygame.draw.rect(surface, BUTTON_BORDER, RESTART_BUTTON_RECT, width=1, border_radius=7)
    text_surf = font.render("Restart", True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=RESTART_BUTTON_RECT.center)
    surface.blit(text_surf, text_rect)


def draw_vs_status(surface, font):
    x_text = font.render("X", True, X_COLOR)
    vs_text = font.render(" vs ", True, TEXT_COLOR)
    o_text = font.render("O", True, O_COLOR)

    total_width = x_text.get_width() + vs_text.get_width() + o_text.get_width()
    start_x = (WINDOW_WIDTH - total_width) // 2
    y = STATUS_Y - (x_text.get_height() // 2)

    surface.blit(x_text, (start_x, y))
    surface.blit(vs_text, (start_x + x_text.get_width(), y))
    surface.blit(o_text, (start_x + x_text.get_width() + vs_text.get_width(), y))


def reset_round():
    return create_board(), "X", False, None, ""


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Tic Tac Toe")

    title_font = pygame.font.SysFont(None, 44)
    hint_font = pygame.font.SysFont(None, 28)
    clock = pygame.time.Clock()

    board, current_player, game_over, win_line_cells, result_text = reset_round()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key in (pygame.K_SPACE, pygame.K_r):
                    board, current_player, game_over, win_line_cells, result_text = reset_round()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if RESTART_BUTTON_RECT.collidepoint(event.pos):
                    board, current_player, game_over, win_line_cells, result_text = reset_round()
                    continue

                if game_over:
                    continue

                selected = board_cell_from_mouse(event.pos)
                if selected is None:
                    continue

                row, col = selected
                if board[row][col] != "":
                    continue

                board[row][col] = current_player
                winner, line_cells = find_winner(board)

                if winner is not None:
                    game_over = True
                    win_line_cells = line_cells
                    result_text = f"{winner} wins"
                elif board_full(board):
                    game_over = True
                    result_text = "Tie game"
                else:
                    current_player = "O" if current_player == "X" else "X"

        screen.fill(HUD_BG)
        draw_board(screen)
        draw_marks(screen, board)
        draw_win_line(screen, win_line_cells)
        draw_restart_button(screen, hint_font)

        if game_over:
            if result_text.startswith("X"):
                status_color = X_COLOR
            elif result_text.startswith("O"):
                status_color = O_COLOR
            else:
                status_color = WIN_LINE_COLOR

            status_surf = title_font.render(result_text, True, status_color)
            status_rect = status_surf.get_rect(center=(WINDOW_WIDTH // 2, STATUS_Y))
            screen.blit(status_surf, status_rect)
        else:
            draw_vs_status(screen, title_font)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()