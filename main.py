import pygame
import random

pygame.init()

# initialize the screen
# region VARIABLES
"""
Variables used in the game
    - window_width: int -> width of the window
    - window_height: int -> height of the window
    - font: pygame.font.Font -> font used in the game
    - fps: int -> frames per second
    - colors: dict -> dictionary with colors used in the game
    - board_rectangle_dimensions: list -> dimensions of the board
    - board_border_width: int -> border width of the board
    - board_rectangle_border_radius: int -> border radius of the board
    - game_over_rect: list -> dimensions of the game over screen
    - board_values: list -> values of the board
    - game_over: bool -> game over flag
    - spawn_new: bool -> flag to spawn a new piece
    - init_pieces_count: int -> initial pieces count
    - direction: str -> direction of the move
    - score: int -> score of the game
    - high_score: int -> high score of the game
    - init_high_score: int -> initial high score of the game
"""
window_width = 400
window_height = 500
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("2048")

timer = pygame.time.Clock()
fps = 60
font = pygame.font.SysFont('Arial', 24)

# color library
colors = {0: (251, 248, 204),
          2: (253, 228, 207),
          4: (255, 207, 210),
          8: (241, 192, 232),
          16: (207, 186, 240),
          32: (163, 196, 243),
          64: (144, 219, 244),
          128: (142, 236, 245),
          256: (152, 245, 225),
          512: (185, 251, 192),
          1024: (175, 252, 175),
          2048: (149, 247, 186),
          "light_text": (126, 130, 135),
          "dark_text": (42, 43, 46),
          "other": (105, 153, 93),
          "bg": (42, 43, 46),
          "screen_color": (251, 251, 251),
          "game_over": (193, 98, 0),
          }

# board variables definitions
board_rectangle_dimensions = [0, 0, 400, 400]
board_border_width = 0
board_rectangle_border_radius = 10

# game over screen
game_over_rect = [50, 50, 300, 100]

# game variables
# _ is a variable that is not going to be used -> not necessary to give it a name
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True

init_pieces_count = 0
direction = ''

score = 0

try:
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

init_high_score = high_score


# endregion VARIABLES
def draw_board():
    """
    Draw the board on the screen using the pygame.draw.rect function
    """
    pygame.draw.rect(screen, colors["bg"], board_rectangle_dimensions, board_border_width,
                     board_rectangle_border_radius)

    # Display scores
    score_text = font.render(f"Score: {score}", True, colors['dark_text'])
    high_score_text = font.render(f"High Score: {high_score}", True, colors['dark_text'])
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


def draw_pieces(board):
    """
    Draw the pieces on the board
    Colors of the pieces are defined in the colors dictionary by numbers in it
    Text color inside is defined by the value of the piece + font scale is adjusted based on the length of the value
    Args:
        board: list -> values of the board
    """
    for i in range(len(board)):
        for j in range(len(board)):
            value = board[i][j]
            # different colors for different values
            if value < 2048:
                value_color = colors["dark_text"]
            else:
                value_color = colors["light_text"]
            if value <= 2048:
                color = colors[value]
            else:
                color = colors["other"]
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 10)
            if value > 0:
                value_len = len(str(value))
                piece_font = pygame.font.SysFont('Arial', 48 - (value_len * 5))
                value_text = piece_font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, colors["light_text"], [j * 95 + 20, i * 95 + 20, 75, 75], 2, 10)


def draw_over():
    """
    Draw the game over screen
    """
    pygame.draw.rect(screen, colors["game_over"], game_over_rect, board_border_width, board_rectangle_border_radius)
    game_over_text = font.render("Game Over", True, colors["light_text"])
    press_enter_text = font.render("Press Enter to play again", True, colors["dark_text"])
    screen.blit(game_over_text, (130, 65))
    screen.blit(press_enter_text, (70, 105))


def spawn_piece(board):
    """
    Spawn a new piece on the board per function call and checks if the game is over
    Args:
        board: list -> values of the board
    """
    # only one new piece per function call
    count = 0
    full_board = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        if board[row][col] == 0:
            count += 1
            # one in ten chance of getting a 4
            if random.randint(1, 10) == 1:
                board[row][col] = 4
            else:
                board[row][col] = 2

    if count == 0 and not can_move_check(board):
        return board, True  # game over

    return board, False  # game not over


def move_board(board, move_direction):
    """
    Move the board in the given direction
    Args:
        board: list -> values of the board
        move_direction: str -> direction of the move
    """
    global score
    if move_direction == "UP":
        board, score = move_up(board, score)
    elif move_direction == "DOWN":
        board, score = move_down(board, score)
    elif move_direction == "LEFT":
        board, score = move_left(board, score)
    elif move_direction == "RIGHT":
        board, score = move_right(board, score)
    return board


# region MOVE FUNCTIONS
def move_up(board, global_score):
    """
    Move the board up and merge the tiles + update the score
    Args:
        board: list -> values of the board
        global_score: int -> score of the game
    Return:
        board: list -> updated values of the board after move UP
        global_score: int -> updated score of the game
    """
    size = len(board)
    for col in range(size):
        # Compact the column
        new_col = [tile for tile in [board[row][col] for row in range(size)] if tile != 0]
        # Merge tiles
        merged_col = []
        skip = False
        for i in range(len(new_col)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_col) and new_col[i] == new_col[i + 1]:
                merged_col.append(new_col[i] * 2)
                global_score += new_col[i] * 2
                skip = True
            else:
                merged_col.append(new_col[i])
        # Fill the remaining spaces with zeros
        merged_col += [0] * (size - len(merged_col))
        # Place back into the board
        for row in range(size):
            board[row][col] = merged_col[row]
    return board, global_score


def move_down(board, global_score):
    """
        Move the board down and merge the tiles + update the score
        Args:
            board: list -> values of the board
            global_score: int -> score of the game
        Return:
            board: list -> updated values of the board after move DOWN
            global_score: int -> updated score of the game
    """
    size = len(board)
    for col in range(size):
        # Compact the column in reverse (bottom to top)
        new_col = [tile for tile in [board[row][col] for row in range(size - 1, -1, -1)] if tile != 0]
        # Merge tiles
        merged_col = []
        skip = False
        for i in range(len(new_col)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_col) and new_col[i] == new_col[i + 1]:
                merged_col.append(new_col[i] * 2)
                global_score += new_col[i] * 2
                skip = True
            else:
                merged_col.append(new_col[i])
        # Fill the remaining spaces with zeros, reverse before placing back
        merged_col += [0] * (size - len(merged_col))
        for row in range(size):
            board[size - 1 - row][col] = merged_col[row]
    return board, global_score


def move_left(board, global_score):
    """
        Move the board left and merge the tiles + update the score
        Args:
            board: list -> values of the board
            global_score: int -> score of the game
        Return:
            board: list -> updated values of the board after move LEFT
            global_score: int -> updated score of the game
    """
    size = len(board)
    for row in range(size):
        # Compact the row
        new_row = [tile for tile in board[row] if tile != 0]
        # Merge tiles
        merged_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged_row.append(new_row[i] * 2)
                global_score += new_row[i] * 2
                skip = True
            else:
                merged_row.append(new_row[i])
        # Fill the remaining spaces with zeros
        merged_row += [0] * (size - len(merged_row))
        board[row] = merged_row
    return board, global_score


def move_right(board, global_score):
    """
        Move the board right and merge the tiles + update the score
        Args:
            board: list -> values of the board
            global_score: int -> score of the game
        Return:
            board: list -> updated values of the board after move RIGHT
            global_score: int -> updated score of the game
    """
    size = len(board)
    for row in range(size):
        # Compact the row in reverse (right to left)
        new_row = [tile for tile in board[row] if tile != 0][::-1]
        # Merge tiles
        merged_row = []
        skip = False
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged_row.append(new_row[i] * 2)
                global_score += new_row[i] * 2
                skip = True
            else:
                merged_row.append(new_row[i])
        # Fill the remaining spaces with zeros, reverse before placing back
        merged_row += [0] * (size - len(merged_row))
        board[row] = merged_row[::-1]
    return board, global_score


# endregion MOVE FUNCTIONS


def can_move_check(board):
    """
    Check if the board can be moved in any direction (up, down, left, right) by checking if there are any same adjacent
    For determining if the game is over
    Args:
        board: list -> values of the board
    Return:
        bool -> True if the board can be moved in any direction, False otherwise
    """
    size = len(board)
    for i in range(size):
        for j in range(size):
            if i < size - 1 and board[i][j] == board[i + 1][j]:
                return True  # Check vertical moves
            if j < size - 1 and board[i][j] == board[i][j + 1]:
                return True  # Check horizontal moves
    return False


# main menu
def main_menu():
    """
    Draw the main menu of the game with the start and exit buttons
    """
    menu = True
    while menu:
        screen.fill(colors["screen_color"])
        # Menu Title
        title = font.render("2048 Game", True, colors["dark_text"])
        title_rect = title.get_rect(center=(window_width / 2, 150))
        screen.blit(title, title_rect)

        # Start Game Button
        start_game_text = font.render("Start Game", True, colors["dark_text"])
        start_game_rect = start_game_text.get_rect(center=(window_width / 2, 250))
        screen.blit(start_game_text, start_game_rect)

        # Exit Game Button
        exit_game_text = font.render("Exit Game", True, colors["dark_text"])
        exit_game_rect = exit_game_text.get_rect(center=(window_width / 2, 300))
        screen.blit(exit_game_text, exit_game_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if start_game_rect.collidepoint(mouse_pos):
                    menu = False
                    return True
                elif exit_game_rect.collidepoint(mouse_pos):
                    menu = False
                    return False

        timer.tick(fps)


def return_to_menu():
    return main_menu()


def draw_return_button():
    """
    Draw the return to menu button on the game screen
    """
    return_text = font.render("Return to Menu", True, colors["light_text"])
    return_rect = return_text.get_rect(center=(300, 470))
    pygame.draw.rect(screen, colors["bg"], return_rect.inflate(20, 10))
    screen.blit(return_text, return_rect)
    return return_rect


"""
    Main game loop
"""
run = main_menu()
if run:
    while run:
        timer.tick(fps)
        screen.fill(colors["screen_color"])

        return_rect = draw_return_button()

        draw_board()
        draw_pieces(board_values)

        if spawn_new or init_pieces_count < 2:
            board_values, game_over = spawn_piece(board_values)
            spawn_new = False
            init_pieces_count += 1

        if direction != '':
            board_values = move_board(board_values, direction)
            direction = ''
            spawn_new = True

        if game_over:
            draw_over()
            if high_score > init_high_score:
                with open('high_score.txt', 'w') as file:
                    file.write(str(high_score))
            init_high_score = high_score

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if return_rect.collidepoint(event.pos):
                    run = return_to_menu()
                    if not run:
                        break

            if event.type == pygame.KEYUP and not game_over:
                if event.key == pygame.K_UP:
                    direction = "UP"
                elif event.key == pygame.K_DOWN:
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT:
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT:
                    direction = "RIGHT"

            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

        if score > high_score:
            high_score = score

        pygame.display.flip()

pygame.quit()
