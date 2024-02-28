import pygame
import sys
import csv
import random

# Step 1: Load the Word List
def load_word_list(file_path):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        word_list = [row[0] for row in reader]
    return word_list

# Modify Step 2: Select a Target Word
def select_target_word(word_list):
    return random.choice(word_list)

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
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
                # Check if the word is valid
                guessed_word = ''.join([''.join(row) for row in word_guess])
                if guessed_word in word_list:
                    print("Congratulations! You guessed the word correctly:", guessed_word)
                else:
                    print("Sorry, the word", guessed_word, "is not valid.")
            elif event.key == pygame.K_BACKSPACE:
                # Handle backspace to delete a letter
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
            else:
                # Handle typing to input letters
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
