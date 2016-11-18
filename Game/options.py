import pygame


# This is a class that we as a CSCI 3308 team implemented to make handling settings easier
class Options:
    def __init__(self):
        self.mute = False
        self.max_difficulty = 3
        self.difficulty = 0
        self.meteor_speed = 5
        self.player_speed = 10
        self.player_velocity = self.player_speed
        self.start = True
        self.logged_in = False
        self.userID = ""
        self.background_speed = 2

    def changePause(self):
        self.mute = not self.mute
        if self.mute:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def changeDifficulty(self, difficulty):
        self.difficulty = difficulty
        self.player_speed = 10 + difficulty*4
        self.meteor_speed = 5 + difficulty*3
        self.background_speed = 2 + difficulty*20
