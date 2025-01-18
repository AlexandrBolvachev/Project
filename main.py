import sys
import pygame
from random import randrange


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
        self.step = 3

    def left(self):
        self.image = player_image270
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if not other or other.rect.x > self.rect.x:
            self.rect.x -= self.step

    def right(self):
        self.image = player_image90
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if not other or other.rect.x < self.rect.x:
            self.rect.x += self.step

    def up(self):
        self.image = player_image0
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if not other or other.rect.y > self.rect.y:
            self.rect.y -= self.step

    def down(self):
        self.image = player_image180
        other = pygame.sprite.spritecollideany(self, tiles_group)
        if not other or other.rect.y < self.rect.y:
            self.rect.y += self.step

class Missile(pygame.sprite.Sprite):
    def __init__(self, player, pos_x, pos_y):
        super().__init__(missile, all_sprites)



def load_level(screen, level_num):
    tile_type = {'.': 0, 'X': 1, '@': 10}
    new_player, x, y = None, None, None
    all_sprites.empty()
    tiles_group.empty()
    player_group.empty()
    filename = f"levels/level_{level_num:02d}.txt"
    with open(filename, 'r') as mapFile:
        level = [[tile_type[s] for s in line.strip()] for line in mapFile]
    for y in range(len(level)):
        for x in range(len(level[y])):
            screen.blit(tile_images[0], (tile_size * x, tile_size * y + offset))
            if level[y][x] == 10:
                new_player = Player(x, y)
            elif level[y][x]:
                Tile(level[y][x], x, y)
    return new_player, len(level[0]), len(level)


def draw_level(screen):
    screen.fill('black')
    for y in range(level_size_y):
        for x in range(level_size_x):
            screen.blit(tile_images[0], (tile_size * x, tile_size * y + offset))


def start_screen():
    intro_text = ["Правила игры",
                  "Клавиши со стрелками перемещают героя,",
                  "Ваша задача собрать все бонусы"]

    load_level(screen, 0)
    tiles_group.draw(screen)
    font30 = pygame.font.Font(None, 30)
    font90 = pygame.font.Font(None, 90)
    string_rendered = font90.render('Моя игра', 1, 'yellow')
    rect = string_rendered.get_rect()
    rect.centerx = width // 2
    rect.y = 10
    screen.blit(string_rendered, rect)
    text_coord = offset + 130
    for line in intro_text:
        string_rendered = font30.render(line, 1, pygame.Color('yellow'))
        rect = string_rendered.get_rect()
        text_coord += 10
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


if __name__ == '__main__':
    pygame.init()
    size = width, height = 1088, 592
    tile_size = 16
    offset = 80
    FPS = 50
    all_sprites = pygame.sprite.Group()
    tiles_group = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    missile = pygame.sprite.Group()
    PLAYER_UP = pygame.USEREVENT + 1
    PLAYER_DOWN = pygame.USEREVENT + 2
    PLAYER_LEFT = pygame.USEREVENT + 3
    PLAYER_RIGHT = pygame.USEREVENT + 4
    PLAYER_SHOOT = pygame.USEREVENT + 5

    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    player_image0 = load_image('tank0.png', -1)
    player_image90 = load_image('tank90.png', -1)
    player_image180 = load_image('tank180.png', (255, 255, 255))
    player_image270 = load_image('tank270.png', (255, 255, 255))
    tile_images = [load_image('background.png'), load_image('stone.png')]

    start_screen()

    running = True
    player, level_size_x, level_size_y = load_level(screen, 1)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.K_SPACE and event.type == pygame.KEYDOWN:
                pass
            if event.type == PLAYER_LEFT:
                player.left()
            elif event.type == PLAYER_RIGHT:
                player.right()
            elif event.type == PLAYER_UP:
                player.up()
            elif event.type == PLAYER_DOWN:
                player.down()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.left()
                    pygame.time.set_timer(PLAYER_LEFT, 50)
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                    pygame.time.set_timer(PLAYER_UP, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_RIGHT:
                    player.right()
                    pygame.time.set_timer(PLAYER_RIGHT, 50)
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                    pygame.time.set_timer(PLAYER_UP, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_UP:
                    player.up()
                    pygame.time.set_timer(PLAYER_UP, 50)
                    pygame.time.set_timer(PLAYER_LEFT, 0)
                    pygame.time.set_timer(PLAYER_RIGHT, 0)
                    pygame.time.set_timer(PLAYER_DOWN, 0)
                elif event.key == pygame.K_DOWN:
                    player.down()
                    pygame.time.set_timer(PLAYER_DOWN, 50)
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
        clock.tick(50)
    pygame.quit()
