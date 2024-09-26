# skilltext.py

import pygame

class SkillText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, font, color):
        super().__init__()
        self.font = font
        self.color = color
        self.image = self.font.render(text, True, self.color)
        self.rect = self.image.get_rect(center=(x, y))
        self.lifetime = 60  # Frame duration
        self.timer = 0

    def update(self):
        self.timer += 1
        if self.timer > self.lifetime:
            self.kill()  # Remove text
