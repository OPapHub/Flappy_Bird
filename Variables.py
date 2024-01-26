import pygame


class GameState:
    flying = False
    game_over = False
    @classmethod
    def update_flying(cls, new_flying):
        cls.flying = new_flying


fps = 60

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
color = (255, 255, 255)
ground_scroll = 0
pipe_gap = 150
scroll_speed = 4
game_over = False
pipe_frequency = 1500  # milliseconds
last_pipe = pygame.time.get_ticks() - pipe_frequency
score = 0
pass_pipe = False
sound_played = False

# load images
bg = pygame.image.load('images/background.png')
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT - 100))
base = pygame.image.load('images/base.png')
base = pygame.transform.scale(base, (SCREEN_WIDTH + 35, 100))
button_img = pygame.image.load('images/restart.png')

# load music
pygame.mixer.init()
bg_music = pygame.mixer.Sound('music/bgmusic.ogg')
die_sound = pygame.mixer.Sound('music/die.ogg')
point_sound = pygame.mixer.Sound('music/point.ogg')
hit_sound = pygame.mixer.Sound('music/hit.ogg')
wing_sound = pygame.mixer.Sound('music/wing.ogg')
bg_music.set_volume(0.3)
die_sound.set_volume(0.3)
point_sound.set_volume(0.3)
hit_sound.set_volume(0.3)
wing_sound.set_volume(0.3)

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
