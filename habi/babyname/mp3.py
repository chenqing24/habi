# coding=gbk

import os
import pygame
import time


file = os.path.abspath('.') + '\\faded.mp3'

pygame.mixer.init()

track = pygame.mixer.music.load(file)
pygame.mixer.music.play()


time.sleep(1000)
pygame.mixer.music.play()
