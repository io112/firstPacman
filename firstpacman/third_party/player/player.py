import pygame


class Player:
    def __init__(self):
        pygame.mixer.init()
        self.sounds = [
            pygame.mixer.Sound('sounds/machigatte-iru-torappuintoro.ogg'),
            pygame.mixer.Sound('sounds/Toby_Fox_-_Here_We_Are_64962842.ogg'),
            pygame.mixer.Sound('sounds/Bass_Drum_Impact_Sound_Effect_[Free].ogg')
        ]

    def play_game_sound(self):
        self.sounds[0].play(-1)

    def stop_game_sound(self):
        self.sounds[0].stop()

    def play_menu_sound(self):
        self.sounds[1].play(-1)

    def stop_menu_sound(self):
        self.sounds[1].stop()

    def play_bass(self):
        self.sounds[2].play(3)
