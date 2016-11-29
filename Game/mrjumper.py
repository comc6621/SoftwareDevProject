import pygame
import random
from spritesheet import spritesheet
import options
import inputbox
import sys

# global vars
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
display_surf = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Mr. Jumper')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

game_exit = False
FPS = 20
pygame.init()
pygame.mixer.init()
fpsClock = pygame.time.Clock()

MUSIC_FILE = "gameplay.wav"
options = options.Options()

# Dead code from when all we had was one image. Now we're implementing sprite sheets
# charSprite = pygame.image.load('MarioHead.jpeg')
# player_width = charSprite.get_rect()[2]
# player_height = charSprite.get_rect()[3]

# New experimental code to implement the spritesheet
SPRITE_ROWS = 4
SPRITE_COLS = 4
ss = spritesheet.spritesheet('SpriteSheet.png')
SHEET_WIDTH = ss.sheet.get_rect()[2]
sheet_height = ss.sheet.get_rect()[3]
PLAYER_WIDTH = SHEET_WIDTH // SPRITE_COLS
PLAYER_HEIGHT = sheet_height // SPRITE_ROWS

background_image = pygame.image.load("game_background.png")
background_height = background_image.get_rect()[3]

welcome_image = pygame.image.load("welcome_screen.jpg")

locations = {}
loc_map = {0: 'front', 1: 'left', 2: 'right', 3: 'back'}
# locations = []
for i in range(SPRITE_ROWS):
    side = loc_map[i]
    temp_list = []
    for j in range(SPRITE_COLS):
        temp_list.append((j * PLAYER_WIDTH, i * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
    locations[side] = temp_list

player_front = ss.images_at(locations['front'], colorkey=(255, 255, 255))
player_left = ss.images_at(locations['left'], colorkey=(255, 255, 255))
player_right = ss.images_at(locations['right'], colorkey=(255, 255, 255))
player_back = ss.images_at(locations['back'], colorkey=(255, 255, 255))
charSprite = [player_left, player_right]

PLAYER_Y_POS = SCREEN_HEIGHT - 100 - PLAYER_HEIGHT
count_frames = 0
which_sprite = 0

meteorImg = pygame.image.load('meteor.png')
meteor_width = meteorImg.get_rect()[2]
meteor_height = meteorImg.get_rect()[3]

menu_font = pygame.font.SysFont(None, 60)


# Necessary to reset the variables for consecutive gameplay
def setVars():
    global playerXPos, meteors, player_direction, score, background_location
    playerXPos = SCREEN_WIDTH//2
    options.player_velocity = options.player_speed
    meteors = []
    player_direction = 0
    score = 0
    background_location = SCREEN_HEIGHT-background_height


# quits program if appropriate
def eventHandler():
    global game_exit, player_direction
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                options.player_velocity = -options.player_speed
                player_direction = 1
            elif event.key == pygame.K_RIGHT:
                options.player_velocity = options.player_speed
                player_direction = 0
            elif event.key == pygame.K_m:
                options.changePause()
            elif event.key == pygame.K_ESCAPE:
                game_exit = True


def makeMeteors():
    if random.randint(0, 20) == 0:
        meteors.append([random.randint(0, SCREEN_WIDTH-meteor_width), -meteor_height])


# Handles drawing all graphics for the screen
def drawScreen():
    global count_frames, which_sprite, score
    display_surf.fill(GREEN)

    display_surf.blit(background_image, [0, background_location])

    count_frames += 1
    flip_sprite_image_speed = 5
    if count_frames == flip_sprite_image_speed:
        count_frames = 0
        which_sprite += 1
        if which_sprite == SPRITE_ROWS:
            which_sprite = 0
            score += 1

    display_surf.blit(charSprite[player_direction][which_sprite], [playerXPos, PLAYER_Y_POS])

    for meteor in meteors:
        display_surf.blit(meteorImg, meteor)

    score_text = menu_font.render("Your score: "+str(score), True, WHITE)
    score_rect = score_text.get_rect()
    score_rect.center = (SCREEN_WIDTH//2, 50)

    display_surf.blit(score_text, score_rect)

    pygame.display.update()
    fpsClock.tick(FPS)


# Updates player and meteor positions and the background
def movePlayer():
    global playerXPos, background_location
    playerXPos += options.player_velocity

    background_location += options.background_speed
    if background_location >= 2:
        background_location = SCREEN_HEIGHT - background_height
    for meteor in meteors:
        meteor[1] += options.meteor_speed


# First checks if player is at the edge of the screen to bounce back the other way
# Then checks if a meteor has hit the player
# Then check if a meteor has gone off the screen!
def collisionDetection():
    global player_direction, playerXPos
    if playerXPos+PLAYER_WIDTH >= SCREEN_WIDTH or playerXPos <= 0:
        options.player_velocity *= -1
        player_direction = not player_direction

    for meteor in meteors:
        if (meteor[0] <= playerXPos+PLAYER_WIDTH and meteor[0]+meteor_width >= playerXPos) and\
                (meteor[1] <= PLAYER_Y_POS+PLAYER_HEIGHT and meteor[1]+meteor_height >= PLAYER_Y_POS):
            return True
        elif meteor[1] > SCREEN_HEIGHT:
            del meteors[0]
    return False


# This function checks if the music is playing or not, and if not, it plays it
def play_music():
    if not pygame.mixer.music.get_busy() and not options.mute:
        pygame.mixer.music.load(MUSIC_FILE)
        pygame.mixer.music.play()


# This function shows the about section, which informs the user how cool we are
def about():
    global game_exit
    about_lines = ["This is our dope game", "developed by tons of dope people", "So play it", "and be dope"]

    spacing = 50
    space = 100
    play_text = []
    menu_text_color = WHITE
    start = True

    # This bit of code renders the text and their rects and stores them as tuples in play_text
    for line in about_lines:
        temp_text = menu_font.render(line, True, menu_text_color)
        temp_rect = temp_text.get_rect()  # Get rect
        temp_rect.center = (SCREEN_WIDTH // 2, spacing)
        play_text.append((temp_text, temp_rect))
        spacing += space

    exit_text = menu_font.render("Press 'q' to exit", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT-50)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))
        for text in play_text:
            display_surf.blit(text[0], text[1])
        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(FPS)


# This function displays the leaders on the leaderboard
def leaderboard():
    global game_exit
    leaders = ["1) Matt Niemiec  1575", "2) Kobe Bryant   500", "3) Peyton Manning   450", "4) Aaron Gwin   300",
               "5) Link   5"]
    spacing = 50
    space = 100
    play_text = []
    menu_text_color = WHITE
    start = True

    # This bit of code renders the text and their rects and stores them as tuples in play_text
    for leader in leaders:
        temp_text = menu_font.render(leader, True, menu_text_color)
        temp_rect = temp_text.get_rect()  # Get rect
        temp_rect.center = (SCREEN_WIDTH // 2, spacing)
        play_text.append((temp_text, temp_rect))
        spacing += space

    exit_text = menu_font.render("Press 'q' to exit", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT-50)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))
        for text in play_text:
            display_surf.blit(text[0], text[1])
        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(FPS)


def login():
    global game_exit
    start = True
    spacing = 80
    num_of_spaces = 2
    menu_text_color = WHITE
    step = 0

    login_text = menu_font.render("Log in", True, menu_text_color)
    login_rect = login_text.get_rect()  # Get rect
    login_rect.center = (SCREEN_WIDTH // 2, spacing * num_of_spaces)
    num_of_spaces += 1

    signup_text = menu_font.render("Sign Up", True, menu_text_color)
    signup_rect = signup_text.get_rect()  # Get rect
    signup_rect.center = (SCREEN_WIDTH // 2, spacing * num_of_spaces)
    num_of_spaces += 1

    return_text = menu_font.render("Return", True, menu_text_color)
    return_rect = return_text.get_rect()  # Get rect
    return_rect.center = (SCREEN_WIDTH // 2, spacing * num_of_spaces)
    num_of_spaces += 1

    prompt_text = menu_font.render("Enter Your Username", True, menu_text_color)
    prompt_rect = prompt_text.get_rect()  # Get rect
    prompt_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)
    num_of_spaces += 1

    quit_text = menu_font.render("Press 'q' to quit", True, menu_text_color)
    quit_rect = quit_text.get_rect()  # Get rect
    quit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)

    while start and not game_exit:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

        mouse_pos = pygame.mouse.get_pos()

        # These lines check if the cursor is over one of the boxes, and if so, checks if the mouse
        # has been clicked, and then does its respective action

        if login_rect[0] < mouse_pos[0] < login_rect[0] + login_rect[2] and \
                login_rect[1] < mouse_pos[1] < login_rect[1] + login_rect[3]:
            if mouse_down and not step:
                step += 1
                extra_password_check = False
        elif signup_rect[0] < mouse_pos[0] < signup_rect[0] + signup_rect[2] and \
                signup_rect[1] < mouse_pos[1] < signup_rect[1] + signup_rect[3]:
            if mouse_down and not step:
                step += 1
                extra_password_check = True
        elif return_rect[0] < mouse_pos[0] < return_rect[0] + return_rect[2] and \
                return_rect[1] < mouse_pos[1] < return_rect[1] + return_rect[3]:
            if mouse_down and not step:
                return

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))
        if not step:
            display_surf.blit(login_text, login_rect)
            display_surf.blit(signup_text, signup_rect)
            display_surf.blit(return_text, return_rect)
        elif step == 1:
            display_surf.blit(prompt_text, prompt_rect)
            username = inputbox.ask(display_surf, "")
            step += 1
        elif step == 2:
            prompt_text = menu_font.render("What's your password?", True, menu_text_color)
            display_surf.blit(prompt_text, prompt_rect)
            password = inputbox.ask(display_surf, "")
            step += 1
            if not extra_password_check:
                databaseLogin(username, password)
                return
        elif step == 3:
            prompt_text = menu_font.render("Confirm Your Password", True, menu_text_color)
            display_surf.blit(prompt_text, prompt_rect)
            validated_pass = inputbox.ask(display_surf, "")
            step += 1
            if password == validated_pass:
                createUser(username, password)
                success_message = "You successfully created a user!"
            else:
                success_message = "Sorry! Passwords did not match!"
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        return
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_q:
                            return
                display_surf.fill(WHITE)
                display_surf.blit(welcome_image, (0, 0))

                prompt_text = menu_font.render(success_message, True, menu_text_color)
                prompt_rect = prompt_text.get_rect()  # Get rect
                prompt_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100)

                display_surf.blit(prompt_text, prompt_rect)
                display_surf.blit(quit_text, quit_rect)
                pygame.display.update()
                fpsClock.tick(FPS)

        pygame.display.update()
        fpsClock.tick(FPS)


def databaseLogin(username, password):
    print("This is where you connect to the database and log in!")


def createUser(username, password):
    print("This is the function where a user is created!")


def logout():
    print("This is the function that communicates with the database to logout")


# This function show the settings that the user can edit
def options_menu():
    global game_exit

    menu_text_color = WHITE
    start = True

    # There's a fair bit of not-obvious math for the slider. I tried to name well, but still not for math wimps
    max_difficulty = options.max_difficulty
    thickness = 15
    bar_height = 50
    slider_bar_dims = [SCREEN_WIDTH//4, SCREEN_HEIGHT//3, SCREEN_WIDTH//2, thickness]
    increment = (slider_bar_dims[2])//max_difficulty
    initial_bar_pos = slider_bar_dims[0] + options.difficulty*increment
    difficulty_bar_dims = [initial_bar_pos, slider_bar_dims[1]-bar_height+thickness//2, thickness, bar_height*2]

    exit_text = menu_font.render("Press 'q' to exit or 's' to save", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    while start:
        is_clicked = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if is_clicked[0] and difficulty_bar_dims[1] < mouse_pos[1] < difficulty_bar_dims[1] + difficulty_bar_dims[3]:
            # I offset the slider and x to the left-hand side of the screen to simplify math, then change it back

            #
            # DO NOT TOUCH THE FOLLOWING LINES OF CODE
            #
            x = mouse_pos[0]
            if x < slider_bar_dims[0]:
                x = slider_bar_dims[0]
            if x > slider_bar_dims[0] + slider_bar_dims[2]:
                x = slider_bar_dims[0] + slider_bar_dims[2]
            x -= slider_bar_dims[0]
            x = int(round(x / increment)) * increment
            x += slider_bar_dims[0]
            difficulty_bar_dims[0] = x
            #
            # Okay you can touch the code again
            #

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return
                if event.key == pygame.K_s:
                    level = round((difficulty_bar_dims[0]-slider_bar_dims[0])*max_difficulty/slider_bar_dims[2])
                    options.changeDifficulty(level)
                    return

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))

        pygame.draw.rect(display_surf, menu_text_color, tuple(slider_bar_dims))
        pygame.draw.rect(display_surf, menu_text_color, tuple(difficulty_bar_dims))

        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(FPS)


# This function shows the screen that the user sees after they die, inviting the to play again or return to the menu
def hasLost():
    global game_exit

    menu_text_color = WHITE
    start = True

    score_informer = "Your score is: {0}".format(score)

    score_text = menu_font.render(score_informer, True, menu_text_color)
    score_rect = score_text.get_rect()  # Get rect
    score_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    exit_text = menu_font.render("Press 'm' for menu or 'p' to play again", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)

    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    options.start = True
                    setVars()
                    return
                if event.key == pygame.K_p:
                    options.start = False
                    setVars()
                    return

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))
        display_surf.blit(score_text, score_rect)
        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(FPS)


# Start screen
def startMenu():
    global game_exit
    start = True
    spacing = 80
    num_of_spaces = 1
    menu_text_color = WHITE

    play_text = menu_font.render("Click to Play", True, menu_text_color)
    play_rect = play_text.get_rect()  # Get rect
    play_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    leaderboard_text = menu_font.render("Leaderboard", True, menu_text_color)
    leaderboard_rect = leaderboard_text.get_rect()  # Get rect
    leaderboard_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    about_text = menu_font.render("About", True, menu_text_color)
    about_rect = about_text.get_rect()  # Get rect
    about_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    login_text = menu_font.render("Login/Sign Up", True, menu_text_color)
    login_rect = login_text.get_rect()  # Get rect
    login_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    options_text = menu_font.render("Settings", True, menu_text_color)
    options_rect = options_text.get_rect()  # Get rect
    options_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    quit_text = menu_font.render("Quit", True, menu_text_color)
    quit_rect = quit_text.get_rect()  # Get rect
    quit_rect.center = (SCREEN_WIDTH // 2, spacing*num_of_spaces)
    num_of_spaces += 1

    while start and not game_exit:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                game_exit = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True

        mouse_pos = pygame.mouse.get_pos()

        # These lines check if the cursor is over one of the boxes, and if so, checks if the mouse
        # has been clicked, and then does its respective action
        if play_rect[0] < mouse_pos[0] < play_rect[0] + play_rect[2] and \
                play_rect[1] < mouse_pos[1] < play_rect[1] + play_rect[3]:
            if mouse_down:
                setVars()
                options.start = False
                start = False

        elif leaderboard_rect[0] < mouse_pos[0] < leaderboard_rect[0] + leaderboard_rect[2] and \
                leaderboard_rect[1] < mouse_pos[1] < leaderboard_rect[1] + leaderboard_rect[3]:
            if mouse_down:
                leaderboard()

        elif about_rect[0] < mouse_pos[0] < about_rect[0] + about_rect[2] and \
                about_rect[1] < mouse_pos[1] < about_rect[1] + about_rect[3]:
            if mouse_down:
                about()

        elif login_rect[0] < mouse_pos[0] < login_rect[0] + login_rect[2] and \
                login_rect[1] < mouse_pos[1] < login_rect[1] + login_rect[3]:
            if mouse_down:
                login()

        elif options_rect[0] < mouse_pos[0] < options_rect[0] + options_rect[2] and \
                options_rect[1] < mouse_pos[1] < options_rect[1] + options_rect[3]:
            if mouse_down:
                options_menu()

        elif quit_rect[0] < mouse_pos[0] < quit_rect[0] + quit_rect[2] and \
                quit_rect[1] < mouse_pos[1] < quit_rect[1] + quit_rect[3]:
            if mouse_down:
                start = False
                game_exit = True

        display_surf.fill(WHITE)
        display_surf.blit(welcome_image, (0, 0))
        display_surf.blit(play_text, play_rect)
        display_surf.blit(leaderboard_text, leaderboard_rect)
        display_surf.blit(about_text, about_rect)
        display_surf.blit(login_text, login_rect)
        display_surf.blit(options_text, options_rect)
        display_surf.blit(quit_text, quit_rect)
        pygame.display.update()
        fpsClock.tick(FPS)


# Runs the start menu and then loops through the game
def main():
    while not game_exit:
        if options.start:
            startMenu()
            if game_exit:
                break
        play_music()
        makeMeteors()
        drawScreen()
        movePlayer()
        eventHandler()
        dead = collisionDetection()

        if dead:
            pygame.mixer.music.stop()
            hasLost()

    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    main()
