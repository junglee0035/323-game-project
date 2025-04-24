from settings import *

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos, groups, coin_image, value=1):
        super().__init__(groups)
        self.image = coin_image
        self.rect = self.image.get_rect(topleft=pos)
        self.value = value
