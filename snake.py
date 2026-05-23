import random
import sys

import pygame


WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // CELL_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

FPS_START = 8
FPS_MAX = 24

BACKGROUND = (245, 248, 250)
SNAKE_COLOR = (25, 25, 25)
FOOD_COLOR = (30, 170, 90)
TEXT_COLOR = (20, 20, 20)
GAME_OVER_COLOR = (190, 30, 45)
PANEL_BG = (228, 234, 238)
PANEL_BORDER = (150, 162, 170)


UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def random_food_position(snake):
    """Return a random grid position not occupied by the snake."""
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos


def draw_grid_cell(surface, color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def draw_text(surface, text, font, color, topleft):
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, topleft)


def draw_controls_panel(surface, font):
    lines = [
        "Controls",
        "Move: WASD / Arrows",
        "Pause: SPACE",
        "Quit: ESC",
    ]

    rendered_lines = [font.render(line, True, TEXT_COLOR) for line in lines]
    max_width = max(line.get_width() for line in rendered_lines)
    line_height = rendered_lines[0].get_height()
    panel_padding_x = 12
    panel_padding_y = 10
    panel_width = max_width + panel_padding_x * 2
    panel_height = (line_height * len(rendered_lines)) + panel_padding_y * 2 + 6

    panel_x = WINDOW_WIDTH - panel_width - 10
    panel_y = 8
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, panel_rect, width=1, border_radius=8)

    current_y = panel_y + panel_padding_y
    for index, line in enumerate(rendered_lines):
        surface.blit(line, (panel_x + panel_padding_x, current_y))
        current_y += line_height + (4 if index == 0 else 2)


def draw_score_panel(surface, font, score, high_score):
    lines = [
        f"Score: {score}",
        f"High Score: {high_score}",
    ]

    rendered_lines = [font.render(line, True, TEXT_COLOR) for line in lines]
    max_width = max(line.get_width() for line in rendered_lines)
    line_height = rendered_lines[0].get_height()
    panel_padding_x = 12
    panel_padding_y = 10
    panel_width = max_width + panel_padding_x * 2
    panel_height = (line_height * len(rendered_lines)) + panel_padding_y * 2 + 4

    panel_x = 10
    panel_y = 8
    panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
    pygame.draw.rect(surface, PANEL_BG, panel_rect, border_radius=8)
    pygame.draw.rect(surface, PANEL_BORDER, panel_rect, width=1, border_radius=8)

    current_y = panel_y + panel_padding_y
    for line in rendered_lines:
        surface.blit(line, (panel_x + panel_padding_x, current_y))
        current_y += line_height + 2


def reset_game():
    center_x = GRID_WIDTH // 2
    center_y = GRID_HEIGHT // 2
    snake = [
        (center_x, center_y),
        (center_x - 1, center_y),
        (center_x - 2, center_y),
    ]
    direction = RIGHT
    next_direction = RIGHT
    food = random_food_position(snake)
    score = 0
    fps = FPS_START
    game_over = False
    paused = False
    return snake, direction, next_direction, food, score, fps, game_over, paused


def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")

    score_font = pygame.font.SysFont(None, 30)
    title_font = pygame.font.SysFont(None, 50)
    hint_font = pygame.font.SysFont(None, 28)
    controls_font = pygame.font.SysFont(None, 22)

    clock = pygame.time.Clock()

    snake, direction, next_direction, food, score, fps, game_over, paused = reset_game()
    high_score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                if game_over and event.key == pygame.K_SPACE:
                    snake, direction, next_direction, food, score, fps, game_over, paused = reset_game()
                    continue

                if not game_over and event.key == pygame.K_SPACE:
                    paused = not paused
                    continue

                if event.key in (pygame.K_UP, pygame.K_w):
                    if direction != DOWN:
                        next_direction = UP
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    if direction != UP:
                        next_direction = DOWN
                elif event.key in (pygame.K_LEFT, pygame.K_a):
                    if direction != RIGHT:
                        next_direction = LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    if direction != LEFT:
                        next_direction = RIGHT

        if not game_over and not paused:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = (head_x + dx, head_y + dy)

            hit_wall = (
                new_head[0] < 0
                or new_head[0] >= GRID_WIDTH
                or new_head[1] < 0
                or new_head[1] >= GRID_HEIGHT
            )
            hit_self = new_head in snake

            if hit_wall or hit_self:
                game_over = True
            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 1
                    high_score = max(high_score, score)
                    food = random_food_position(snake)
                    fps = min(FPS_MAX, FPS_START + score // 2)
                else:
                    snake.pop()

        screen.fill(BACKGROUND)

        for segment in snake:
            draw_grid_cell(screen, SNAKE_COLOR, segment)

        draw_grid_cell(screen, FOOD_COLOR, food)

        draw_score_panel(screen, score_font, score, high_score)
        draw_controls_panel(screen, controls_font)

        if game_over:
            game_over_text = title_font.render("Game Over", True, GAME_OVER_COLOR)
            restart_text = hint_font.render("Press SPACE to restart", True, TEXT_COLOR)
            quit_text = hint_font.render("Press ESC to quit", True, TEXT_COLOR)

            game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 35))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 5))
            quit_rect = quit_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 35))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(restart_text, restart_rect)
            screen.blit(quit_text, quit_rect)
        elif paused:
            paused_text = title_font.render("Paused", True, TEXT_COLOR)
            resume_text = hint_font.render("Press SPACE to resume", True, TEXT_COLOR)

            paused_rect = paused_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 15))
            resume_rect = resume_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))

            screen.blit(paused_text, paused_rect)
            screen.blit(resume_text, resume_rect)

        pygame.display.flip()
        clock.tick(fps)


if __name__ == "__main__":
    main()
