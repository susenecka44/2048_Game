import pygame
import random

"""
---------------------------------------------------------------------   
    This is a 2048 game implementation using Pygame library
---------------------------------------------------------------------
    - The game has two modes: Classic and Timed
    - Classic mode: The player can play the game without any time limit
    - Timed mode: The player has a time limit of 3 minutes to play the game
    - The player can undo the last move with a cooldown of 10 moves
    - The player can return to the main menu at any time
    - The game has a high score system for both modes
    - The game has a tutorial screen to explain the rules of the game

Author: Julie Vondráčková
Date: 28-5-2024
* Done for the Programming in Python course at Charles University 
---------------------------------------------------------------------
"""

pygame.init()

# region VARIABLES
"""
Variables used in the game
    - window_width: int -> width of the game window
    - window_height: int -> height of the game window
    
    - timer: pygame.time.Clock -> timer for the game
    - fps: int -> frames per second
    
    - font: pygame.font.Font -> font for the game
    - colors: dict -> colors used in the game
    
    - board_rectangle_dimensions: list -> dimensions of the board rectangle
    - board_border_width: int -> width of the board border
    - board_rectangle_border_radius: int -> border radius of the board rectangle
    - game_over_rect: list -> dimensions of the game over rectangle
    
    - board_values: list -> values of the board
    
    - game_over: bool -> game over status
    - spawn_new: bool -> spawn new piece status
    
    - init_pieces_count: int -> initial pieces count
    - direction: str -> direction of the move
    
    - score: int -> score of the game
    - high_score: int -> high score of the game
    - init_high_score: int -> initial high score
    - timed_score: int -> score of the timed game
    - timed_high_score: int -> high score of the timed game
    - init_time_high_score: int -> initial high score of the timed game
    
    - cooldown_counter: int -> cooldown counter for the undo button
    - previous_states: list -> previous states of the board
    
    - run: bool -> run status of the game
    
    - start_time: int -> start time of the timed game
    
    - current_game_mode -> tracks the currently selected game mode

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
          "screen_color": (251, 251, 251)
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
    with open('score_files/high_score.txt', 'r') as file:
        high_score = int(file.read())
except FileNotFoundError:
    high_score = 0

init_high_score = high_score

# return buttons
previous_states = []
cooldown_counter = 10

# timed game variables
start_time = pygame.time.get_ticks()
timed_score = 0
try:
    with open('score_files/timed_high_score.txt', 'r') as file:
        timed_high_score = int(file.read())
except FileNotFoundError:
    timed_high_score = 0
init_time_high_score = timed_high_score

run = False
current_game_mode = None

# UI - sounds
pygame.mixer.init()
move_sound = pygame.mixer.Sound('sounds/move.mp3')
mouse_click_sound = pygame.mixer.Sound('sounds/button_click.mp3')


# endregion VARIABLES

# region ADDITIONS

def play_sound(sound):
    pygame.mixer.Sound.play(sound)


# endregion ADDITIONS

# region DRAW FUNCTIONS
def draw_board(game_type='classic'):
    """
    Draw the board on the screen using the pygame.draw.rect function
    """
    pygame.draw.rect(screen, colors["bg"], board_rectangle_dimensions, board_border_width,
                     board_rectangle_border_radius)

    # Display scores
    if game_type == 'classic':
        score_text = font.render(f"Score: {score}", True, colors['dark_text'])
        high_score_text = font.render(f"High Score: {high_score}", True, colors['dark_text'])
        screen.blit(score_text, (10, 410))
        screen.blit(high_score_text, (10, 450))
    elif game_type == 'timed':
        score_text = font.render(f"Score: {timed_score}", True, colors['dark_text'])
        high_score_text = font.render(f"High Score: {timed_high_score}", True, colors['dark_text'])
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


def draw_over(end_text="Game Over"):
    """
    Draw the game over screen
    Args:
        end_text: str -> text to display on the game over screen
    """
    pygame.draw.rect(screen, colors["other"], game_over_rect, board_border_width, board_rectangle_border_radius)
    game_over_text = font.render(end_text, True, colors["light_text"])
    press_enter_text = font.render("Press Enter to play again", True, colors["dark_text"])
    screen.blit(game_over_text, (130, 65))
    screen.blit(press_enter_text, (70, 105))


def draw_timer(remaining_time):
    """
    Display the remaining time on the game screen
    """
    minutes = int(remaining_time // 60)
    seconds = int(remaining_time % 60)
    time_text = font.render(f"Time: {minutes:02}:{seconds:02}", True, colors["light_text"])
    time_rect = time_text.get_rect(center=(window_width - 100, 30))
    pygame.draw.rect(screen, colors["bg"], time_rect.inflate(20, 10))
    screen.blit(time_text, time_rect)


# region DRAW BUTTONS
def draw_return_button():
    """
    Draw the return to menu button on the game screen
    """
    return_text = font.render("Return to Menu", True, colors["light_text"])
    return_button_rect = return_text.get_rect(center=(300, 470))
    pygame.draw.rect(screen, colors["bg"], return_button_rect.inflate(20, 10))
    screen.blit(return_text, return_button_rect)
    return return_button_rect


def draw_undo_button():
    """
        Draw the undo button on the game screen with the cooldown counter or with undo text
        Return:
            undo_rect: pygame.Rect -> rectangle of the undo button
    """
    if cooldown_counter == 0:
        undo_text_content = "Undo Move"
        undo_text_color = colors[2]
    else:
        undo_text_content = f"Cooldown: {cooldown_counter}"
        undo_text_color = colors[16]

    undo_text = font.render(undo_text_content, True, undo_text_color)
    undo_button_rect = undo_text.get_rect(center=(300, 430))
    pygame.draw.rect(screen, colors["bg"], undo_button_rect.inflate(20, 10))  # Background for button
    screen.blit(undo_text, undo_button_rect)
    return undo_button_rect


# endregion DRAW BUTTONS
# endregion DRAW FUNCTIONS

# region GAME LOGIC FUNCTIONS

def spawn_piece(board):
    """
    Spawn a new piece on the board per function call and checks if the game is over
    Args:
        board: list -> values of the board
    """
    # only one new piece per function call
    count = 0
    # spawn a new piece on the board randomly
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


def return_one_move():
    """
    Return one move back in the game by popping the last state from the previous_states list
    Return:
        bool -> True if the move is undone, False otherwise
    """
    global board_values, previous_states, cooldown_counter
    if previous_states and cooldown_counter == 0:
        board_values = previous_states.pop()
        cooldown_counter = 10
        return True
    return False


def reset_game_data():
    """
    Restart the game -> resets game values
    """
    global board_values, spawn_new, init_pieces_count, score, direction, game_over, cooldown_counter, previous_states

    board_values = [[0 for _ in range(4)] for _ in range(4)]
    spawn_new = True
    score = 0
    direction = ''
    game_over = False
    cooldown_counter = 10
    previous_states = []


def reset_timed_game_data():
    """
    Restart the timed game -> resets game values + timed game values
    """
    global start_time, timed_score

    reset_game_data()
    timed_score = 0
    start_time = pygame.time.get_ticks()


# endregion GAME LOGIC FUNCTIONS

# region MOVE FUNCTIONS
def move_board(board, move_direction, game_type='classic'):
    """
    Move the board in the given direction
    Args:
        board: list -> values of the board
        move_direction: str -> direction of the move
        game_type: str -> type of the game (classic or timed)
    """
    global score, previous_states, cooldown_counter, timed_score, cooldown_counter

    # Save the previous state of the board if return is available
    if cooldown_counter == 0:
        previous_states.append([row[:] for row in board])
    else:
        cooldown_counter = max(0, cooldown_counter - 1)

    play_sound(move_sound)

    if game_type == 'classic':
        if move_direction == "UP":
            board, score = move_up(board, score)
        elif move_direction == "DOWN":
            board, score = move_down(board, score)
        elif move_direction == "LEFT":
            board, score = move_left(board, score)
        elif move_direction == "RIGHT":
            board, score = move_right(board, score)
        return board
    elif game_type == 'timed':
        if move_direction == "UP":
            board, timed_score = move_up(board, timed_score)
        elif move_direction == "DOWN":
            board, timed_score = move_down(board, timed_score)
        elif move_direction == "LEFT":
            board, timed_score = move_left(board, timed_score)
        elif move_direction == "RIGHT":
            board, timed_score = move_right(board, timed_score)
        return board


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
        # merge tiles
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
        merged_row += [0] * (size - len(merged_row))
        board[row] = merged_row[::-1]
    return board, global_score


# endregion MOVE FUNCTIONS

# region MAIN MENU
def main_menu():
    """
    Draw the main menu of the game with the start, timed mode, tutorial, and exit buttons
    """
    global current_game_mode

    menu = True
    while menu:
        screen.fill(colors["screen_color"])
        title = font.render("2048 Game", True, colors["dark_text"])
        title_rect = title.get_rect(center=(window_width / 2, 100))
        screen.blit(title, title_rect)

        # Start Classic Game
        start_game_text = font.render("Classic Mode", True, colors["dark_text"])
        start_game_rect = start_game_text.get_rect(center=(window_width / 2, 200))
        screen.blit(start_game_text, start_game_rect)

        # Start Timed Game
        timed_game_text = font.render("Timed Mode", True, colors["dark_text"])
        timed_game_rect = timed_game_text.get_rect(center=(window_width / 2, 250))
        screen.blit(timed_game_text, timed_game_rect)

        # Display Tutorial
        tutorial_text = font.render("Tutorial", True, colors["dark_text"])
        tutorial_rect = tutorial_text.get_rect(center=(window_width / 2, 300))
        screen.blit(tutorial_text, tutorial_rect)

        # Exit Game
        exit_game_text = font.render("Exit Game", True, colors["dark_text"])
        exit_game_rect = exit_game_text.get_rect(center=(window_width / 2, 350))
        screen.blit(exit_game_text, exit_game_rect)

        pygame.display.flip()

        # Handle all user input events in menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None, False
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_sound(mouse_click_sound)
                mouse_pos = event.pos
                new_mode = None
                if start_game_rect.collidepoint(mouse_pos):
                    new_mode = 'classic'
                elif timed_game_rect.collidepoint(mouse_pos):
                    new_mode = 'timed'
                elif tutorial_rect.collidepoint(mouse_pos):
                    show_tutorial()
                elif exit_game_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    return None, False

                if new_mode:
                    mode_changed = (new_mode != current_game_mode)
                    current_game_mode = new_mode
                    return new_mode, mode_changed

        timer.tick(fps)

    return False, False


def return_to_menu():
    return main_menu()


def show_tutorial():
    """
    Display the tutorial screen and the instructions on how to play the game
    """
    tutorial_running = True
    while tutorial_running:
        screen.fill(colors["screen_color"])
        instructions = [
            "How to Play 2048:",
            "Use your arrow keys to move the tiles.",
            "Tiles with the same number merge into one when they touch.",
            "Add them up to reach 2048! AND BEYOND!"
        ]

        y_offset = 150
        tutorial_font = pygame.font.SysFont('Arial', 15)
        for line in instructions:
            instruction_text = tutorial_font.render(line, True, colors["dark_text"])
            instruction_rect = instruction_text.get_rect(center=(window_width / 2, y_offset))
            screen.blit(instruction_text, instruction_rect)
            y_offset += 50

        # Back Button
        back_text = font.render("Back to Menu", True, colors["dark_text"])
        back_rect = back_text.get_rect(center=(window_width / 2, 400))
        screen.blit(back_text, back_rect)

        pygame.display.flip()
        for menu_event in pygame.event.get():
            if menu_event.type == pygame.QUIT:
                tutorial_running = False
            elif menu_event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(menu_event.pos):
                    tutorial_running = False

        timer.tick(fps)


# endregion MAIN MENU

# region GAME HANDLERS

def handle_game_events(game_type='classic'):
    """
    Check the game events and handle them correctly based on the game type
    Args:
        game_type: str -> type of the game (classic or timed)
    """
    global run, direction, spawn_new, game_over, cooldown_counter

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            play_sound(mouse_click_sound)
            handle_mouse_button(event)

        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_RETURN:
                if game_type == 'classic':
                    reset_game_data()
                elif game_type == 'timed':
                    reset_timed_game_data()
                game_over = False

        elif event.type == pygame.KEYUP:
            handle_key_press(event)


def handle_mouse_button(mouse_button_event):
    """
    Handle the mouse button events for the game
    Args:
        mouse_button_event: pygame.event -> key press event on which the function decides what to do next
    """
    global run

    if return_rect.collidepoint(mouse_button_event.pos):
        run = False

    if undo_rect.collidepoint(mouse_button_event.pos) and cooldown_counter == 0:
        return_one_move()


def handle_key_press(key_press_event):
    """
    Handle the key press events for the game
    Args:
        key_press_event: pygame.event -> key press event on which the function decides what to do next
    """
    global direction, game_over, run

    if key_press_event.key == pygame.K_ESCAPE:
        run = False

    if not game_over:
        if key_press_event.key == pygame.K_UP:
            direction = "UP"
        elif key_press_event.key == pygame.K_DOWN:
            direction = "DOWN"
        elif key_press_event.key == pygame.K_LEFT:
            direction = "LEFT"
        elif key_press_event.key == pygame.K_RIGHT:
            direction = "RIGHT"


# endregion GAME EVENT HANDLERS

# region GAME MODS
def classic_game_loop():
    """
    Main game loop for the classic mode
    """
    global run, spawn_new, direction, game_over, board_values, init_pieces_count, score, high_score, init_high_score, \
        return_rect, undo_rect, cooldown_counter
    while run:
        timer.tick(fps)
        screen.fill(colors["screen_color"])

        # Draw the return and undo buttons
        return_rect = draw_return_button()
        undo_rect = draw_undo_button()

        # Draw the board and pieces
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

        handle_game_events()

        # Draw the game over screen and update the high score file
        if game_over:
            draw_over()
            if high_score > init_high_score:
                with open('score_files/high_score.txt', 'w') as highscore_file:
                    highscore_file.write(str(high_score))
            init_high_score = high_score

        if score > high_score:
            high_score = score

        pygame.display.flip()


def timed_game_loop():
    global run, spawn_new, direction, game_over, board_values, init_pieces_count, timed_score, timed_high_score, \
        init_time_high_score, return_rect, undo_rect, start_time, cooldown_counter

    time_limit = 300  # seconds
    start_time = pygame.time.get_ticks()

    while run:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000  # convert milliseconds to seconds
        remaining_time = max(time_limit - elapsed_time, 0)

        timer.tick(fps)
        screen.fill(colors["screen_color"])

        # Draw the return and undo buttons
        return_rect = draw_return_button()
        undo_rect = draw_undo_button()

        # Draw the board and pieces
        draw_board('timed')
        draw_pieces(board_values)
        draw_timer(remaining_time)

        if spawn_new or init_pieces_count < 2:
            board_values, game_over = spawn_piece(board_values)
            spawn_new = False
            init_pieces_count += 1

        if direction != '':
            board_values = move_board(board_values, direction, 'timed')
            direction = ''
            spawn_new = True

        handle_game_events('timed')

        # Check if a new timed high score is achieved
        if timed_score > timed_high_score:
            timed_high_score = timed_score
            with open('score_files/timed_high_score.txt', 'w') as timed_highscore_file:
                timed_highscore_file.write(str(timed_high_score))

        # Draw the game over screen
        if remaining_time <= 0 or game_over:
            game_over = True
            draw_over("Time's Up!" if remaining_time <= 0 else "Game Over")

        pygame.display.flip()


# endregion GAME MODS

# region GAME LOOP
def main():
    """
    Run the main menu and the game loop based on the user's choice
    """
    global run
    run, mode_changed = main_menu()
    while run is not None and run is not False:
        if mode_changed:
            if run == 'classic':
                reset_game_data()
                classic_game_loop()
            elif run == 'timed':
                reset_timed_game_data()
                timed_game_loop()
        else:
            if run == 'classic':
                classic_game_loop()
            elif run == 'timed':
                timed_game_loop()

        run, mode_changed = main_menu()


if __name__ == "__main__":
    main()

# endregion GAME LOOP

pygame.quit()
