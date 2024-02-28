import pygame
import sys
import csv
import random

# Define word_list globally
word_list = []

# Step 1: Load the Word List
def load_word_list(file_path):
    global word_list  # Use the global word_list variable
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        word_list = [row[0] for row in reader]
    return word_list

# Modify Step 2: Select a Target Word
def select_target_word(word_list):
    return random.choice(word_list)

# Function to handle the game logic
def play_wordle():
    # Initialize Pygame
    pygame.init()

    # Define constants
    SCREEN_WIDTH = 400
    SCREEN_HEIGHT = 400
    WHITE = (255, 255, 255)
    GRAY = (200, 200, 200)
    GREEN = (97, 139, 85)
    YELLOW = (178, 159, 77)
    TILE_SIZE = 50
    GRID_WIDTH = 5
    GRID_HEIGHT = 6
    MARGIN = 10

    # Calculate the total width and height of the game board
    board_width = GRID_WIDTH * (TILE_SIZE + MARGIN) - MARGIN
    board_height = GRID_HEIGHT * (TILE_SIZE + MARGIN) - MARGIN

    # Calculate the position of the top-left corner of the game board to center it on the screen
    board_x = (SCREEN_WIDTH - board_width) // 2
    board_y = (SCREEN_HEIGHT - board_height) // 2

    # Set up the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Wordle Clone')

    # Function to draw the game board
    def draw_game_board(word_guess):
        screen.fill(WHITE)  # Fill the screen with white
        for row in range(GRID_HEIGHT):
            for col in range(GRID_WIDTH):
                pygame.draw.rect(screen, GRAY, (board_x + col * (TILE_SIZE + MARGIN), 
                                                board_y + row * (TILE_SIZE + MARGIN), 
                                                TILE_SIZE, TILE_SIZE))
                font = pygame.font.Font(None, 36)
                if word_guess[row][col] != '':
                    text_surface = font.render(word_guess[row][col], True, (0, 0, 0))
                    screen.blit(text_surface, (board_x + col * (TILE_SIZE + MARGIN) + TILE_SIZE / 2 - text_surface.get_width() / 2,
                                                board_y + row * (TILE_SIZE + MARGIN) + TILE_SIZE / 2 - text_surface.get_height() / 2))

    word_list = load_word_list('valid-words.csv')
    target_word = select_target_word(word_list)

    print(target_word)
    # Main game loop
    running = True
    word_guess = [['' for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]  # Initialize the word guess grid
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Construct the guessed word
                    guessed_word = ''
                    for row in range(GRID_HEIGHT):
                        for col in range(GRID_WIDTH):
                            guessed_word += word_guess[row][col]
                    guessed_word = guessed_word.strip().lower()  # Remove any leading or trailing whitespace and convert to lowercase
                    
                    # Check if the word is 5 letters
                    if len(guessed_word) != 5:
                        print("Must be a five-letter word")
                        break
                    
                    # Check if the word is valid
                    if guessed_word in word_list:
                        print("Guess is in word_list")
                        # Check each letter in the guessed word and update the colors of the tiles accordingly
                        for row in range(GRID_HEIGHT):
                            for col, letter in enumerate(guessed_word):
                                # Initialize color variable
                                color = None
                                if letter == target_word[col]:
                                    # Turn the tile green if the letter is in the right slot
                                    color = GREEN
                                elif letter in target_word:
                                    # Turn the tile yellow if the letter is in the target word but not in the right slot
                                    color = YELLOW
                                else:
                                    # Leave the tile gray if the letter is not in the target word at all
                                    color = GRAY
                                # Update the color of the corresponding tile
                                pygame.draw.rect(screen, color, (board_x + col * (TILE_SIZE + MARGIN), board_y + row * (TILE_SIZE + MARGIN), TILE_SIZE, TILE_SIZE))
                        pygame.display.flip()  # Update the display after setting tile colors
                    else:
                        print("Sorry, the word", guessed_word, "is not valid.")

                # Handle backspace to delete a letter
                elif event.key == pygame.K_BACKSPACE:
                    for row in range(GRID_HEIGHT):
                        for col in range(GRID_WIDTH - 1, -1, -1):  # Iterate through columns in reverse order
                            if word_guess[row][col] != '':
                                word_guess[row][col] = ''
                                draw_game_board(word_guess)
                                pygame.display.flip()
                                break
                        else:
                            continue
                        break
                # Handle typing to input letters
                else:
                    for row in range(GRID_HEIGHT):
                        for col in range(GRID_WIDTH):
                            if word_guess[row][col] == '':
                                word_guess[row][col] = event.unicode.upper()
                                draw_game_board(word_guess)
                                pygame.display.flip()
                                break
                        else:
                            continue
                        break

        # Draw the game board
        draw_game_board(word_guess)
        
        # Update the display
        pygame.display.flip()

    # Quit Pygame
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    play_wordle()
