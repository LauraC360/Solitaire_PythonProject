"""
main.py

Solitaire Game Main Script with PEP 8 Documentation Style

Author: Chiriac Laura-Florina
Created: 22-12-2024
"""

# Pygame Library
import pygame

# Initialize Pygame
pygame.init()

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Solitaire')

# Loading background image for main menu
background_image = pygame.image.load('resources/images/photorealistic-casino-lifestyle.jpg')
background_image_game = pygame.image.load('resources/images/green_background.png')

player = pygame.Rect((300, 250, 50, 50))

# Setting frame rate
clock = pygame.time.Clock()
FPS = 60

# Defining CONSTANTS
# Game states
MAIN_MENU = 'main_menu'
GAME = 'game'
current_state = MAIN_MENU

# Colors
border_color = (255, 255, 255)
text_color = (255, 255, 255)
hover_color = (50, 50, 50, 118)  # Semi-transparent hover color

# Fonts
font = pygame.font.Font(None, 70)
title_font = pygame.font.Font(None, 170)

# Start Menu
def main_menu():
    screen.blit(background_image, (0, 0))

    # Main Menu elements
    mouse_pos = pygame.mouse.get_pos()

    # Add title text
    title_text = title_font.render('Solitaire', True, text_color)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 330))  # Lower y-coordinate centered

    # Main menu logic : for buttons and text
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
    return True

# Main Game Screen
def game():
    screen.blit(background_image_game, (0, 0))

    # Game logic
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            return False
    return True


# Main loop
run = True
while run:

    # Set frame rate
    clock.tick(FPS)

    if current_state == MAIN_MENU:
        run = main_menu()
    elif current_state == GAME:
        run = game()

    pygame.display.update()

pygame.quit()