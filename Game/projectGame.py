import pygame
import random

# global vars
screen_width = 800
screen_height = 600
display_surf = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('The Game^tm')

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
YELLOW = (0, 255, 255)

game_exit = False
FPS = 20
pygame.init()
pygame.mixer.init()
fpsClock = pygame.time.Clock()

charSprite = pygame.image.load('MarioHead.jpeg')
player_width = charSprite.get_rect()[2]
player_height = charSprite.get_rect()[3]

playerYPos = screen_height - 100 - player_height

meteorImg = pygame.image.load('meteor.png')
meteor_width = meteorImg.get_rect()[2]
meteor_height = meteorImg.get_rect()[3]

menu_font = pygame.font.SysFont(None, 60)


# Necessary to reset the variables for consecutive gameplay
def setVars():
    global playerXPos, playerXSpeed, meteors
    playerXPos = 155
    playerXSpeed = 10
    meteors = []


# quits program if appropriate
def eventHandler():
    global playerXSpeed, game_exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_exit = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXSpeed = -10
            elif event.key == pygame.K_RIGHT:
                playerXSpeed = 10
            elif event.key == pygame.K_ESCAPE:
                game_exit = True


def makeMeteors():
    if random.randint(0, 20) == 0:
        meteors.append([random.randint(0, screen_width-meteor_width), -meteor_height])


# Handles drawing all graphics for the screen
def drawScreen():
    display_surf.fill(GREEN)

    display_surf.blit(charSprite, [playerXPos, playerYPos])

    for meteor in meteors:
        display_surf.blit(meteorImg, meteor)

    pygame.display.update()
    fpsClock.tick(FPS)


# Updates player and meteor positions
def movePlayer():
    global playerXPos
    playerXPos += playerXSpeed
    for meteor in meteors:
        meteor[1] += 5


# First checks if player is at the edge of the screen to bounce back the other way
# Then checks if a meteor has hit the player
# Then check if a meteor has gone off the screen!
def collisionDetection():
    global playerXSpeed
    if playerXPos+player_width >= screen_width or playerXPos <= 0:
        playerXSpeed *= -1

    for meteor in meteors:
        if (meteor[0] <= playerXPos+player_width and meteor[0]+meteor_width >= playerXPos) and\
                (meteor[1] <= playerYPos+player_height and meteor[1]+meteor_height >= playerYPos):
            return True
        elif meteor[1] > screen_height:
            del meteors[0]
    return False


# This function shows the about section, which informs the user how cool we are
def about():
    global game_exit
    about_lines = ["This is our dope game", "developed by tons of dope people", "So play it", "and be dope"]

    spacing = 50
    space = 100
    play_text = []
    menu_text_color = GREEN
    start = True

    # This bit of code renders the text and their rects and stores them as tuples in play_text
    for line in about_lines:
        temp_text = menu_font.render(line, True, menu_text_color)
        temp_rect = temp_text.get_rect()  # Get rect
        temp_rect.center = (screen_width // 2, spacing)
        play_text.append((temp_text, temp_rect))
        spacing += space

    exit_text = menu_font.render("Press 'q' to exit", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (screen_width // 2, screen_height-50)

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
        for text in play_text:
            display_surf.blit(text[0], text[1])
        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(15)


# This function displays the leaders on the leaderboard
def leaderboard():
    global game_exit
    leaders = ["1) Matt Niemiec  1575", "2) Kobe Bryant   500", "3) Peyton Manning   450", "4) Aaron Gwin   300",
               "5) Link   5"]
    spacing = 50
    space = 100
    play_text = []
    menu_text_color = GREEN
    start = True

    # This bit of code renders the text and their rects and stores them as tuples in play_text
    for leader in leaders:
        temp_text = menu_font.render(leader, True, menu_text_color)
        temp_rect = temp_text.get_rect()  # Get rect
        temp_rect.center = (screen_width // 2, spacing)
        play_text.append((temp_text, temp_rect))
        spacing += space

    exit_text = menu_font.render("Press 'q' to exit", True, menu_text_color)
    exit_rect = exit_text.get_rect()  # Get rect
    exit_rect.center = (screen_width // 2, screen_height-50)

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
        for text in play_text:
            display_surf.blit(text[0], text[1])
        display_surf.blit(exit_text, exit_rect)
        pygame.display.update()
        fpsClock.tick(15)


# Start screen
def startMenu():
    global game_exit
    start = True
    spacing = 100
    menu_text_color = GREEN

    play_text = menu_font.render("Click to Play", True, menu_text_color)
    play_rect = play_text.get_rect()  # Get rect
    play_rect.center = (screen_width // 2, spacing)

    leaderboard_text = menu_font.render("Leaderboard", True, menu_text_color)
    leaderboard_rect = leaderboard_text.get_rect()  # Get rect
    leaderboard_rect.center = (screen_width // 2, spacing*2)

    about_text = menu_font.render("About", True, menu_text_color)
    about_rect = about_text.get_rect()  # Get rect
    about_rect.center = (screen_width // 2, spacing * 3)

    quit_text = menu_font.render("Quit", True, menu_text_color)
    quit_rect = quit_text.get_rect()  # Get rect
    quit_rect.center = (screen_width // 2, spacing*4)

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

        if play_rect[0] < mouse_pos[0] < play_rect[0] + play_rect[2] and \
                play_rect[1] < mouse_pos[1] < play_rect[1] + play_rect[3]:
            if mouse_down:
                start = False

        elif leaderboard_rect[0] < mouse_pos[0] < leaderboard_rect[0] + leaderboard_rect[2] and \
                leaderboard_rect[1] < mouse_pos[1] < leaderboard_rect[1] + leaderboard_rect[3]:
            if mouse_down:
                leaderboard()

        elif about_rect[0] < mouse_pos[0] < about_rect[0] + about_rect[2] and \
                about_rect[1] < mouse_pos[1] < about_rect[1] + about_rect[3]:
            if mouse_down:
                about()

        elif quit_rect[0] < mouse_pos[0] < quit_rect[0] + quit_rect[2] and \
                quit_rect[1] < mouse_pos[1] < quit_rect[1] + quit_rect[3]:
            if mouse_down:
                start = False
                game_exit = True

        display_surf.fill(WHITE)
        display_surf.blit(play_text, play_rect)
        display_surf.blit(leaderboard_text, leaderboard_rect)
        display_surf.blit(about_text, about_rect)
        display_surf.blit(quit_text, quit_rect)
        pygame.display.update()
        fpsClock.tick(15)


# Runs the start menu and then loops through the game
def main():
    startMenu()
    setVars()
    while not game_exit:
        makeMeteors()
        drawScreen()
        movePlayer()
        eventHandler()
        dead = collisionDetection()

        if dead:
            startMenu()
            setVars()

    pygame.display.quit()
    pygame.quit()

if __name__ == '__main__':
    main()
