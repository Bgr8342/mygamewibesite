import pygame
import heapq
import sys
import random
import asyncio

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
SAPPHIRE = (15, 82, 186)  # 蓝宝石颜色


# 敌人类型的颜色
ENEMY_COLOR_1 = (255, 69, 0)    # 橙色
ENEMY_COLOR_2 = (0, 191, 255)   # 深天蓝
ENEMY_COLOR_3 = (144, 238, 144) # 浅绿色
ENEMY_COLOR_4 = (148, 0, 211)   # 深紫罗兰

# 定义敌人类型
#可以放置炸弹 + 可以被击杀 橙色
enemy_type_1 = {
    'pos': [0, 0],  # 初始位置可根据需要更改
    'lives': random.randint(1, 9),  # 1到9之间的生命值
    'last_move_time': pygame.time.get_ticks(),
    'last_bomb_place_time': pygame.time.get_ticks(),
    'can_place_bombs': True,  # 可以放置炸弹
    'color': ENEMY_COLOR_1  # 橙色
}
#可以放置炸弹 + 无敌 深天蓝
enemy_type_2 = {
    'pos': [0, 14],  # 初始位置可根据需要更改
    'lives': 10,  # 无敌
    'last_move_time': pygame.time.get_ticks(),
    'last_bomb_place_time': pygame.time.get_ticks(),
    'can_place_bombs': True,  # 可以放置炸弹
    'color': ENEMY_COLOR_2  # 深天蓝
}
#不可以放置炸弹 + 可以被击杀 浅绿色
enemy_type_3 = {
    'pos': [14, 0],  # 初始位置可根据需要更改
    'lives': random.randint(1, 9),  # 1到9之间的生命值
    'last_move_time': pygame.time.get_ticks(),
    'last_bomb_place_time': None,  # 不放置炸弹
    'can_place_bombs': False,  # 不可以放置炸弹
    'color': ENEMY_COLOR_3  # 浅绿色
}
#不可以放置炸弹 + 无敌 深紫罗兰
enemy_type_4 = {
    'pos': [14, 14],  # 初始位置可根据需要更改
    'lives': 10,  # 无敌
    'last_move_time': pygame.time.get_ticks(),
    'last_bomb_place_time': None,  # 不放置炸弹
    'can_place_bombs': False,  # 不可以放置炸弹
    'color': ENEMY_COLOR_4  # 深紫罗兰
}

# 示例关卡敌人
enemies_list = [
    enemy_type_1.copy(),#可以放置炸弹 + 可以被击杀 橙色
    enemy_type_2.copy(),#可以放置炸弹 + 无敌 深天蓝
    enemy_type_3.copy(),#不可以放置炸弹 + 可以被击杀 浅绿色
    enemy_type_4.copy() #不可以放置炸弹 + 无敌 深紫罗兰
]

# 为每个敌人设置不同的位置
#enemies[0]['pos'] = [0, 0]
#enemies[1]['pos'] = [0, 14]
enemies_list[2]['pos'] = [14, 2]
#enemies[3]['pos'] = [14, 14]


# 时间控制
enemy_move_delay = 300
player_move_delay = 200
bomb_place_delay = 200
enemy_bomb_place_delay = 2000
# 玩家 初始位置
player_pos = [5, 12]
player_lives = 9

# 敌人初始状态
enemy_pos = None
enemy_lives = None  # 初始生命值为 None

enemies_list_two = [
    {'pos': [0, 0], 'lives': None, 'last_move_time': pygame.time.get_ticks(), 'last_bomb_place_time': pygame.time.get_ticks()},
    {'pos': [0, 14], 'lives': None, 'last_move_time': pygame.time.get_ticks(), 'last_bomb_place_time': pygame.time.get_ticks()},
    {'pos': [14, 0], 'lives': None, 'last_move_time': pygame.time.get_ticks(), 'last_bomb_place_time': pygame.time.get_ticks()},
    # 可以根据需要添加更多敌人
]


last_player_move_time = pygame.time.get_ticks()
last_bomb_place_time = pygame.time.get_ticks()
last_enemy_bomb_place_time = pygame.time.get_ticks()
last_move_time = pygame.time.get_ticks()


# 使用预定义的地图数组
map_grid_third = [
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1]
]

map_grid_second = [
    [4, 3, 1, 2, 3, 1, 4, 0, 4, 1, 3, 2, 1, 3, 4],
    [3, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 3],
    [1, 0, 4, 0, 1, 4, 0, 3, 0, 4, 1, 0, 4, 0, 1],
    [2, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 2],
    [3, 3, 1, 0, 4, 0, 4, 0, 4, 0, 4, 0, 1, 3, 3],
    [1, 0, 4, 1, 0, 3, 0, 1, 0, 3, 0, 1, 4, 0, 1],
    [4, 1, 0, 4, 3, 0, 1, 4, 1, 0, 3, 4, 0, 1, 4],
    [0, 4, 3, 1, 0, 4, 0, 0, 0, 4, 0, 1, 3, 4, 0],
    [4, 1, 0, 4, 3, 0, 1, 4, 1, 0, 3, 4, 0, 1, 4],
    [1, 0, 4, 1, 0, 3, 0, 1, 0, 3, 0, 1, 4, 0, 1],
    [3, 3, 1, 0, 4, 0, 4, 0, 4, 0, 4, 0, 1, 3, 3],
    [2, 1, 0, 1, 3, 0, 1, 4, 1, 5, 3, 1, 0, 1, 2],
    [1, 0, 4, 0, 1, 4, 0, 3, 0, 4, 1, 0, 4, 0, 1],
    [3, 1, 0, 1, 3, 0, 1, 4, 1, 0, 3, 1, 0, 1, 3],
    [4, 3, 1, 2, 3, 1, 4, 0, 4, 1, 3, 2, 1, 3, 4]
]

map_grid_final = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
[0, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]

# 地图配置
map_grid_first = [
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

map_grid_esther = [
    [3, 3, 3, 0, 1, 0, 3, 1, 1, 1, 1, 0, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 3, 0, 0, 3, 1, 1, 4, 2, 1],
    [3, 0, 2, 2, 0, 3, 3, 1, 1, 1, 0, 1, 4, 2, 1],
    [3, 0, 4, 1, 1, 1, 3, 1, 1, 1, 0, 1, 4, 3, 1],
    [4, 0, 4, 1, 0, 0, 4, 4, 4, 1, 0, 1, 0, 3, 0],
    [4, 2, 4, 1, 0, 1, 3, 3, 4, 4, 0, 0, 0, 3, 1],
    [4, 4, 4, 1, 0, 2, 0, 0, 3, 4, 4, 2, 0, 0, 0],
    [0, 1, 0, 0, 0, 1, 3, 0, 3, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 2, 4, 4, 3, 0, 0, 2, 0, 1, 4, 4, 4],
    [1, 3, 0, 0, 0, 4, 4, 3, 3, 1, 0, 1, 4, 2, 4],
    [0, 3, 0, 1, 0, 1, 4, 4, 4, 0, 0, 0, 1, 4, 0],
    [1, 3, 4, 1, 0, 1, 1, 1, 1, 3, 1, 1, 4, 0, 3],
    [1, 2, 4, 1, 0, 1, 1, 1, 3, 3, 0, 2, 2, 0, 3],
    [1, 2, 4, 1, 1, 3, 0, 0, 3, 0, 0, 0, 0, 0, 3],
    [5, 0, 0, 0, 1, 1, 1, 3, 0, 1, 0, 3, 3, 3, 3]
]

# 游戏状态定义
STATE_INITIAL = "initial"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

# 当前游戏状态
game_state = STATE_INITIAL

def show_initial_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text1 = font.render("Press 1 for Level 1", True, WHITE)
    text2 = font.render("Press 2 for Level 2", True, WHITE)
    text3 = font.render("Press 3 for Level 3", True, WHITE)
    screen.blit(text1, (50, 50))
    screen.blit(text2, (50, 100))
    screen.blit(text3, (50, 150))
    pygame.display.flip()
def handle_initial_screen_events():
    global game_state, current_level, enemies, map_grid
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_level = 1
                enemies, map_grid = setup_level(current_level)
                game_state = STATE_PLAYING
            elif event.key == pygame.K_2:
                current_level = 2
                enemies, map_grid = setup_level(current_level)
                game_state = STATE_PLAYING
            elif event.key == pygame.K_3:
                current_level = 3
                enemies, map_grid = setup_level(current_level)
                game_state = STATE_PLAYING

level_3_start_time = 0  # 初始化为0

def setup_level(level_number):
    global level_3_start_time
    if level_number == 1:
        return [enemy_type_3.copy()], map_grid_esther  # 关卡1: 一个不能放置炸弹且不无敌的敌人
    elif level_number == 2:
        return [enemy_type_1.copy()], map_grid_first  # 关卡2: 一个能放置炸弹的敌人
    elif level_number == 3:
        enemies = []
        # 在四个角落生成无敌且可以放置炸弹的敌人
        corner_positions = [(0, 0), (0, num_cells - 1), (num_cells - 1, 0), (num_cells - 1, num_cells - 1)]
        for pos in corner_positions:
            new_enemy = enemy_type_2.copy()
            new_enemy['pos'] = list(pos)
            enemies.append(new_enemy)
        level_3_start_time = pygame.time.get_ticks()  # 初始化关卡3的计时器
        return enemies, map_grid_final  # 关卡3: 使用最终地图和4个无敌敌人


# 根据关卡选择敌人
#enemies = setup_level(1)  # 例如，选择第1关的敌人

#map_grid = map_grid_first

# 关卡状态变量
current_level = 1
max_levels = 3
enemies, map_grid = setup_level(current_level)
max_enemies_in_level_2 = 3  # 第二关最多生成3个敌人
enemies_spawned_in_level_2 = 1  # 初始生成了1个敌人

def next_level():
    global current_level, enemies, map_grid, max_enemies_in_level_2, enemies_spawned_in_level_2, game_state
    if current_level < max_levels:
        current_level += 1
        enemies, map_grid = setup_level(current_level)
        if current_level == 2:
            enemies_spawned_in_level_2 = 1 # 重置第二关的敌人生成计数
    else:
        show_game_over("Victory! All levels completed!")  # 显示胜利消息
        game_state = STATE_GAME_OVER
        handle_game_over_screen_events() # 返回初始目录

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
    elif map_grid[x][y] == 6:
        pygame.draw.rect(screen, SAPPHIRE, rect)  # 绘制蓝宝石砖块
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

    # 绘制敌人
    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy['pos'][0] * cell_size, enemy['pos'][1] * cell_size, cell_size, cell_size)
        pygame.draw.ellipse(screen, enemy['color'], enemy_rect)  # 根据敌人类型的颜色绘制

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

    # 显示敌人生命值（针对每个敌人）
    for i, enemy in enumerate(enemies):
        if enemy['lives'] is None:
            lives_text = font.render(f"Enemy {i + 1}: Invincible", True, BLACK)
        else:
            lives_text = font.render(f"Enemy {i + 1} Lives: {enemy['lives']}", True, BLACK)
        screen.blit(lives_text, (10, 50 + i * 40))

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
    global player_lives, enemy_lives, enemies, enemies_spawned_in_level_2
    if bomb not in bombs:
        return

    x, y = bomb['pos']
    bomb_range = bomb['range'] # 使用炸弹的范围属性
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四个主要方向
    affected_tiles = []
    immediate_explosions = []

    for dx, dy in directions:
        for step in range(1, bomb_range + 1):  # 使用炸弹的范围确定影响的格子
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
                game_state = STATE_GAME_OVER


    # 检查敌人是否在爆炸范围内
    for enemy in enemies[:]:
        if enemy['pos'] is not None and tuple(enemy['pos']) in affected_tiles:
            if enemy['lives'] is not None and enemy['lives'] < 10:  # 生命值为10时无敌
                enemy['lives'] -= 1
                if enemy['lives'] <= 0:
                    print(f"敌人被击败！位置: {enemy['pos']}")
                    map_grid[enemy['pos'][0]][enemy['pos'][1]] = 0
                    enemies.remove(enemy)  # 移除被击败的敌人

                    if current_level == 2:
                        if enemies_spawned_in_level_2 < max_enemies_in_level_2:
                            new_enemy = enemy_type_1.copy()
                            new_enemy['pos'] = random_empty_position()
                            enemies.append(new_enemy)
                            enemies_spawned_in_level_2 += 1
                            print(f"新敌人生成！位置: {new_enemy['pos']}")
                        elif len(enemies) == 0:  # 如果已经生成了3个敌人，且全部被击败
                            next_level() # 直接进入下一关
                    elif len(enemies) == 0 and current_level == 1:
                        next_level()  # 关卡1结束，进入下一关


    # 立即引爆触及的其他炸弹
    for bomb_to_explode in immediate_explosions:
        explode_bomb(bomb_to_explode)

# 找到地图中的空位置
def random_empty_position():
    empty_positions = [(x, y) for x in range(num_cells) for y in range(num_cells) if map_grid[x][y] == 0]
    return random.choice(empty_positions)

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

    player_bomb_range = 3  # 玩家的炸弹范围，可根据需要调整

    if map_grid[player_pos[0]][player_pos[1]] == 0 and not any(bomb['pos'] == player_pos for bomb in bombs):
        bombs.append({'pos': player_pos.copy(), 'time': pygame.time.get_ticks(), 'range': player_bomb_range})
        last_bomb_place_time = current_time

def enemy_place_bomb(enemy):
    current_time = pygame.time.get_ticks()

    # 根据关卡不同调整敌人的炸弹范围
    if current_level == 3:
        enemy_bomb_range = 15  # 关卡3的敌人炸弹范围为(1, 15)
    else:
        enemy_bomb_range = 2  # 其他关卡的敌人炸弹范围为2

    if current_time - enemy['last_bomb_place_time'] >= enemy_bomb_place_delay:
        bombs.append({'pos': enemy['pos'].copy(), 'time': pygame.time.get_ticks(), 'range': enemy_bomb_range})
        enemy['last_bomb_place_time'] = current_time


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
    pass

# 敌人移动逻辑
enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))
path_update_delay = 3000
last_path_update_time = pygame.time.get_ticks()

def move_enemy():
    global enemy_pos, enemy_path, last_path_update_time, player_lives
    current_time = pygame.time.get_ticks()

    if enemy_pos is None:
        return

    for enemy in enemies:
        if current_time - enemy['last_move_time'] > enemy_move_delay:
            enemy_path = a_star_search(map_grid, tuple(enemy['pos']), tuple(player_pos))

            if enemy_path:
                next_pos = enemy_path.pop(0)

                map_grid[enemy['pos'][0]][enemy['pos'][1]] = 0
                enemy['pos'] = list(next_pos)
                map_grid[enemy['pos'][0]][enemy['pos'][1]] = 5
                enemy['last_move_time'] = current_time

                if enemy['pos'] == player_pos:
                    if player_lives < 10:
                        print("无敌敌人碰到玩家，游戏结束！")
                        pygame.quit()
                        sys.exit()
                    else:
                        pass

                if enemy['last_bomb_place_time'] is not None and current_time - enemy['last_bomb_place_time'] >= enemy_bomb_place_delay:
                    enemy_place_bomb(enemy)

            else:
                random_move_enemy(enemy)
                if enemy['last_bomb_place_time'] is not None and current_time - enemy['last_bomb_place_time'] >= enemy_bomb_place_delay:
                    enemy_place_bomb(enemy)

def random_move_enemy(enemy):
    current_time = pygame.time.get_ticks()

    if current_time - enemy['last_move_time'] < enemy_move_delay:
        return

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    random.shuffle(directions)

    moved = False
    for dx, dy in directions:
        new_x, new_y = enemy['pos'][0] + dx, enemy['pos'][1] + dy
        if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
            map_grid[enemy['pos'][0]][enemy['pos'][1]] = 0
            enemy['pos'] = [new_x, new_y]
            map_grid[enemy['pos'][0]][enemy['pos'][1]] = 5
            enemy['last_move_time'] = current_time
            moved = True
            break

    if not moved:
        enemy['last_move_time'] = current_time  # 即使不能移动，也更新 last_move_time 防止卡住

last_player_pos = player_pos[:]

def update_game_state():
    global last_player_pos, enemy_path
    if player_pos != last_player_pos:
        enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))
        last_player_pos = player_pos[:]

def show_game_over(message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(cell_size * num_cells // 2, cell_size * num_cells // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # 显示3秒

def handle_game_over_screen_events():
    global game_state, enemies, player_pos, player_lives, current_level
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            current_level = 1
            player_pos = [5, 12]
            player_lives = 9
            enemies, map_grid = setup_level(current_level)
            game_state = STATE_INITIAL
            show_initial_screen()

async def main():
    global game_state
    # 原来的主循环代码
    clock = pygame.time.Clock()
    running = True
    while running:
        if game_state == STATE_INITIAL:
            show_initial_screen()
            handle_initial_screen_events()
        elif game_state == STATE_PLAYING:
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

            update_game_state()

            # 关卡3胜利条件：20秒内不被击杀
            if current_level == 3:
                elapsed_time = pygame.time.get_ticks() - level_3_start_time
                if elapsed_time >= 20000:  # 20秒
                    show_game_over("Victory! Survived 20 seconds!")  # 显示胜利消息
                    game_state = STATE_GAME_OVER
                    handle_game_over_screen_events()

            await asyncio.sleep(0)  # 需要添加这行以支持异步

        elif game_state == STATE_GAME_OVER:
            show_game_over("Victory! Press any key to return to the main menu")
            handle_game_over_screen_events()

    pygame.quit()
    sys.exit()

# 运行异步主循环
asyncio.run(main())