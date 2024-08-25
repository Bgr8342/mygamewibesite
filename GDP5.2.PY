import pygame
import heapq
import sys
import random

pygame.init()

# 设置窗口大小
cell_size = 40
num_cells = 15

screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))
pygame.display.set_caption("Pygame Bomberman Map")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GOLD = (255, 215, 0)
SLATE_GRAY = (112, 128, 144)
BROWN = (139, 69, 19)
CYAN = (0, 255, 255)  # 敌人的颜色
BLUE = (0, 0, 255)  # 不可破坏的砖块颜色

# 时间控制
enemy_move_delay = 300
player_move_delay = 200
bomb_place_delay = 200
enemy_bomb_place_delay = 2000

# 玩家 初始位置
player_pos = [7, 7]
player_lives = 9

# 敌人初始状态
enemy_pos = None
enemy_lives = None

last_player_move_time = pygame.time.get_ticks()
last_bomb_place_time = pygame.time.get_ticks()
last_enemy_bomb_place_time = pygame.time.get_ticks()
last_move_time = pygame.time.get_ticks()

map_grid = [
    [5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 1, 1, 1, 1, 1, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 1, 0, 0, 0, 1, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 1, 1, 1, 1, 1, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 4, 0],
    [0, 4, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 4, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
    [0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


# A* 算法定义
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def a_star_search(map_grid, start, goal):
    neighbors = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, goal)}
    oheap = []
    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == goal:
            data = []
            while current in came_from:
                data.append(current)
                current = came_from[current]
            return data[::-1]

        close_set.add(current)
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j
            if 0 <= neighbor[0] < num_cells and 0 <= neighbor[1] < num_cells:
                if map_grid[neighbor[0]][neighbor[1]] != 0:
                    continue

                tentative_g_score = gscore[current] + 1
                if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                    continue

                if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                    came_from[neighbor] = current
                    gscore[neighbor] = tentative_g_score
                    fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return False

# 炸弹列表
bombs = []
# 爆炸效果列表
explosions = []

def draw_tile(x, y, rect):
    if map_grid[x][y] == 1:
        pygame.draw.rect(screen, GREY, rect)  # 绘制可破坏的砖块
    elif map_grid[x][y] == 2:
        pygame.draw.rect(screen, BLUE, rect)  # 绘制不可破坏的砖块
    elif map_grid[x][y] == 3:
        pygame.draw.rect(screen, SLATE_GRAY, rect)  # 绘制Slate_Gray砖块
    elif map_grid[x][y] == 4:
        pygame.draw.rect(screen, BROWN, rect)  # 绘制灰褐色砖块
    elif map_grid[x][y] == 5:
        pygame.draw.rect(screen, CYAN, rect)  # 绘制敌人为青色
    else:
        pygame.draw.rect(screen, WHITE, rect)  # 绘制空地
    pygame.draw.rect(screen, BLACK, rect, 1)  # 绘制网格线

def draw_grid():
    for x in range(num_cells):
        for y in range(num_cells):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            draw_tile(x, y, rect)

    # 绘制玩家
    player_rect = pygame.Rect(player_pos[0] * cell_size, player_pos[1] * cell_size, cell_size, cell_size)
    pygame.draw.ellipse(screen, RED, player_rect)

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

    # 显示玩家生命值
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player_lives}", True, BLACK)
    screen.blit(lives_text, (10, 10))

    # 显示敌人生命值
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {enemy_lives}", True, BLACK)
    screen.blit(lives_text, (500, 10))

def process_tile_destruction(nx, ny):
    if map_grid[nx][ny] == 4:  # 检查灰褐色砖块
        map_grid[nx][ny] = 3  # 降级为Slate_Gray砖块
        return True  # 阻挡爆炸继续穿透
    elif map_grid[nx][ny] == 3:  # 检查Slate_Gray砖块
        map_grid[nx][ny] = 1  # 降级为普通灰色砖块
        return True  # 阻挡爆炸继续穿透
    elif map_grid[nx][ny] == 1:  # 检查普通灰色砖块
        map_grid[nx][ny] = 0  # 被炸毁变为空地
        return True  # 阻挡爆炸继续穿透
    elif map_grid[nx][ny] == 2:  # 遇到不可破坏的蓝色砖块
        return True  # 阻挡爆炸继续穿透
    return False  # 空地或其他情况，允许爆炸继续传播

def explode_bomb(bomb):
    global player_lives, enemy_lives, enemy_pos
    if bomb not in bombs:
        return

    x, y = bomb['pos']
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四个主要方向
    affected_tiles = []
    immediate_explosions = []

    for dx, dy in directions:
        for step in range(1, 3):  # 检查距离为1到4的格子
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < num_cells and 0 <= ny < num_cells:
                if process_tile_destruction(nx, ny):
                    break  # 阻挡爆炸继续穿透
                affected_tiles.append((nx, ny))

                # 检查是否触及其他炸弹
                for other_bomb in bombs:
                    if other_bomb['pos'] == [nx, ny] and other_bomb not in immediate_explosions:
                        immediate_explosions.append(other_bomb)
            else:
                break  # 超出边界也停止检查

    bombs.remove(bomb)
    explosions.append({'tiles': affected_tiles, 'end_time': pygame.time.get_ticks() + 500})

    # 检查玩家是否在爆炸范围内
    if tuple(player_pos) in affected_tiles:
        if player_lives < 10:  # 生命值为10时无敌，不减少生命值
            player_lives -= 1
            if player_lives <= 0:
                print("游戏结束！")
                pygame.quit()
                sys.exit()

    # 检查敌人是否在爆炸范围内
    if enemy_pos is not None and tuple(enemy_pos) in affected_tiles:
        if enemy_lives is not None:
            if enemy_lives < 10: # 5 表示无敌
                if enemy_lives <= 0:
                    print("敌人被击败！")
                    map_grid[enemy_pos[0]][enemy_pos[1]] = 0
                    enemy_pos = None
                else:
                    enemy_lives -= 1
                    if enemy_lives <= 0:
                        print("敌人被击败！")
                        map_grid[enemy_pos[0]][enemy_pos[1]] = 0
                        enemy_pos = None
        else:
            enemy_lives = 0

    # 立即引爆触及的其他炸弹
    for bomb_to_explode in immediate_explosions:
        explode_bomb(bomb_to_explode)

def move_player(dx, dy):
    global last_player_move_time, player_pos
    current_time = pygame.time.get_ticks()
    if current_time - last_player_move_time < player_move_delay:
        return

    new_x, new_y = player_pos[0] + dx, player_pos[1] + dy
    if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
        player_pos[0] = new_x
        player_pos[1] = new_y

    last_player_move_time = current_time

def place_bomb():
    global last_bomb_place_time
    current_time = pygame.time.get_ticks()
    if current_time - last_bomb_place_time < bomb_place_delay:
        return

    if map_grid[player_pos[0]][player_pos[1]] == 0 and not any(bomb['pos'] == player_pos for bomb in bombs):
        bombs.append({'pos': player_pos.copy(), 'time': pygame.time.get_ticks()})
        last_bomb_place_time = current_time

def enemy_place_bomb():
    global last_enemy_bomb_place_time
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
        bombs.append({'pos': enemy_pos.copy(), 'time': pygame.time.get_ticks()})
        last_enemy_bomb_place_time = current_time

def find_enemy_position(map_grid):
    for x in range(num_cells):
        for y in range(num_cells):
            if map_grid[x][y] == 5:
                return [x, y]
    return None

# 在主程序中初始化
enemy_pos = find_enemy_position(map_grid)
if enemy_pos is None:
    print("No enemy found on the map")
    sys.exit(1)

# 敌人移动逻辑
enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))
path_update_delay = 3000
last_path_update_time = pygame.time.get_ticks()

def move_enemy():
    global enemy_pos, enemy_path, last_move_time, last_path_update_time, player_lives
    current_time = pygame.time.get_ticks()

    if enemy_pos is None:
        return

    if current_time - last_move_time > enemy_move_delay:
        enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))

        if enemy_path:
            next_pos = enemy_path.pop(0)
            map_grid[enemy_pos[0]][enemy_pos[1]] = 0
            enemy_pos = list(next_pos)
            map_grid[enemy_pos[0]][enemy_pos[1]] = 5
            last_move_time = current_time

            if enemy_pos == player_pos:
                if player_lives < 10:
                    print("无敌敌人碰到玩家，游戏结束！")
                    pygame.quit()
                    sys.exit()
                else:
                    pass

            if current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
                enemy_place_bomb()

        else:
            random_move_enemy()
            if current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
                enemy_place_bomb()

def random_move_enemy():
    global enemy_pos, last_move_time
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time < enemy_move_delay:
        return

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)
    for dx, dy in directions:
        new_x, new_y = enemy_pos[0] + dx, enemy_pos[1] + dy
        if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
            map_grid[enemy_pos[0]][enemy_pos[1]] = 0
            enemy_pos = [new_x, new_y]
            map_grid[enemy_pos[0]][enemy_pos[1]] = 5
            last_move_time = current_time
            break

last_player_pos = player_pos[:]

def update_game_state():
    global last_player_pos, enemy_path
    if player_pos != last_player_pos:
        enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))
        last_player_pos = player_pos[:]

clock = pygame.time.Clock()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                place_bomb()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        move_player(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move_player(1, 0)
    elif keys[pygame.K_UP]:
        move_player(0, -1)
    elif keys[pygame.K_DOWN]:
        move_player(0, 1)

    if keys[pygame.K_SPACE]:
        place_bomb()

    screen.fill(BLACK)
    move_enemy()
    draw_grid()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
