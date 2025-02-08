import sys
from random import randrange

import pygame


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = 'pics/' + name
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Невозможно загрузить картинку:', fullname)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_num, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_num]
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image0
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)
        self.step = 2


    def left(self):
        self.image = player_image270
        collide = pygame.sprite.spritecollideany(self, enemy_group)
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if collide:
            collide.move()
        elif not other or other.rect.x > self.rect.x:
            self.rect.x -= self.step

    def right(self):
        self.image = player_image90
        collide = pygame.sprite.spritecollideany(self, enemy_group)
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if collide:
            collide.move()
        elif not other or other.rect.x < self.rect.x:
            self.rect.x += self.step

    def up(self):
        self.image = player_image0
        collide = pygame.sprite.spritecollideany(self, enemy_group)
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if collide:
            collide.move()
        elif not other or other.rect.y > self.rect.y:
            self.rect.y -= self.step

    def down(self):
        self.image = player_image180
        collide = pygame.sprite.spritecollideany(self, enemy_group)
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if collide:
            collide.move()
        elif not other or other.rect.y < self.rect.y:
            self.rect.y += self.step

    def coords(self):
        return self.rect

    def hit(self):
        hp[hp.count(1) - 1] = 0


class Missile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, size_x, size_y, rotate):
        self.side_shoot = rotate
        self.pos_x, self.pos_y, self.size_x, self.size_y = pos_x, pos_y, size_x, size_y
        super().__init__(missile_group, all_sprites)
        self.get_image1()
        self.get_rect1()
        self.step = 5

    def get_rect1(self):
        if self.side_shoot == 0:
            self.rect = self.image.get_rect().move(self.pos_x + self.size_x // 2 - 5, self.pos_y - 20)
        elif self.side_shoot == 90:
            self.rect = self.image.get_rect().move(self.pos_x + self.size_x, self.pos_y + self.size_y // 2 - 5)
        elif self.side_shoot == 180:
            self.rect = self.image.get_rect().move(self.pos_x + self.size_x // 2 - 5, self.pos_y + self.size_y)
        elif self.side_shoot == 270:
            self.rect = self.image.get_rect().move(self.pos_x - 20, self.pos_y + self.size_y // 2 - 5)

    def get_image1(self):
        if self.side_shoot == 0:
            self.image = missile_image0
        elif self.side_shoot == 90:
            self.image = missile_image90
        elif self.side_shoot == 180:
            self.image = missile_image180
        elif self.side_shoot == 270:
            self.image = missile_image270

    def check(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.kill()
            return 0
        tank = pygame.sprite.spritecollideany(self, enemy_group)
        if tank:
            self.kill()
            tank.hit()
            return 0
        col = pygame.sprite.spritecollideany(self, player_group)
        if col:
            self.kill()
            col.hit()
            return 0
        return 1

    def update(self, *args, **kwargs):
        if self.check():
            if self.side_shoot == 0:
                self.rect.y -= self.step
            elif self.side_shoot == 90:
                self.rect.x += self.step
            elif self.side_shoot == 180:
                self.rect.y += self.step
            elif self.side_shoot == 270:
                self.rect.x -= self.step


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, rot):
        super().__init__(all_sprites, enemy_group)
        self.shot = randrange(11)
        self.step = 2
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.rot = rot
        self.hp = 3
        self.get_image1()
        self.rect = self.image.get_rect().move(
            tile_size * pos_x, tile_size * pos_y + offset)

    def get_image1(self):
        if self.rot == 0:
            self.image = enemy_image0
        elif self.rot == 90:
            self.image = enemy_image90
        elif self.rot == 180:
            self.image = enemy_image180
        elif self.rot == 270:
            self.image = enemy_image270

    def shoot(self):
        self.shot = (self.shot + 1) % 10
        if self.shot == 0:
            Missile(self.rect.x, self.rect.y, self.rect.w, self.rect.h, self.rot)

    def move(self):
        self.step = -self.step

    def hit(self):
        global cnt_enemy_destroyed
        self.hp -= 1
        if self.hp == 0:
            cnt_enemy_destroyed += 1
            self.kill()

    def update(self, *args, **kwargs):
        # collide = pygame.sprite.spritecollideany(self, player_group)
        col = pygame.sprite.spritecollideany(self, enemy_group)
        # if collide:
        #     self.move()
        if col:
            self.move()
            col.move()
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.move()
        if self.rot == 0 or self.rot == 180:
            self.rect.x += self.step
        else:
            self.rect.y += self.step


def load_level(screen, level_num):
    tile_type = {'.': 0, 'X': 1, '@': 10, '{': 11, 'T': 12, '}': 13, 'L': 14}
    new_player, x, y = None, None, None
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    missile_group.empty()
    enemy_group.empty()
    hp.clear()
    for _ in range(hit_points - level_num + 1):
        hp.append(1)
    filename = f"levels/level_{level_num:02d}.txt"
    with open(filename, 'r') as mapFile:
        level = [[tile_type[s] for s in line.strip()] for line in mapFile]
    for y in range(len(level)):
        for x in range(len(level[y])):
            screen.blit(tile_images[0], (tile_size * x, tile_size * y + offset))
            if level[y][x] == 10:
                new_player = Player(x, y)
            elif level[y][x] == 11:
                Enemy(x, y, 270)
            elif level[y][x] == 12:
                Enemy(x, y, 180)
            elif level[y][x] == 13:
                Enemy(x, y, 90)
            elif level[y][x] == 14:
                Enemy(x, y, 0)
            elif level[y][x]:
                Tile(level[y][x], x, y)
    return new_player, len(level[0]), len(level)


def draw_level(screen):
    screen.fill('black')
    for y in range(level_size_y):
        for x in range(level_size_x):
            screen.blit(tile_images[0], (tile_size * x, tile_size * y + offset))
    for i in range(len(control)):
        screen.blit(control[i], (width // 2 + 100 + 70 * i, offset // 2 - 28))
    health()


def start_screen():
    intro_text = ["Правила игры",
                  "Клавиши со стрелками перемещают танк,",
                  "Пробел - стрельба,",
                  "Ваша задача уничтожить все танки",
                  "Нажмите любую кнопку для продолжения"]

    screen.fill('black')
    load_level(screen, 0)
    tiles_group.draw(screen)
    font30 = pygame.font.Font(None, 30)
    font90 = pygame.font.Font(None, 90)
    string_rendered = font90.render('Battle of tanks', 1, 'yellow')
    rect = string_rendered.get_rect()
    rect.centerx = width // 2
    rect.y = 10
    screen.blit(string_rendered, rect)
    text_coord = offset + 130
    for line in intro_text[:-1]:
        string_rendered = font30.render(line, 1, pygame.Color('yellow'))
        rect = string_rendered.get_rect()
        text_coord += 10
        rect.top = text_coord
        rect.centerx = width // 2
        text_coord += rect.height
        screen.blit(string_rendered, rect)
    string_rendered = font30.render(intro_text[-1], 1, pygame.Color('white'))
    rect = string_rendered.get_rect()
    text_coord += 100
    rect.top = text_coord
    rect.centerx = width // 2
    text_coord += rect.height
    screen.blit(string_rendered, rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


def gameover():
    pygame.time.set_timer(PLAYER_UP, 0)
    pygame.time.set_timer(PLAYER_DOWN, 0)
    pygame.time.set_timer(PLAYER_LEFT, 0)
    pygame.time.set_timer(PLAYER_RIGHT, 0)
    pygame.time.set_timer(ENEMY_SHOOT, 0)
    r = pygame.Surface(size, pygame.SRCALPHA)
    r.fill((0, 0, 0, 230))
    screen.blit(r, (0, 0))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)

def last_screen():
    pass



def health():
    for i in range(min(len(hp), 10)):
        if hp[i]:
            screen.blit(hp1, (48 * i, 0))
        else:
            screen.blit(hp0, (48 * i, 0))


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1088, 592
    tile_size = 16
    offset = 80
    FPS = 50
    missile_ready = 1
    enemy_shoot = 0
    lvl_num = 1

    rotate = 0
    hit_points = 3
    hp = []

    # статистика

    cnt_hits = 0
    cnt_shots_fire = 0
    cnt_enemy_destroyed = 0

    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    missile_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    PLAYER_UP = pygame.USEREVENT + 1
    PLAYER_DOWN = pygame.USEREVENT + 2
    PLAYER_LEFT = pygame.USEREVENT + 3
    PLAYER_RIGHT = pygame.USEREVENT + 4
    ENEMY_SHOOT = pygame.USEREVENT + 5
    PLAYER_RELOAD = pygame.USEREVENT + 6

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()

    player_image0 = load_image('tank0.png', (255, 255, 255))
    player_image90 = load_image('tank90.png', (255, 255, 255))
    player_image180 = load_image('tank180.png', (255, 255, 255))
    player_image270 = load_image('tank270.png', (255, 255, 255))

    missile_image0 = load_image('missile0.png', (255, 255, 255))
    missile_image90 = load_image('missile90.png', (255, 255, 255))
    missile_image180 = load_image('missile180.png', (255, 255, 255))
    missile_image270 = load_image('missile270.png', (255, 255, 255))

    enemy_image0 = load_image('enemy0.png', (255, 255, 255))
    enemy_image90 = load_image('enemy90.png', (255, 255, 255))
    enemy_image180 = load_image('enemy180.png', (255, 255, 255))
    enemy_image270 = load_image('enemy270.png', (255, 255, 255))

    hp1 = load_image('hp1.png', (255, 255, 255))
    hp0 = load_image('hp0.png', (255, 255, 255))
    control = [
        load_image('down.png', -1), load_image('up.png', -1),
        load_image('left.png', -1), load_image('right.png', -1),
        load_image('space.png', -1)
    ]
    tile_images = [load_image('background.png'), load_image('stone.png')]

    start_screen()

    running = True
    player, level_size_x, level_size_y = load_level(screen, lvl_num)
    enemy_shoot_flag = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if hp.count(1) == 0:
                gameover()
                lvl_num = 0
                start_screen()
                player, level_size_x, level_size_y = load_level(screen, lvl_num)
                enemy_shoot_flag = True

            if enemy_shoot_flag:
                pygame.time.set_timer(ENEMY_SHOOT, 200)
                enemy_shoot_flag = False

            if len(enemy_group) == 0:
                lvl_num += 1
                if lvl_num == 4:
                    lvl_num = 0
                    last_screen()
                else:
                    gameover()
                    player, level_size_x, level_size_y = load_level(screen, lvl_num)
                    enemy_shoot_flag = True
            if event.type == ENEMY_SHOOT:
                for sprite in enemy_group:
                    sprite.shoot()
                pygame.time.set_timer(ENEMY_SHOOT, 200)
            if event.type == PLAYER_RELOAD:
                missile_ready = 1
            if event.type == PLAYER_LEFT:
                rotate = 270
                player.left()
            elif event.type == PLAYER_RIGHT:
                rotate = 90
                player.right()
            elif event.type == PLAYER_UP:
                rotate = 0
                player.up()
            elif event.type == PLAYER_DOWN:
                rotate = 180
                player.down()
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and missile_ready:
                    cnt_shots_fire += 1
                    Missile(*player.coords(), rotate)
                    pygame.time.set_timer(PLAYER_RELOAD, 2000)
                    missile_ready = 0
                if event.key == pygame.K_LEFT:
                    rotate = 270
                    player.left()
                    pygame.time.set_timer(PLAYER_LEFT, 17)
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                    pygame.time.set_timer(PLAYER_UP, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_RIGHT:
                    rotate = 90
                    player.right()
                    pygame.time.set_timer(PLAYER_RIGHT, 17)
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                    pygame.time.set_timer(PLAYER_UP, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_UP:
                    rotate = 0
                    player.up()
                    pygame.time.set_timer(PLAYER_UP, 17)
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_DOWN:
                    rotate = 180
                    player.down()
                    pygame.time.set_timer(PLAYER_DOWN, 17)
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                    pygame.time.set_timer(PLAYER_UP, 0)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                elif event.key == pygame.K_RIGHT:
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                elif event.key == pygame.K_UP:
                    pygame.time.set_timer(PLAYER_UP, 0)
                elif event.key == pygame.K_DOWN:
                    pygame.time.set_timer(PLAYER_DOWN, 0)

        draw_level(screen)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()
