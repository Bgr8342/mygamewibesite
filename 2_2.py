import pygame
import time
import random
# 初始化 Pygame
pygame.init()

pygame.font.init()
pygame.mixer.init()


pygame.mixer.music.load('/build/web/msc/let-the-games-begin.mp3')
pygame.mixer.music.play(-1)  # '-1' 表示无限循环播放音乐


# 设置窗口大小
WIDTH, HEIGHT = 600, 375
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Dodge')


# 加载图片并调整大小
BG = pygame.transform.scale(pygame.image.load(r'C:\Users\ThinkPad\PycharmProjects\pythonCrawler\pythonProject\img\space_background.png'), (WIDTH, HEIGHT))


# 游戏参数
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_speed = 5
STAR_WIDTH = 10
STAR_HEIGHT = 20
FONT = pygame.font.SysFont('Comic Sans MS', 30)
BUTTON_FONT = pygame.font.SysFont('Comic Sans MS', 20)
star_speed = 3


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

    # 增加垂直移动变量
    timer_x = WIDTH // 2
    timer_y = HEIGHT // 2
    timer_speed_x = 2
    timer_speed_y = 2
    timer_direction_x = 1  # 水平方向：1 为向右，-1 为向左
    timer_direction_y = 1  # 垂直方向：1 为向下，-1 为向上

    while not hit:
        clock.tick(88)
        total_elapsed_time = time.time() - game_start_time
        elapsed_time = time.time() - star_time

        # 更新计时器位置
        timer_x += timer_speed_x * timer_direction_x
        timer_y += timer_speed_y * timer_direction_y

        # 水平方向边界处理
        if timer_x > WIDTH - 127.5 or timer_x < 0:
            timer_direction_x *= -1

        # 垂直方向边界处理
        if timer_y > HEIGHT - 50 or timer_y < 0:
            timer_direction_y *= -1

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
            pygame.time.delay(1888)
            break

        draw(player, total_elapsed_time, stars, timer_x, timer_y)

    pygame.quit()

def draw(player, elapsed_time, stars, timer_x, timer_y):
    # 绘制调整后的背景
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f'Time: {int(elapsed_time)}s', 1, (255, 255, 255))
    WIN.blit(time_text, (timer_x, timer_y))  # 使用 timer_x 和 timer_y 作为坐标
    pygame.draw.rect(WIN, (36, 36, 36), player)
    for star in stars:
        pygame.draw.rect(WIN, 'white', star)
    pygame.display.update()


if __name__ == '__main__':
    main_menu()