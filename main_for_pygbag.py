import random
import pygame
import asyncio
import os

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Flappy Bird')

fps = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

color = (255, 255, 255)
ground_scroll = 0
pipe_gap = 150
scroll_speed = 4
flying = False
game_over = False
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
sound_played = False

# load images
bg = pygame.image.load(os.path.join(os.getcwd(), 'images', 'background.png')).convert_alpha()
bg.set_colorkey((255, 255, 255))
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT - 100))
base = pygame.image.load(os.path.join(os.getcwd(), 'images', 'base.png')).convert_alpha()
base.set_colorkey((255, 255, 255))
base = pygame.transform.scale(base, (SCREEN_WIDTH + 35, 100))
button_img = pygame.image.load(os.path.join(os.getcwd(), 'images', 'restart.png')).convert_alpha()
button_img.set_colorkey((0, 0, 0))

# load music
bg_music = pygame.mixer.Sound(os.path.join(os.getcwd(), 'music', 'bgmusic.ogg'))
die_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'music', 'die.ogg'))
point_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'music', 'point.ogg'))
hit_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'music', 'hit.ogg'))
wing_sound = pygame.mixer.Sound(os.path.join(os.getcwd(), 'music', 'wing.ogg'))
bg_music.set_volume(0.3)
die_sound.set_volume(0.3)
point_sound.set_volume(0.3)
hit_sound.set_volume(0.3)
wing_sound.set_volume(0.3)

clock = pygame.time.Clock()

bg_music.play(loops=-1)


def draw_text(text, text_col, x, y, font_size):
    font = pygame.font.Font(os.path.join(os.getcwd(), 'fonts', 'Bauhaus93Regular.ttf'), font_size)
    img = font.render(text, True, text_col)
    img.set_colorkey((0, 0, 0))
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = SCREEN_HEIGHT // 2
    new_score = 0
    bg_music.play(loops=-1)
    return new_score


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(os.path.join(os.getcwd(), 'images', f'bird{num}.png')).convert_alpha()
            img.set_colorkey((255, 255, 255))
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        # gravity
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8

            if self.rect.bottom < SCREEN_HEIGHT - 100:
                self.rect.y += int(self.vel)

        if not game_over:
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


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.getcwd(), 'images', 'pipe.png')).convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        # position 1 - top, -1 - bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - pipe_gap // 2]
        if position == -1:
            self.rect.topleft = [x, y + pipe_gap // 2]

    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()


class Button:
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self):

        action = False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # check if mouse is over the button
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        # draw button
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird(100, SCREEN_HEIGHT // 2)

bird_group.add(flappy)

# create restart button instance
button = Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50, button_img)


async def main():
    global ground_scroll, pass_pipe, score, sound_played, game_over, flying, last_pipe
    run = True
    while run:

        clock.tick(fps)

        # draw background
        screen.blit(bg, (0, 0))

        bird_group.draw(screen)
        bird_group.update()
        pipe_group.draw(screen)

        # draw the ground
        screen.blit(base, (ground_scroll, SCREEN_HEIGHT - 100))

        # check the score
        if len(pipe_group) > 0:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                    and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                    and not pass_pipe:
                pass_pipe = True
            if pass_pipe:
                if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                    score += 1
                    point_sound.play()
                    pass_pipe = False

        draw_text(str(score), color, (SCREEN_WIDTH // 2) - 30, 20, 60)
        draw_text("HIT SPACE", color, 10, SCREEN_HEIGHT - 80, 60)
        draw_text("made by OPapHub", color, 20, SCREEN_HEIGHT - 20, 10)
        # look for collision
        if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
            if not sound_played:
                bg_music.stop()
                hit_sound.play()
                die_sound.play()
                sound_played = True
            game_over = True

        # check if bird has hit the ground
        if flappy.rect.bottom >= SCREEN_HEIGHT - 102:
            game_over = True
            flying = False
            if not sound_played:
                bg_music.stop()
                hit_sound.play()
                die_sound.play()
                sound_played = True

        if not game_over and flying:
            # generate new pipes
            time_now = pygame.time.get_ticks()
            if time_now - last_pipe > pipe_frequency:
                pipe_height = random.randint(-100, 100)
                btm_pipe = Pipe(SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + pipe_height, -1)
                top_pipe = Pipe(SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + pipe_height, 1)
                pipe_group.add(btm_pipe)
                pipe_group.add(top_pipe)
                last_pipe = time_now

            # scroll the ground
            ground_scroll -= scroll_speed
            if abs(ground_scroll) > 35:
                ground_scroll = 0

            pipe_group.update()

        # check for game over and reset
        if game_over:
            if button.draw():
                game_over = False
                sound_played = False
                flying = False
                bg_music.play(loops=-1)
                score = reset_game()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and not flying and not game_over:
                if event.key == pygame.K_SPACE:
                    flying = True

        pygame.display.update()
        await asyncio.sleep(0)


asyncio.run(main())
