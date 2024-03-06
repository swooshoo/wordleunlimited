import pygame
import sys
import csv
import random

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 463
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

# Set up the screen and logo
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Wordle Unlimited')
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Define variables for message display
display_message = None
message_duration = 420  # Duration in frames (assuming 60 frames per second)

# Messages for when the guess matches the target word
success_messages = ["Nicely done.", "YIPPEE!", "Exemplary.", "BINGPOT!", "Damn straight."]

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
        # Define guess_word outside the event handling block
        guess_word = ''.join(guess)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Handle key presses here
                if event.key == pygame.K_RETURN:
                    # Check if the guess is valid
                    if guess_word in word_list:
                        # Check if the guess is correct
                        if guess_word == target_word:
                            display_message = random.choice(success_messages)
                            current_attempt = attempts + 1  # End the current play
                        else:
                            # Handle incorrect guess
                            guesses.append(guess)
                            current_attempt += 1
                            guess = ['' for _ in range(5)]  # Reset the guess 
                    else:   
                        display_message = "Invalid word"
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

        # Draw message below the grid
        if display_message:
            message_text = FONT.render(display_message, True, WHITE)
            screen.blit(message_text, (SCREEN_WIDTH // 2 - message_text.get_width() // 2, SCREEN_HEIGHT - message_text.get_height() - 10))
            message_duration -= 1
            if message_duration <= 0:
                display_message = None
                message_duration = 420  # Reset message duration

        pygame.display.flip()
    # If all attempts are used and word is not guessed correctly
    if current_attempt > attempts and guess_word != target_word:
        display_message = f"Word was {target_word}"
        
pygame.quit()
sys.exit()