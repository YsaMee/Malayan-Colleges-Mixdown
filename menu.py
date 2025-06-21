import pygame
from pygame import mixer
import os
from game import run_game
from credits import display_credits
from settings import display_settings

pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu")

# Load background image
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load background music
mixer.music.load("start menu.mp3")
mixer.music.play(-1)  # -1 plays the music in an infinite loop

# Load font
font_path = os.path.join(os.path.dirname(__file__), "broken-console-broken-console-bold-700.ttf")
font = pygame.font.Font(font_path, 36)

# Define colors
white = (255, 255, 255)
red = (235, 30, 41)
black = (17, 34, 80)

# Define menu options
menu_options = ["Start Game", "Settings", "Credits", "Exit Game"]
selected_option = 0

# Game Title
game_title = pygame.image.load("game logo.png").convert_alpha()
game_title = pygame.transform.scale(game_title, (600, 480))

# Fade parameters
fade_color = red
fade_alpha = 0
fade_speed = 5  # Adjust the fade speed as needed

# begin main menu loop
running = True
while running:
    # look for events
    for event in pygame.event.get():
        # quit
        if event.type == pygame.QUIT:
            running = False
        # menu navigation
        elif event.type == pygame.KEYDOWN:
            # menu navigation
            if event.key == pygame.K_DOWN:
                selected_option = (selected_option + 1) % len(menu_options)
            elif event.key == pygame.K_UP:
                selected_option = (selected_option - 1) % len(menu_options)
            # select
            elif event.key == pygame.K_RETURN:
                if selected_option == 0:  # Start Game

                    print("Starting the game!")

                    run_game()

                    # On return to menu from game, reload and play menu music
                    mixer.music.load("start menu.mp3")
                    mixer.music.play(-1)

                elif selected_option == 1:  # Settings
                    display_settings()

                elif selected_option == 2:  # Credits
                    display_credits()

                elif selected_option == 3:  # Exit Game
                    running = False

        pygame.display.set_caption("Menu")

    # Update fade color
    if selected_option == 0:
        fade_alpha = min(fade_alpha + fade_speed, 255)
    else:
        fade_alpha = max(fade_alpha - fade_speed, 0)
    fade_color = (255, 0, 0, fade_alpha)

    # Draw background
    screen.blit(background, (0, 0))

    # Draw title
    screen.blit(game_title, (100, -10))  # Adjust the position as needed

    # Draw menu options with fade effect
    for i, option in enumerate(menu_options):
        text_color = white if i == selected_option else fade_color
        text = font.render(option, True, text_color)
        text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2 + i * 60))

        # Draw border for menu options
        option_border = font.render(option, True, black)
        screen.blit(option_border, (text_rect.centerx - option_border.get_width() // 2 - 2,
                                    text_rect.centery - option_border.get_height() // 2 - 2))
        screen.blit(option_border, (text_rect.centerx - option_border.get_width() // 2 - 2,
                                    text_rect.centery - option_border.get_height() // 2 + 2))
        screen.blit(option_border, (text_rect.centerx - option_border.get_width() // 2 + 2,
                                    text_rect.centery - option_border.get_height() // 2 + 2))

        screen.blit(text, text_rect)

    pygame.display.flip()

# Quit Pygame and mixer
pygame.quit()
mixer.quit()
