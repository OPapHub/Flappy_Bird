from Variables import *
from Variables import GameState


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'images/bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # gravity
        if GameState.flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)

        if not GameState.game_over:
            # jump
            if pygame.key.get_pressed()[pygame.K_SPACE] and not self.clicked:
                self.vel = -10
                self.clicked = True
                wing_sound.play()

            if not pygame.key.get_pressed()[pygame.K_SPACE] and self.clicked:
                self.clicked = False

            # handle the animation
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)
