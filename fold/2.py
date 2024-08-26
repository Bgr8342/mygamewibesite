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

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
player_speed = 5
#elapsed_time = 0
#star_count = 0
STAR_WIDTH = 10
STAR_HEIGHT = 20
FONT = pygame.font.SysFont('Comic Sans MS', 30)
hit = False
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

def main():
    # 初始化游戏和计时器
    player = pygame.Rect(280, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    stars = []
    star_add_increment = 2000
    clock = pygame.time.Clock()
    game_start_time = time.time()  # 游戏开始的总时间
    star_time  = time.time()  # 控制星星生成的计时器
    hit = False

    while not hit:
        clock.tick(60)
        total_elapsed_time = time.time() - game_start_time
        elapsed_time = time.time() - star_time

        if elapsed_time * 1000 > star_add_increment:  # 将秒转换为毫秒来比较

            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)
            star_time = time.time()
            #这行代码的目的是每次执行时将star_add_increment减少50，但不允许它低于200。
            star_add_increment = max(200, star_add_increment - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player_speed >= 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.x + player_speed <= WIDTH - PLAYER_WIDTH:
            player.x += player_speed

        #进行列表复制，这样可以在star碰到底线时删除，也不会影响上面的表格
        for star in stars[:]:
            star.y += star_speed
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit = True
                print("Collision Detected! Game Over.")
                break
        if hit:
            lost_text = FONT.render('You Lost!', 1, (255, 255, 255))
            # 正确居中文本
            text_x = WIDTH / 2 - lost_text.get_width() / 2
            text_y = HEIGHT / 2 - lost_text.get_height() / 2
            WIN.blit(lost_text, (text_x, text_y))
            pygame.display.update()
            pygame.time.delay(4000)  # 游戏结束后停留4秒



        draw(player, total_elapsed_time, stars)

    pygame.quit()

if __name__ == '__main__':
    main()


