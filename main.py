"""
main.py

Solitaire Game Main Script with PEP 8 Documentation Style

Author: Chiriac Laura-Florina
Created: 22-12-2024
"""

# Third-party Library Imports
import pygame

# Local Imports
from deck import Deck

# Initialize Pygame
pygame.init()

# Define CONSTANTS
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800
display_dimensions = (SCREEN_WIDTH, SCREEN_HEIGHT)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Solitaire')

# Loading background image for main menu
background_image = pygame.image.load('resources/images/photorealistic-casino-lifestyle.jpg')
background_image_game = pygame.image.load('resources/images/green_background.png')

# Setting frame rate
clock = pygame.time.Clock()
FPS = 60

# Game states
MAIN_MENU = 'main_menu'
GAME = 'game'
current_state = MAIN_MENU

# Play button surface with per-pixel alpha
play_button_surface = pygame.Surface((200, 70), pygame.SRCALPHA)
play_button_rect = play_button_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))
play_button = pygame.Rect(play_button_rect.topleft, play_button_rect.size)

# Quit button surface with per-pixel alpha
quit_button_surface = pygame.Surface((200, 70), pygame.SRCALPHA)
quit_button_rect = quit_button_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 230))
quit_button = pygame.Rect(quit_button_rect.topleft, quit_button_rect.size)

# Create an undo button surface
undo_button_surface = pygame.Surface((100, 70), pygame.SRCALPHA)
undo_button_rect = undo_button_surface.get_rect(center=(SCREEN_WIDTH // 2 - 600, SCREEN_HEIGHT // 2 - 300))
undo_button = pygame.Rect(undo_button_rect.topleft, undo_button_rect.size)

# Create a new game button surface
new_game_button_surface = pygame.Surface((150, 50), pygame.SRCALPHA)
new_game_button_rect = new_game_button_surface.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20))
new_game_button = pygame.Rect(new_game_button_rect.topleft, new_game_button_rect.size)

# Create a hint button surface
hint_button_surface = pygame.Surface((100, 50), pygame.SRCALPHA)
hint_button_rect = hint_button_surface.get_rect(bottomright=(SCREEN_WIDTH - 20, SCREEN_HEIGHT - 80))
hint_button = pygame.Rect(hint_button_rect.topleft, hint_button_rect.size)

# Colors
border_color = (255, 255, 255)
text_color = (255, 255, 255)
hover_color = (50, 50, 50, 118)

# Fonts
font = pygame.font.Font(None, 70)
title_font = pygame.font.Font(None, 170)

# Start Menu
def main_menu():
    """Displays the main menu and handles events for the menu.

    This includes the background, the play button, and the quit button, as well as handling events for the buttons.
    """
    screen.blit(background_image, (0, 0))

    # Main Menu elements
    mouse_pos = pygame.mouse.get_pos()

    # Add title text
    title_text = title_font.render('Solitaire', True, text_color)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 330))  # Lower y-coordinate centered

    # Play button
    if play_button_rect.collidepoint(mouse_pos):
        play_button_surface.fill(hover_color)
    else:
        play_button_surface.fill((0, 0, 0, 50))  # Fill with transparent color

    pygame.draw.rect(play_button_surface, border_color, play_button_surface.get_rect(), 2)  # Draw the border

    # Render the text
    text = font.render('Play', True, text_color)
    play_button_surface.blit(text, (50, 10))

    # Draw the button
    screen.blit(play_button_surface, play_button_rect.topleft)

    # Quit button
    if quit_button_rect.collidepoint(mouse_pos):
        quit_button_surface.fill(hover_color)
    else:
        quit_button_surface.fill((0, 0, 0, 50))  # Fill with transparent color
    pygame.draw.rect(quit_button_surface, border_color, quit_button_surface.get_rect(), 2)  # Draw the border

    # Render the text
    text = font.render('Quit', True, text_color)
    quit_button_surface.blit(text, (50, 10))

    # Draw the button
    screen.blit(quit_button_surface, quit_button_rect.topleft)

    # Main menu logic : for buttons and text
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            if play_button.collidepoint(ev.pos):
                global current_state
                current_state = GAME
            elif quit_button.collidepoint(ev.pos):
                return False
    return True

# Create the deck
card_size = (100, 150)

# Load card images and resize them to fit in game
def load_and_resize_image(path, size):
    """
    Loads and resizes an image to the specified size.

    Args:
        path (str): The path to the image file.
        size (tuple): The desired size of the image.

    Returns:
        pygame.transform: The resized image.

    Raises:
        FileNotFoundError: If the image file is not found.
    """
    try:
        image = pygame.image.load(path)
    except pygame.error:
        raise FileNotFoundError(f"Card image not found at: {path}")
    return pygame.transform.scale(image, size)

# Load card images
card_images = {
    'hearts': {rank: load_and_resize_image(f'resources/images/cards/{rank}_of_hearts.png', card_size) for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']},
    'diamonds': {rank: load_and_resize_image(f'resources/images/cards/{rank}_of_diamonds.png', card_size) for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']},
    'clubs': {rank: load_and_resize_image(f'resources/images/cards/{rank}_of_clubs.png', card_size) for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']},
    'spades': {rank: load_and_resize_image(f'resources/images/cards/{rank}_of_spades.png', card_size) for rank in ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']},
    'card_back': load_and_resize_image('resources/images/cards/card_back.png', card_size)
}

# Create the deck object
deck = Deck((0,0), card_images, card_size)

# Put the stacks in the correct position on the screen
deck.setup_stacks(display_dimensions)

# Game Board
def game_board():
    """
    Displays the game board and handles events for the game.

    This function handles the drawing of the game board, piles, and initial cards, as well as the undo, new game, and hint buttons.
    """

    # Define rectangles for the four card places and the Stock Pile
    card_places = [
        pygame.Rect((200, 50, 100, 150)),  # Stock card place
        pygame.Rect((350, 50, 100, 150)),  # Second stock card place

        pygame.Rect((650, 50, 100, 150)),  # First ace card place
        pygame.Rect((800, 50, 100, 150)),  # Second ace card place
        pygame.Rect((950, 50, 100, 150)),
        pygame.Rect((1100, 50, 100, 150)),

        # Card places for the table stacks
        pygame.Rect((200, 250, 100, 150)),  # First table stack
        pygame.Rect((350, 250, 100, 150)),  # Second table stack
        pygame.Rect((500, 250, 100, 150)),
        pygame.Rect((650, 250, 100, 150)),
        pygame.Rect((800, 250, 100, 150)),
        pygame.Rect((950, 250, 100, 150)),
        pygame.Rect((1100, 250, 100, 150))

    ]

    # Colors
    card_place_color = (255, 255, 255)  # White color for card places

    # Draw card places
    for rect in card_places:
        pygame.draw.rect(screen, card_place_color, rect, 2, border_radius=10)  # Draw the border

    # Draw undo button
    undo_hover_color = (50, 50, 50, 118)  # Hover color for button
    undo_text_font = pygame.font.Font(None, 40)

    if undo_button_rect.collidepoint(pygame.mouse.get_pos()):
        undo_button_surface.fill(undo_hover_color) # Fill with hover color
    else:
        undo_button_surface.fill((0, 0, 0, 50)) # Fill with transparent color
    pygame.draw.rect(undo_button_surface, border_color, undo_button_surface.get_rect(), 2) # Draw the border

    # Fix button text
    text = undo_text_font.render('Undo', True, text_color)
    text_rect = text.get_rect(center=(undo_button_surface.get_width() // 2, undo_button_surface.get_height() // 2))

    undo_button_surface.blit(text, text_rect.topleft)
    screen.blit(undo_button_surface, undo_button_rect.topleft)

    # Draw new game button
    new_game_text_font = pygame.font.Font(None, 30)
    if new_game_button_rect.collidepoint(pygame.mouse.get_pos()):
        new_game_button_surface.fill(undo_hover_color)  # Fill with hover color
    else:
        new_game_button_surface.fill((0, 0, 0, 50))  # Fill with transparent color
    pygame.draw.rect(new_game_button_surface, border_color, new_game_button_surface.get_rect(), 2)  # Draw the border

    # Render button text
    text = new_game_text_font.render('New Game', True, text_color)
    text_rect = text.get_rect(
        center=(new_game_button_surface.get_width() // 2, new_game_button_surface.get_height() // 2))

    new_game_button_surface.blit(text, text_rect.topleft)
    screen.blit(new_game_button_surface, new_game_button_rect.topleft)

    # Draw hint button
    hint_text_font = pygame.font.Font(None, 30)  # Smaller font size
    if hint_button_rect.collidepoint(pygame.mouse.get_pos()):
        hint_button_surface.fill(undo_hover_color)  # Fill with hover color
    else:
        hint_button_surface.fill((0, 0, 0, 50))  # Fill with transparent color
    pygame.draw.rect(hint_button_surface, border_color, hint_button_surface.get_rect(), 2)  # Draw the border

    # Render button text
    text = hint_text_font.render('Hint', True, text_color)
    text_rect = text.get_rect(
        center=(hint_button_surface.get_width() // 2, hint_button_surface.get_height() // 2))

    hint_button_surface.blit(text, text_rect.topleft)
    screen.blit(hint_button_surface, hint_button_rect.topleft)

def win_screen(screen, duration=5):
    """Display a win screen for a specified duration.

    Args:
        screen (pygame.Surface): The Pygame surface where the win screen will be displayed.
        duration (int): The duration to display the win screen, in seconds. Defaults to 5.

    Returns:
        None
    """
    screen.blit(background_image_game, (0, 0))
    win_font = pygame.font.Font(None, 100)
    text = win_font.render('You Win!', True, (255, 255, 255))
    screen_width, screen_height = screen.get_size()
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(duration * 1000)  # Wait for the specified duration in milliseconds

# Game function
def game():
    """Displays the game board and handles events for the game.

    This function handles the overall game logic: drawing the board, drawing the cards, and then handling occuring events."""
    screen.blit(background_image_game, (0, 0))
    game_board()
    deck.draw(screen)
    handle_events(deck)
    if deck.check_win():
        print("You won!")
        # Clear the screen and put a new win screen
        win_screen(screen)
        deck.reset_all(display_dimensions)
        return False
    return True

# Handle events function for adding the game logic to the game
def handle_events(deck):
    """Handles the events for the game such as clicks on game buttons, drag-and-drop for cards, quitting action.

    Args:
        deck (Deck): The deck object for the game.

    Returns:
        None
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_position = pygame.mouse.get_pos()
            if undo_button.collidepoint(mouse_position):
                deck.undo_last_move()
            if new_game_button.collidepoint(mouse_position):
                deck.reset_all(display_dimensions)
            if hint_button.collidepoint(mouse_position):
                deck.show_hint()
            if deck.stock_stack.rect.collidepoint(mouse_position):
                deck.check_for_stock_click(mouse_position)
            for stack in deck.stacks:
                for card in stack.cards[::-1]:
                    if card.check_if_clicked(mouse_position):
                        draggable_stack = card.get_draggable_stack()
                        for c in draggable_stack:
                            c.start_drag(mouse_position)
                        deck.dragged_cards = draggable_stack
                        stack.remove_cards(draggable_stack)
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if deck.dragged_cards:
                deck.stop_dragging()
                for card in deck.dragged_cards:
                    card.stop_drag()
                deck.dragged_cards = None
        elif event.type == pygame.MOUSEMOTION:
            if deck.dragged_cards:
                for card in deck.dragged_cards:
                    card.update_position(pygame.mouse.get_pos())

# Main run loop
run = True
while run:
    clock.tick(FPS) # Set the frame rate
    if current_state == MAIN_MENU:
        run = main_menu() # Run the main menu
    elif current_state == GAME:
        run = game() # Run the game
    pygame.display.flip() # Update the display

pygame.quit() # Quit game after the loop ends