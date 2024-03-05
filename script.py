import pygame
import sys
import csv
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (18, 18, 19)
WHITE = (216, 218, 220)
RED = (255, 0, 0)
YELLOW = (178, 159, 77)
GREEN = (97, 139, 85)
GRAY = (58, 58, 60)
FONT_SIZE = 40
FONT_COLOR = WHITE
FONT = pygame.font.Font(None, FONT_SIZE)
WORD_LIST_FILE = "valid-words.csv"

# Load the word list
word_list = []

def load_word_list(file_path):
    global word_list
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        word_list = [row[0].strip().upper() for row in reader]

load_word_list(WORD_LIST_FILE)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wordle Unlimited')

# Function to draw the game board
def draw_game_board(guesses, guess, current_attempt, target_word, letter_color):
    screen.fill(BLACK)

    # Draw grid
    tile_size = 80
    margin = 10
    grid_width = 5
    grid_height = 6
    for row in range(grid_height):
        for col in range(grid_width):
            pygame.draw.rect(screen, GRAY, (margin + col * (tile_size + margin), margin + row * (tile_size + margin), tile_size, tile_size), 2)

    # Draw guesses
    for i, word in enumerate(guesses):
        for j, letter in enumerate(word):
            color = WHITE
            if letter in target_word:
                if letter == target_word[j]:
                    color = GREEN  # Correct letter
                else:
                    color = YELLOW  # Misplaced letter
            else:
                color = GRAY  # Incorrect letter
            pygame.draw.rect(screen, color, (margin + j * (tile_size + margin), margin + i * (tile_size + margin), tile_size, tile_size))
            letter_text = FONT.render(letter, True, letter_color)
            screen.blit(letter_text, (margin + j * (tile_size + margin) + tile_size // 2 - letter_text.get_width() // 2, margin + i * (tile_size + margin) + tile_size // 2 - letter_text.get_height() // 2))

    # Draw current guess
    if guess:
        for j, letter in enumerate(guess):
            if letter:
                color = GRAY
                letter_text = FONT.render(letter, True, letter_color)
                pygame.draw.rect(screen, color, (margin + j * (tile_size + margin), margin + (current_attempt - 1) * (tile_size + margin), tile_size, tile_size))
                screen.blit(letter_text, (margin + j * (tile_size + margin) + tile_size // 2 - letter_text.get_width() // 2, margin + (current_attempt - 1) * (tile_size + margin) + tile_size // 2 - letter_text.get_height() // 2))

    # Draw attempts left
    attempts_text = FONT.render(f"Attempts Left: {attempts - current_attempt + 1}", True, FONT_COLOR)
    attempts_text_rect = attempts_text.get_rect()
    attempts_text_rect.topright = (SCREEN_WIDTH - 20, SCREEN_HEIGHT // 2)
    screen.blit(attempts_text, attempts_text_rect)

# Main game loop
running = True
while running:
    # Select a new target word for each play
    target_word = random.choice(word_list)
    print("Target Word:", target_word)  # Print the target word in the terminal

    # Initialize game variables
    attempts = 6
    current_attempt = 1
    guesses = []
    guess = ['' for _ in range(5)]  # Define the guess variable

    while current_attempt <= attempts:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle key presses here
                if event.key == pygame.K_RETURN:
                    # Check if the guess is valid
                    guess_word = ''.join(guess)
                    if guess_word in word_list:
                        # Check if the guess is correct
                        if guess_word == target_word:
                            print("You guessed the word correctly!")
                            current_attempt = attempts + 1  # End the current play
                        else:
                            # Handle incorrect guess
                            guesses.append(guess)
                            current_attempt += 1
                            guess = ['' for _ in range(5)]  # Reset the guess
                elif event.key == pygame.K_BACKSPACE:
                    # Delete the last letter in the current guess
                    for i in range(len(guess) - 1, -1, -1):
                        if guess[i]:
                            guess[i] = ''
                            break
                elif event.key in range(pygame.K_a, pygame.K_z + 1):
                    # Add the pressed key to the guess
                    index = len([l for l in guess if l])  # Get the index of the next empty slot in the guess
                    if index < 5:
                        guess[index] = chr(event.key).upper()

        # Draw the game board with custom letter color (in this case, white)
        draw_game_board(guesses, guess, current_attempt, target_word, WHITE)
        pygame.display.flip()

pygame.quit()
sys.exit()
