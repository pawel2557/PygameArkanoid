import pygame
import button
import random
from pygame.locals import *

pygame.init()

screen_width = 600
screen_height = 600
game_paused = True
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Arkanoid')

#dźwięk
explosion_sound = pygame.mixer.Sound("sound/hit.mp3")
pygame.mixer.music.load("sound/stage_music.mp3")
pygame.mixer.music.set_volume(0.02)
pygame.mixer.music.play(-1)


#czcionka
font = pygame.font.SysFont('Constantia', 30)

#kolory
bg = (234,218, 184)
menu_bg = pygame.image.load("img/menu.png").convert()

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
RED = (255, 0, 0)

#kolor paletki
paddle_col = (32, 214, 228)
paddle_outline = (254,254,254)
#kolor tekstu
text_color = (78, 81, 139)

#poziom
cols = 12
rows = 6
#zegar gry
clock = pygame.time.Clock()
fps = 60
live_ball = False
game_over = 0
#aktywny poziom
active_lvl = 1



#load button images
resume_img = pygame.image.load("img/button1.png").convert_alpha()
lvl1_img = pygame.image.load("img/lvl1.png").convert_alpha()
lvl2_img = pygame.image.load("img/lvl2.png").convert_alpha()
lvl3_img = pygame.image.load("img/lvl3.png").convert_alpha()
quit_img = pygame.image.load("img/button2.png").convert_alpha()


#create button instances
resume_button = button.Button(50, 50, resume_img, 1)
lvl1_button = button.Button(200, 50, lvl1_img, 1)
lvl2_button = button.Button(200, 150, lvl2_img, 1)
lvl3_button = button.Button(200, 250, lvl3_img, 1)
quit_button = button.Button(50, 150, quit_img, 1)

#funkcja tekst na ekranie


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
#wybuch
class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speedx = random.randint(-10, 10)
        self.speedy = random.randint(-10, 10)
        self.timer = 20

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.speedx *= 0.9
        self.speedy *= 0.9
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

all_sprites = pygame.sprite.Group()

#klasa poziomu
class Brick(pygame.sprite.Sprite):
    def __init__(self, name, image_path, strength):
        super().__init__()
        self.name = name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.strength = strength
        self.width = screen_width // cols
        self.height = 30

class Wall():
    def __init__(self):
        self.bricks_group = pygame.sprite.Group()

    def draw_wall(self, surface):
        self.bricks_group.draw(surface)
        for col in self.bricks_group:
            pygame.draw.rect(screen, bg, col.rect, 2)

    def create_wall(self, brick_map):
        for row in range(len(brick_map)):
            for col in range(len(brick_map[row])):
                brick_type = brick_map[row][col]
                if brick_type != 0:
                    brick_name = f"Brick{brick_type}"
                    image_path = f"img/brick{brick_type}.png"
                    brick = Brick(brick_name, image_path, brick_type)
                    brick.rect.x = col * brick.width
                    brick.rect.y = row * brick.height
                    self.bricks_group.add(brick)

#poszczególny level


class Wall1(Wall):
    def __init__(self):
        super().__init__()
        self.brick_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0],
            [0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.create_wall(self.brick_map)


class Wall2(Wall):
    def __init__(self):
        super().__init__()
        self.brick_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0],
            [0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
            [0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0],
            [0, 2, 0, 0, 0, 2, 0, 2, 2, 2, 2, 0],
            [0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
            [0, 2, 2, 0, 2, 2, 0, 2, 0, 0, 0, 0],
            [0, 2, 2, 2, 2, 2, 0, 2, 0, 0, 0, 0]
        ]
        self.create_wall(self.brick_map)


class Wall3(Wall):
    def __init__(self):
        super().__init__()
        self.brick_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0]
        ]
        self.create_wall(self.brick_map)


#klasa paletki
class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset()

    def move(self):
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width/4)
        self.x = int((screen_width / 2) - (self.width / 2))
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0

class Game_ball(pygame.sprite.Sprite):
    def __init__(self, x ,y):
        super().__init__()
        self.reset(x, y)

    def move(self):

        collision_thresh = 5



        #kolizja z  cegłą
        for col in wall.bricks_group:
            if self.rect.colliderect(col.rect):

                explosion_sound.set_volume(0.4)
                explosion_sound.play()


                if abs(self.rect.bottom - col.rect.top) < collision_thresh and self.speed_y > 0:
                    self.speed_y *= -1
                elif abs(self.rect.top - col.rect.bottom) < collision_thresh and self.speed_y < 0:
                    self.speed_y *= -1
                elif abs(self.rect.right - col.rect.left) < collision_thresh and self.speed_x > 0:
                    self.speed_x *= -1
                elif abs(self.rect.left - col.rect.right) < collision_thresh and self.speed_x < 0:
                    self.speed_x *= -1
                if col.strength > 1:
                    if col.strength > 2:
                        col.image = pygame.image.load("img/brick2.png")
                    else:
                        col.image = pygame.image.load("img/brick1.png")
                    col.strength -= 1


                else:
                    col.kill()
                    for _ in range(20):
                        particle = Particle(col.rect.x, col.rect.y)
                        all_sprites.add(particle)

        if len(wall.bricks_group) == 0:
            self.game_over = 1
        #kolizja x
        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1
        #kolizja y
        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1
        #kolizja z paletką

        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction*2
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x += -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_r, self.rect.y + self.ball_r), self.ball_r)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_r, self.rect.y + self.ball_r), self.ball_r, 3)

    def reset(self, x, y):
        self.ball_r = 10
        self.x = x - self.ball_r
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_r * 2, self.ball_r * 2)
        self.speed_x = random.randint(-3, 3)
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0







#tworzenie poziomu
def change_lvl(active_lvl):
    if active_lvl == 1:
        wall = Wall1()
    elif active_lvl == 2:
        wall = Wall2()
    elif active_lvl == 3:
        wall = Wall3()

    return wall

#tworzenie paletki
player_paddle = Paddle()
#tworzenie piłki
ball = Game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
wall = change_lvl(active_lvl)


run = True

while run:

    clock.tick(fps)
    # rysowanie tła
    screen.fill(bg)
    if game_paused:
        # draw pause screen buttons
        screen.blit(menu_bg, (0, 0))
        if resume_button.draw(screen):
            game_paused = False
        elif lvl1_button.draw(screen):
            active_lvl = 1
            wall = change_lvl(active_lvl)
        elif lvl2_button.draw(screen):
            active_lvl = 2
            wall = change_lvl(active_lvl)
        elif lvl3_button.draw(screen):
            active_lvl = 3
            wall = change_lvl(active_lvl)
            print("jo")
        elif quit_button.draw(screen):
            run = False

    else:
        all_sprites.update()
        all_sprites.draw(screen)
        #rysowanie
        wall.draw_wall(screen)
        player_paddle.draw()
        ball.draw()

        if live_ball:
            player_paddle.move()
            game_over = ball.move()
            if game_over != 0:
                live_ball = False

        #instrukcje gracza
        if not live_ball:
            if game_over == 0:
                draw_text('Kliknij przycisk SPACJĘ by zacząć', font, text_color, 100, screen_height // 2 + 100)
            elif game_over == 1:
                draw_text('Wygrałeś', font, text_color, 240, screen_height // 2 + 50)

                draw_text('Kliknij przycisk SPACJĘ by zacząć', font, text_color, 100, screen_height // 2 + 100)
            elif game_over == -1:
                draw_text('Przegrałeś', font, text_color, 240, screen_height // 2 + 50)
                draw_text('Kliknij przycisk SPACJĘ by zacząć', font, text_color, 100, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            game_paused = True
        #resetowanie
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and live_ball == False:
            live_ball = True
            if game_over == 1:
                wall.create_wall(wall.brick_map)
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
    pygame.display.update()
pygame.quit()

