import pygame
import sys

def display_settings():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Settings")

    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    settings_file = "settings.txt"

    font_path = "broken-console-broken-console-bold-700.ttf"  # Replace with the path to your font file
    font_size = 36
    font = pygame.font.Font(font_path, font_size)

    # Define colors
    white = (255, 255, 255)
    red = (235, 30, 41)
    black = (17, 34, 80)

    # Load Settings
    with open('settings.txt') as f:
        settings_data = [line for line in f]
        f.close()

    # List of valid difficulties
    difficulty_options = ['easy', 'normal', 'hard', 'advanced']

    # if settings data has invalid value for difficulty options, set it to normal
    try:
        if settings_data[1].lower().strip("\n") not in difficulty_options:

            # change the difficulty line to normal
            settings_data[1] = difficulty_options[1] + "\n"
            f = open(settings_file, 'w')
            f.writelines(settings_data)
            f.close()


    # if settings file is damaged (difficulty line out of index)
    # recover settings file
    except:
        with open('default_settings.txt') as f:

            # omit warning line from default_settings.txt
            settings_data = [line for line in f][1:]

            f = open(settings_file, 'w')

            f.close()

    # get difficulty from the stored settings
    difficulty = settings_data[1].strip()

    # find selected difficulty
    selected_difficulty = difficulty_options.index(difficulty)

    # initialize menu selection
    selected_option = 0

    running = True
    while running:

        # Define menu options
        settings_options = [("Difficulty: " + str(difficulty)), "save and return"]

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN: # menu navigation

                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(settings_options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(settings_options)
                # select
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:  # Difficulty
                        selected_difficulty = (selected_difficulty + 1) % len(difficulty_options)
                        difficulty = difficulty_options[selected_difficulty]

                    else: # Return

                        # save difficulty preferences to text file
                        settings_data[1] = difficulty + '\n'
                        f = open(settings_file, 'w')
                        f.writelines(settings_data)
                        f.close()
                        running = False

        # Draw background
        screen.blit(background, (0, 0))

        for i, option in enumerate(settings_options):
            text_color = white if i == selected_option else red
            text = font.render(option, True, text_color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))

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

if __name__ == "__main__":
    display_settings()

