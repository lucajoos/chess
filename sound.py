import pygame

def play(name):
    pygame.mixer.Sound.play(pygame.mixer.Sound(f'assets/sounds/{name}.wav'))
    pygame.mixer.music.stop()
