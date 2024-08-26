import pygame
import sys

pygame.init()

# 设置窗口大小
cell_size = 40  # 每个单元格的像素大小
num_cells = 15  # 网格的行数和列数

screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))
pygame.display.set_caption("Pygame Bomberman Map")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)  # 不可破坏的墙壁
RED = (255, 0, 0)  # 玩家颜色
YELLOW = (255, 255, 0)  # 炸弹颜色
GOLD = (255, 215, 0)  # 金色光束的颜色

# 时间控制
enemy_move_delay = 1000  # 敌人每1000毫秒移动一次
last_move_time = pygame.time.get_ticks()

# 玩家初始位置
player_pos = [1, 1]  # 第二行第二列的位置

# 使用预定义的地图数组
map_grid = [
 [0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
 [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
 [1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
 [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
 [0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
 [1, 0, 0, 1, 3, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0],
 [1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1],
 [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1],
 [0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0],
 [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
 [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 5, 1, 1],
 [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
 [1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1],
 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0]
]


# 炸弹列表
bombs = []
# 爆炸效果列表
explosions = []

def draw_grid():
    for x in range(num_cells):
        for y in range(num_cells):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if map_grid[x][y] == 1:
                pygame.draw.rect(screen, GREY, rect)  # 绘制可破坏的砖块
            elif map_grid[x][y] == 3:
                pygame.draw.rect(screen, (0, 0, 255), rect)  # 绘制不可破坏的砖块（蓝色）
            elif map_grid[x][y] == 5:
                pygame.draw.rect(screen, (0, 255, 255), rect)  # 绘制敌人为青色
            else:
                pygame.draw.rect(screen, WHITE, rect)  # 绘制空地
            if x == player_pos[0] and y == player_pos[1]:
                pygame.draw.ellipse(screen, RED, rect)
            pygame.draw.rect(screen, BLACK, rect, 1)  # 绘制网格线
        # 绘制炸弹
    for bomb in bombs:
        if pygame.time.get_ticks() - bomb['time'] < 2000:  # 2秒计时
            bomb_rect = pygame.Rect(bomb['pos'][0] * cell_size, bomb['pos'][1] * cell_size, cell_size, cell_size)
            pygame.draw.ellipse(screen, YELLOW, bomb_rect)
        else:
            explode_bomb(bomb)
    # 绘制金色光束
    current_time = pygame.time.get_ticks()
    for explosion in explosions[:]:
        if current_time < explosion['end_time']:
            for (ex, ey) in explosion['tiles']:
                rect = pygame.Rect(ex * cell_size, ey * cell_size, cell_size, cell_size)
                pygame.draw.rect(screen, GOLD, rect)
        else:
            explosions.remove(explosion)

def explode_bomb(bomb):
    if bomb not in bombs:
        return  # 如果炸弹已经不在列表中，直接返回

    x, y = bomb['pos']
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四个主要方向
    affected_tiles = [(x, y)]
    immediate_explosions = []

    for dx, dy in directions:
        for step in range(1, 3):  # 检查距离为1和2的格子
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < num_cells and 0 <= ny < num_cells:
                if map_grid[nx][ny] == 3: # 遇到蓝色砖块，停止这个方向的破坏
                    break
                affected_tiles.append((nx, ny))
                if map_grid[nx][ny] == 1: # 灰色砖块被破坏
                    map_grid[nx][ny] = 0

                # 检查是否触及其他炸弹
                for other_bomb in bombs:
                    if other_bomb['pos'] == [nx, ny] and other_bomb not in immediate_explosions:
                        immediate_explosions.append(other_bomb)
            else:
                break # 超出边界也停止检查

    bombs.remove(bomb)
    # 记录爆炸效果和持续时间
    explosions.append({'tiles': affected_tiles, 'end_time': pygame.time.get_ticks() + 500}) # 保持500毫秒


    # 立即引爆触及的炸弹
    for bomb_to_explode in immediate_explosions:
        explode_bomb(bomb_to_explode)

def move_player(dx, dy):
    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
        player_pos[0] = new_x
        player_pos[1] = new_y

def place_bomb():
    if map_grid[player_pos[0]][player_pos[1]] == 0:
        bombs.append({'pos': player_pos.copy(), 'time': pygame.time.get_ticks()})

def move_enemy():
    global last_move_time
    new_positions = []
    current_time = pygame.time.get_ticks()
    if current_time - last_move_time > enemy_move_delay:
        # 在这里执行敌人的移动逻辑
        last_move_time = current_time
    # Step 1: Find all enemies and determine new positions
        for x in range(num_cells):
            for y in range(num_cells):
                if map_grid[x][y] == 5:  # Assuming 5 is the enemy marker
                    dx, dy = 0, 0
                    # Determine movement direction based on player position
                    if x < player_pos[0]:
                        dx = 1
                    elif x > player_pos[0]:
                        dx = -1

                    if y < player_pos[1]:
                        dy = 1
                    elif y > player_pos[1]:
                        dy = -1

                    # Calculate new position
                    new_x, new_y = x + dx, y + dy

                    # Check if the new position is within bounds and is empty
                    if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
                        new_positions.append((new_x, new_y, x, y))

        # Step 2: Update the map grid with new enemy positions
        for new_x, new_y, old_x, old_y in new_positions:
            map_grid[old_x][old_y] = 0  # Set old position to empty
            map_grid[new_x][new_y] = 5  # Move enemy to new position


clock = pygame.time.Clock()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_player(-1, 0)
            elif event.key == pygame.K_RIGHT:
                move_player(1, 0)
            elif event.key == pygame.K_UP:
                move_player(0, -1)
            elif event.key == pygame.K_DOWN:
                move_player(0, 1)
            elif event.key == pygame.K_SPACE:
                place_bomb()

    screen.fill(BLACK)  # 设置背景颜色
    move_enemy()  # Update enemy position based on player position
    draw_grid()
    pygame.display.flip()
    clock.tick(60)  # 控制游戏帧率

pygame.quit()
sys.exit()