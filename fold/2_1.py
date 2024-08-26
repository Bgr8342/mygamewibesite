import pygame
import time
import random
pygame.font.init()

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 600, 375
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')

# 加载图片并调整大小
BG = pygame.transform.scale(pygame.image.load('../img/space_background.png'), (WIDTH, HEIGHT))

# 游戏参数
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_speed = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
FONT = pygame.font.SysFont('Comic Sans MS', 30)
BUTTON_FONT = pygame.font.SysFont('Comic Sans MS', 20)
star_speed = 3
def draw(player, elapsed_time, stars):
    # 绘制调整后的背景
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {int(elapsed_time)}s', 1, (255, 255, 255))
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, 'red', player)
    for star in stars:
        pygame.draw.rect(WIN, 'white', star)
    pygame.display.update()


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

def main_menu():
    while True:
        WIN.fill((0,0,0))
        draw_text('Test of Luck and Skill', FONT, (255, 255, 255), WIN, 20, 20)
        draw_text('The Unbeatable 50 Seconds', FONT, (255, 255, 255), WIN, 20, 60)
        draw_text('Best Record:', FONT, (255, 255, 255), WIN, 20, 100)
        draw_text('The author himself: 52 Seconds', FONT, (255, 255, 255), WIN, 20, 140)
        draw_text('Click to Start', BUTTON_FONT, (255, 0, 0), WIN, 250, 300)

        mx, my = pygame.mouse.get_pos()

        button = pygame.Rect(250, 300, 200, 50)
        if button.collidepoint((mx, my)):
            if pygame.mouse.get_pressed()[0] == 1:
                game()
                break

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

def game():
    player = pygame.Rect(280, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    stars = []
    star_add_increment = 2000
    clock = pygame.time.Clock()
    game_start_time = time.time()
    star_time = time.time()
    hit = False

    while not hit:
        clock.tick(60)
        total_elapsed_time = time.time() - game_start_time
        elapsed_time = time.time() - star_time

        if elapsed_time * 1000 > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_time = time.time()
            star_add_increment = max(200, star_add_increment - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_speed >= 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player_speed <= WIDTH - PLAYER_WIDTH:
            player.x += player_speed

        for star in stars[:]:
            star.y += star_speed
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                break
        if hit:
            lost_text = FONT.render('You Lost!', 1, (255, 255, 255))
            text_x = WIDTH / 2 - lost_text.get_width() / 2
            text_y = HEIGHT / 2 - lost_text.get_height() / 2
            WIN.blit(lost_text, (text_x, text_y))
            pygame.display.update()
            pygame.time.delay(4000)
            break

        draw(player, total_elapsed_time, stars)

    pygame.quit()

if __name__ == '__main__':
    main_menu()
