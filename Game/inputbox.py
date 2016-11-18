# by Timothy Downs, inputbox written for my map editor

# This program needs a little cleaning up
# It ignores the shift key
# And, for reasons of my own, this program converts "-" to "_"

# A program to get user input, allowing backspace etc
# shown in a box in the middle of the screen
# Called by:
# import inputbox
# answer = inputbox.ask(screen, "Your name")
#
# Only near the center of the screen is blitted to

# The above comments give credit to the source where Return A of CSCI 3308 got this,
# but I am going to change it some, so it will not be exactly the same

import pygame, pygame.font, pygame.event, pygame.draw
from pygame.locals import *
import sys


def get_key():
    while 1:
        event = pygame.event.poll()
        if event.type == KEYDOWN:
            # print(event.key)
            return event.key
        elif event.type == pygame.QUIT:
            sys.exit(0)


def display_box(screen, message):
    # Print a message in a box in the middle of the screen
    fontobject = pygame.font.Font(None, 28)
    pygame.draw.rect(screen, (0, 0, 0),
                     ((screen.get_width() / 2) - 100,
                      (screen.get_height() / 2) - 10,
                      200, 20), 0)
    pygame.draw.rect(screen, (255,255,255),
                     ((screen.get_width() / 2) - 102,
                     (screen.get_height() / 2) - 12,
                     204, 24), 1)
    if len(message) != 0:
        screen.blit(fontobject.render(message, 1, (255, 255, 255)),
                    ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
    pygame.display.flip()


def ask(screen, question):
    # ask(screen, question) -> answer
    pygame.font.init()
    current_string = []
    display_box(screen, question + " " + "".join(current_string))
    while 1:
        inkey = get_key()
        if inkey == K_BACKSPACE:
            current_string = current_string[0:-1]
            display_box(screen, question + " " + "".join(current_string))
        elif inkey == K_RETURN:
            break
        elif inkey == K_MINUS:
            current_string.append("_")
        elif inkey <= 127:
            current_string.append(chr(inkey))
            display_box(screen, question + " " + "".join(current_string))
    return "".join(current_string)


def main():
    screen = pygame.display.set_mode((320,240))
    print(ask(screen, "Name") + " was entered")

if __name__ == '__main__':
    main()