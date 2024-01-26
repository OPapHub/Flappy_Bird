import random

import Bird as Bird
import Button as Button
import Pipe as Pipe
from Variables import *
from Variables import GameState

pygame.init()
pygame.display.set_caption('Flappy Bird')

bg_music.play(loops=-1)

font = pygame.font.SysFont('Bauhaus 93', 60)


def draw_text(text, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


def reset_game():
    pipe_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = SCREEN_HEIGHT // 2
    new_score = 0
    bg_music.play(loops=-1)
    return new_score


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappy = Bird.Bird(100, SCREEN_HEIGHT // 2)

bird_group.add(flappy)

# create restart button instance
button = Button.Button(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2 - 50, button_img)

run = True

global ground_scroll, score, last_pipe, pass_pipe, sound_played, screen
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

    draw_text(str(score), color, (SCREEN_WIDTH // 2) - 30, 20)

    # look for collision
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappy.rect.top < 0:
        if not sound_played:
            bg_music.stop()
            hit_sound.play()
            die_sound.play()
            sound_played = True
        GameState.game_over = True

    # check if bird has hit the ground
    if flappy.rect.bottom >= SCREEN_HEIGHT - 102:
        GameState.game_over = True
        flying = False
        if not sound_played:
            bg_music.stop()
            hit_sound.play()
            die_sound.play()
            sound_played = True

    if not GameState.game_over and GameState.flying:
        # generate new pipes
        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipe_height = random.randint(-100, 100)
            btm_pipe = Pipe.Pipe(SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + pipe_height, -1)
            top_pipe = Pipe.Pipe(SCREEN_WIDTH, (SCREEN_HEIGHT // 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_now

        # scroll the ground
        ground_scroll -= scroll_speed
        if abs(ground_scroll) > 35:
            ground_scroll = 0

        pipe_group.update()

    # check for game over and reset
    if GameState.game_over:
        if button.draw():
            GameState.game_over = False
            sound_played = False
            GameState.update_flying(False)
            bg_music.play(loops=-1)
            score = reset_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN and not GameState.flying and not GameState.game_over:
            if event.key == pygame.K_SPACE:
                GameState.update_flying(True)

    pygame.display.update()
pygame.quit()
