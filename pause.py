import pygame
import sys

def pause_menu(screen, clock):
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    font_path = "broken-console-broken-console-bold-700.ttf"  # Replace with the path to your font file
    font_size = 36
    font = pygame.font.Font(font_path, font_size)

    pause_text = font.render("Paused", True, WHITE)
    pause_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    options = ["Resume", "Replay", "Return to Menu"]
    selected_option = 0

    option_rects = []
    for i, option in enumerate(options):
        option_text = font.render(option, True, WHITE)
        option_rect = option_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + i * 60))
        option_rects.append(option_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "resume"

                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)

                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)

                elif event.key == pygame.K_RETURN:
                    selected_option_text = options[selected_option]
                    if selected_option_text == "Resume":
                        return "resume"
                    elif selected_option_text == "Replay":
                        return "replay"
                    elif selected_option_text == "Return to Menu":
                        return "menu"

        screen.blit(background, (0, 0))

        screen.blit(pause_text, pause_rect)

        for i, option_rect in enumerate(option_rects):
            option_text = font.render(options[i], True, WHITE)
            screen.blit(option_text, option_rect)

            # Draw a border around the selected option
            if i == selected_option:
                pygame.draw.rect(screen, WHITE, option_rect, 2)

        pygame.display.flip()
        clock.tick(60)