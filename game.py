import pygame
import sys
import random
from pygame import mixer
from pause import pause_menu


# Function to check if the music is still playing
def is_music_playing():
    return pygame.mixer.music.get_busy()


# Function for the game
def run_game():

    # Initializes pygame and mixer
    # Initializes pygame and mixer
    pygame.init()
    mixer.init()

    # Variable init - window
    SCREEN_WIDTH = 800  # default 800
    SCREEN_HEIGHT = 600  # default 600

    # Variable init - visual
    TILE_WIDTH = (SCREEN_WIDTH // 4)  # default 200
    TILE_HEIGHT = 100  # default 100
    CLICK_LINE_HEIGHT = 6  # default 60
    LINE_HEIGHT = 30  # default 30

    # Variable Init - difficulty & gameplay
        # get difficulty from settings
    with open('settings.txt') as f:
        difficulty = [line for line in f][1].strip()
        f.close()

    # Default values
    song = "malayan hymn.mp3"
    misses_to_fail = 10  # amount of tiles to miss to trigger fail
    TILE_SPEED = 6  # dspeed of tile going to bottom of screen from spawning
    NEW_TILE_INTERVAL = 60  # delay between new tiles being spawned

    if difficulty == 'easy': # easy
        misses_to_fail = 40
        TILE_SPEED = 6
        NEW_TILE_INTERVAL = 120
    elif difficulty == 'hard': # hard
        TILE_SPEED = 9
        NEW_TILE_INTERVAL = 40
    elif difficulty == 'advanced': #advanced
        song = "malayan hymn advanced.mp3"
        TILE_SPEED = 12
        NEW_TILE_INTERVAL = 20
    else: # normal (default)
        misses_to_fail = 10
        TILE_SPEED = 6
        NEW_TILE_INTERVAL = 60

    # Loads music
    mixer.music.load(song)
    mixer.music.play(1)

    # Variable init - gameplay

    # 60 = 60 bpm, 50 = 71 bpm,

    # Colours
    WHITE = (255, 255, 255)
    YELLOW = (250, 230, 0)
    ORANGE = (245, 104, 0)
    PINK = (250, 0, 138)
    PURPLE = (183, 0, 229)

    # Loads screen and puts window caption
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Malayan Colleges Mixdown")

    # Loads background image
    background = pygame.image.load("background.jpg").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    # Load game image
    gamebackground = pygame.image.load("gridbackground.jpg").convert()


    clock = pygame.time.Clock()

    # individual tile class
    class Tile:
        def __init__(self, x, color):
            self.x = x
            self.y = -TILE_HEIGHT  # height at which tiles will spawn, default -100
            self.speed = TILE_SPEED  # set speed
            self.color = color

        def move(self):
            self.y += self.speed  # move tile position downwards as defined by speed

        def draw(self):  # render the  tile at
            pygame.draw.rect(screen, self.color, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT/2), 0, 10)

    def create_tile():  # spawns a tile at a random column
        position = random.randint(0, 3)   # picks a random column
        column_colors = [YELLOW, ORANGE, PINK, PURPLE]
        tiles.append(Tile(position * TILE_WIDTH, column_colors[position]))  # adds a tile at chosen random column

        if random.randint(0,3) == 0: # 25% chance of generating a double note

            position = (position - 2) % 3 # find a new position that isn't the same as the previous one
            tiles.append(Tile(position * TILE_WIDTH, column_colors[position]))






    def draw_piano():
        column_colors = [YELLOW, ORANGE, PINK, PURPLE]  # assign colors for each column
        for i in range(4):  # render the piano at the bottom of the screen
            pygame.draw.rect(screen, column_colors[i],
                             (i * TILE_WIDTH, SCREEN_HEIGHT - LINE_HEIGHT, TILE_WIDTH, LINE_HEIGHT))
            pygame.draw.rect(screen, WHITE, (
                i * TILE_WIDTH, SCREEN_HEIGHT - LINE_HEIGHT - CLICK_LINE_HEIGHT, TILE_WIDTH, CLICK_LINE_HEIGHT))

    frame_count = 0

    score = 0

    tiles = []  # list of current tiles on the screen
    missed_tiles = 0
    score_increase = 10
    grade = ""
    game_over = False
    game_clear = False

    font = pygame.font.Font("broken-console-broken-console-bold-700.ttf", 32)

    sfx_volume = 1 # default 1, volume for sound effects

    global game_over_sound

    game_over_sound = mixer.Sound("gameover.mp3")
    game_over_sound.set_volume(sfx_volume)

    global scored_sound

    scored_sound = mixer.Sound("hitsound.mp3")
    scored_sound.set_volume(sfx_volume)

    global hit_notile_sound

    hit_notile_sound = mixer.Sound("hitsoundnotile.mp3")
    hit_notile_sound.set_volume(sfx_volume)


    global game_clear_sound
    game_clear_sound = mixer.Sound("clear.mp3")
    game_clear_sound.set_volume(sfx_volume)

    music_start_time = pygame.time.get_ticks()

    # on startup set pause state to False
    paused = False

    # Start game
    while True:
        # Fill the screen with black color
        screen.blit(gamebackground, (0, 0))

        draw_piano()

        # check for keyboard input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    score += hit_tile(0, tiles, TILE_HEIGHT, SCREEN_HEIGHT, TILE_WIDTH, score_increase)
                elif event.key == pygame.K_s:
                    score += hit_tile(1, tiles, TILE_HEIGHT, SCREEN_HEIGHT, TILE_WIDTH, score_increase)
                elif event.key == pygame.K_d:
                    score += hit_tile(2, tiles, TILE_HEIGHT, SCREEN_HEIGHT, TILE_WIDTH, score_increase)
                elif event.key == pygame.K_f:
                    score += hit_tile(3, tiles, TILE_HEIGHT, SCREEN_HEIGHT, TILE_WIDTH, score_increase)

                    # Pause the game when Esc key is pressed
                elif event.key == pygame.K_ESCAPE:
                    paused = True
                    print("DEBUG : PAUSED")
                    pygame.mixer.music.pause()  # Pause the music

                    if paused:

                        # put player in pause menu
                        pause_result = pause_menu(screen, clock)

                        if pause_result == "replay":
                            # Restart the game
                            run_game()
                            return True
                        elif pause_result == "menu":
                            # Return to the main menu
                            return True
                        elif pause_result == "resume":
                            # Resume
                            pygame.mixer.music.unpause()
                            paused = False

        # if game is ongoing
        if not paused and not game_over and not game_clear:

            for tile in tiles:
                tile.move()
                if tile.y > SCREEN_HEIGHT:
                    missed_tiles += 1
                    tiles.remove(tile)
                else:
                    tile.draw()

            if frame_count % NEW_TILE_INTERVAL == 0 and is_music_playing():
                create_tile()

            if missed_tiles >= misses_to_fail or score <= score_increase * -misses_to_fail:
                mixer.music.stop()
                game_over = True

            elif not is_music_playing():
                game_clear = True

        # Determine grade based on the score
        if score <= 59:
            grade = "IP"
        elif 60 <= score <= 99:
            grade = "3"
        elif 100 <= score <= 149:
            grade = "2.75"
        elif 150 <= score <= 199:
            grade = "2.5"
        elif 200 <= score <= 249:
            grade = "2.25"
        elif 250 <= score <= 349:
            grade = "2"
        elif 350 <= score <= 449:
            grade = "1.75"
        elif 450 <= score <= 549:
            grade = "1.5"
        elif 550 <= score <= 649:
            grade = "1.25"
        elif score >= 650:
            grade = "1"

        if not game_over and not game_clear:
            # Display score and missed only if the game is not over
            score_text = font.render("Score: " + str(score), True, WHITE)
            missed_text = font.render("Missed: " + str(missed_tiles), True, WHITE)
            # Calculate the position to center the text horizontally
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 40))
            missed_text_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, 80))
            screen.blit(score_text, score_text_rect)
            screen.blit(missed_text, missed_text_rect)

        if game_over:
            game_over_sound.play()
            game_over_text = font.render("GAME OVER! ", True, WHITE)
            final_score_text = font.render("Total Score: " + str(score), True, WHITE)
            missed_text = font.render("Missed: " + str(missed_tiles), True, WHITE)
            grade_text = font.render("Overall Grade: " + str(grade), True, WHITE)
            screen.blit(background, (0, 0))

            # Calculate the position to center the text vertically and horizontally
            game_over_text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            final_score_text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
            missed_text_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 100))
            grade_text_rect = grade_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 150))

            screen.blit(game_over_text, game_over_text_rect)
            screen.blit(final_score_text, final_score_text_rect)
            screen.blit(missed_text, missed_text_rect)
            screen.blit(grade_text, grade_text_rect)

            pygame.display.flip()
            pygame.time.wait(5000)
            return True

        if game_clear:
            mixer.music.stop()
            screen.blit(background, (0, 0))
            game_clear_sound.play()
            game_clear_text = font.render("GAME CLEARED! ", True, WHITE)
            final_score_text = font.render("Total Score: " + str(score), True, WHITE)
            missed_text = font.render("Missed: " + str(missed_tiles), True, WHITE)
            grade_text = font.render("Overall Grade: " + str(grade), True, WHITE)

            # Calculate the position to center the text vertically and horizontally
            game_clear_text_rect = game_clear_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
            final_score_text_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 50))
            missed_text_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 100))
            grade_text_rect = grade_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 + 150))

            screen.blit(game_clear_text, game_clear_text_rect)
            screen.blit(final_score_text, final_score_text_rect)
            screen.blit(missed_text, missed_text_rect)
            screen.blit(grade_text, grade_text_rect)

            pygame.display.flip()
            pygame.time.wait(5000)
            return True

        pygame.display.flip()
        clock.tick(60)
        frame_count += 1

    return False


def hit_tile(column, tiles, TILE_HEIGHT, SCREEN_HEIGHT, TILE_WIDTH, score_increase):

    hit_tolerance = 15  # default 15, higher values makes window of hit tolerance larger

    for tile in tiles:

        # if tile is hit within range of hit tolerance, stop drawing tile and return score to be added
        if tile.y + TILE_HEIGHT >= SCREEN_HEIGHT - hit_tolerance and tile.x == column * TILE_WIDTH:
            tiles.remove(tile)
            scored_sound.play()
            return score_increase

    # player tapped but no tile within range
    hit_notile_sound.play()

    return -score_increase*3

if __name__ == "__main__":
    try:
        while True:
            game_over = run_game()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
