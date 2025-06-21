import pygame
import sys

def display_credits():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Credits")

    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_path = "broken-console-broken-console-bold-700.ttf"  # Replace with the path to your font file
    font_size = 25
    font = pygame.font.Font(font_path, font_size)

    credits_text = [
        "CREDITS:",
        "",
        "Nick Arendain- game code",
        "Ram Monsendo- menu, uml",
        "Gwen Cañete- scoring, flowgorithm",
        "Jahna - base code, game logo, debugging",
        "",
        "Special thanks to:",
        "newvagabond - Pixel art of the MMCM building",
        "Labatorio - game music",
        "toby fox - start menu music",
        "artefak project - Broken Console font"
    ]

    button_text = "Return"
    button_font = pygame.font.Font(font_path, 36)
    button_color = (255, 0, 0)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT - 80, 100, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False

        # Draw background
        screen.blit(background, (0, 0))

        # Display credits text with black outline
        y_offset = 100
        for line in credits_text:
            text_surface = font.render(line, True, WHITE)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))

            # Create a black-outlined version of the text
            outline_surface = font.render(line, True, BLACK)
            outline_rect = outline_surface.get_rect(center=(text_rect.centerx + 2, text_rect.centery + 2))

            screen.blit(outline_surface, outline_rect)
            screen.blit(text_surface, text_rect)
            y_offset += font_size

        # Draw exit button with border
        button_text_surface = button_font.render(button_text, True, WHITE)
        button_text_rect = button_text_surface.get_rect(center=button_rect.center)

        # Draw border for exit button
        button_border = button_font.render(button_text, True, (17, 34, 80))
        screen.blit(button_border, (button_text_rect.centerx - button_border.get_width() // 2 - 2,
                                    button_text_rect.centery - button_border.get_height() // 2 - 2))
        screen.blit(button_border, (button_text_rect.centerx - button_border.get_width() // 2 - 2,
                                    button_text_rect.centery - button_border.get_height() // 2 + 2))
        screen.blit(button_border, (button_text_rect.centerx - button_border.get_width() // 2 + 2,
                                    button_text_rect.centery - button_border.get_height() // 2 + 2))

        screen.blit(button_text_surface, button_text_rect)

        pygame.display.flip()

if __name__ == "__main__":
    display_credits()
