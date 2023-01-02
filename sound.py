import pygame

def play(name):
    pygame.mixer.Sound.play(pygame.mixer.Sound(f'assets/sounds/{name}.mp3'))
    pygame.mixer.music.stop()
