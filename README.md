# User Documentation for 2048 Game

## Introduction
Welcome to the 2048 Game, a fun and engaging puzzle game where you combine tiles with the same numbers to achieve a high score. This guide will help you understand how to play the game, navigate through different modes, and use available features.

## Getting Started

### Installation
Ensure you have Python and Pygame installed on your computer. Follow these steps to start the game:
1. Install Python from [python.org](https://python.org).
2. Install Pygame by running `pip install pygame` in your command prompt or terminal.
3. Download and extract the game files from the provided repository.
4. Run the game script using `python 2048_game.py`.

### Main Menu
When you start the game, you will be presented with the main menu options:
- **Classic Mode**: Start the game in classic mode without time constraints.
- **Timed Mode**: Challenge yourself in a 3-minute timed game session.
- **Tutorial**: Learn how to play 2048.
- **Settings**: Adjust game settings like theme and sound.
- **Exit Game**: Exit the game.

## Gameplay

### Controls
- **Arrow Keys**: Use the arrow keys to slide the tiles across the board.
- **Enter**: Restart the game after a game over.
- **ESC**: Return to the main menu during gameplay.

### Game Modes
- **Classic Mode**: Play as long as you want, trying to beat your high score.
- **Timed Mode**: You have 180 seconds to make as many points as possible.

### Scoring
Combine tiles to increase your score. Each merge adds the combined value to your score.

## Settings
Change the game's appearance and sound in the settings menu:
- **Theme**: Choose between Basic, Dark, Classic, and Retro themes.
- **Sound**: Toggle sound effects on or off.

## Tips for High Scores
- Plan your moves ahead.
- Try to keep your highest value tile in a corner.
- Focus on combining smaller tiles to create room for new tiles.

Enjoy your game, and try to reach 2048!




---

# Technical Documentation for 2048 Game

## Overview
This document details the technical aspects of the 2048 game implemented in Python using the Pygame library. It covers the game's structure, main modules, and core functionalities.

## System Requirements
- Python 3.x
- Pygame library

## Modules and Libraries
The game uses the Pygame library for rendering the game interface and handling user interactions. Key Python modules used include:
- `pygame`: For game graphics and events.
- `random`: For spawning new tiles at random positions.
- `json`: For saving and loading game state.

## Game Architecture
The game is structured into several parts:

### Main Loop
The game's entry point is the `main()` function, which initializes the game and manages the game loop.

### Game Initialization
- Load configurations and set up the game window.
- Initialize game states such as the board configuration and scores.

### Game Modes
- **Classic Mode**: Manage the game logic without time constraints.
- **Timed Mode**: Introduce a timer and manage game state transitions based on time.

### Event Handling
- Keyboard inputs for tile movement.
- Mouse inputs for navigating menus and buttons.

### Rendering
- Draw the game board, tiles, and UI elements based on the current state.
- Update the display to reflect changes.

### Saving and Loading
- Use JSON files to save the high scores and board state.
- Load existing state at game start-up to resume previous sessions.

## File Structure
- `2048_game.py`: Main game script containing all game logic and UI rendering.
- `assets/`: Directory containing sound effects and save files.

## Extending the Game
To add new features or modify existing ones:
1. Clone the repository.
2. Navigate to the game script.
3. Make changes to add features like new game modes or improved AI.
4. Test the changes thoroughly before deployment.

## Conclusion
This documentation provides a technical snapshot of the 2048 game implementation. For detailed insights into the code, refer to the inline comments in the `2048_game.py` script.
