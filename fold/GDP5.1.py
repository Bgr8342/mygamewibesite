#备注：总共有0 1 2 3 4 5五种砖块
#0是空地，2是不可破坏的，5是敌人
#爆炸范围调节在def explode_bomb里面，爆炸时威力无法穿透
#当敌人大于等于五时是无敌的，被碰到就游戏结束,当玩家的生命值大于等于10时，玩家是无敌的
#按键支持长按，但有速度限制，可以更改
#受到伤害砖块会降级
#玩家的生命值为2，可以调节
#敌人会主动追踪玩家，追踪速度可以调节
#炸弹可以发生连锁反应
#炸弹无法重复释放

#还需改进：炸弹的释放有个数限制

#新的设想：游戏关卡设置，1 破坏所有方块进入第二关
#2 击杀所有敌人（被碰到就寄）进入第三关
#3 躲避敌人（无敌）的追杀并破坏掉所有的砖块进入下一关
#生存时间为88秒，敌人会逐渐增多，敌人可被击杀，但是敌人血量逐渐增多
#最后关卡：生存88秒，敌人（无敌）会主动破坏墙壁，
# 并且会释放炸弹，不能碰到敌人（3个），会被炸弹炸死

import pygame
import heapq
import sys
import random

pygame.init()

# 设置窗口大小
cell_size = 40  # 每个单元格的像素大小
num_cells = 15  # 网格的行数和列数

screen = pygame.display.set_mode((cell_size * num_cells, cell_size * num_cells))
pygame.display.set_caption("Pygame Bomberman Map")

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)  # 可破坏的墙壁
RED = (255, 0, 0)  # 玩家颜色
YELLOW = (255, 255, 0)  # 炸弹颜色
GOLD = (255, 215, 0)  # 金色光束的颜色
SLATE_GRAY = (112, 128, 144)  # 需要2次攻击的砖块
BROWN = (139, 69, 19)  # 需要3次攻击的砖块

# 时间控制
enemy_move_delay = 500  # 敌人每1000毫秒移动一次
last_move_time = pygame.time.get_ticks()

# 玩家 初始位置
player_pos = [1, 1]  # 第二行第二列的位置
player_lives = 10  # 玩家生命值初始为2

# 设置敌人的初始血量
enemy_lives = 10  # 如果为大于5，则表示无敌

player_move_delay = 200  # 玩家每次移动间隔（毫秒）
last_player_move_time = pygame.time.get_ticks()

bomb_place_delay = 200  # 炸弹放置间隔（毫秒）
last_bomb_place_time = pygame.time.get_ticks()

enemy_bomb_place_delay = 2000  # 敌人放置炸弹的间隔（毫秒）
last_enemy_bomb_place_time = pygame.time.get_ticks()

# 使用预定义的地图数组


map_grid = [
[4, 1, 0, 3, 0, 4, 1, 3, 4, 0, 3, 0, 1, 4, 4],
[1, 0, 4, 0, 1, 3, 0, 1, 3, 1, 0, 4, 0, 1, 1],
[3, 1, 0, 4, 1, 0, 3, 0, 3, 0, 1, 4, 0, 1, 3],
[4, 3, 1, 0, 4, 0, 4, 3, 4, 0, 4, 0, 1, 3, 4],
[0, 4, 3, 1, 0, 3, 1, 4, 1, 3, 0, 1, 3, 4, 0],
[3, 1, 0, 4, 1, 0, 4, 1, 4, 0, 1, 4, 0, 1, 3],
[4, 3, 1, 0, 4, 3, 1, 4, 1, 3, 0, 4, 1, 3, 4],
[1, 4, 0, 3, 4, 1, 0, 1, 0, 1, 4, 3, 0, 4, 1],
[4, 3, 1, 0, 4, 3, 1, 4, 1, 3, 0, 4, 1, 3, 4],
[3, 1, 0, 4, 1, 0, 4, 1, 4, 0, 1, 4, 0, 1, 3],
[0, 4, 3, 1, 0, 3, 1, 4, 1, 3, 0, 1, 3, 4, 0],
[4, 3, 1, 0, 4, 0, 4, 3, 4, 0, 4, 0, 1, 3, 4],
[3, 1, 0, 4, 1, 0, 3, 0, 3, 0, 1, 4, 0, 1, 3],
[1, 0, 4, 0, 1, 3, 0, 1, 3, 1, 0, 4, 5, 1, 1],
[4, 1, 0, 3, 0, 4, 1, 3, 4, 0, 3, 0, 1, 4, 4]
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
                if map_grid[neighbor[0]][neighbor[1]] != 0:  # 避开非空格
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

def draw_grid():
    for x in range(num_cells):
        for y in range(num_cells):
            rect = pygame.Rect(x*cell_size, y*cell_size, cell_size, cell_size)
            if map_grid[x][y] == 1:
                pygame.draw.rect(screen, GREY, rect)  # 绘制可破坏的砖块
            elif map_grid[x][y] == 2:
                pygame.draw.rect(screen, (0, 0, 255), rect)  # 绘制不可破坏的砖块（蓝色）
            elif map_grid[x][y] == 3:
                pygame.draw.rect(screen, SLATE_GRAY, rect)  # 绘制Slate_Gray砖块
            elif map_grid[x][y] == 4:
                pygame.draw.rect(screen, BROWN, rect)  # 绘制灰褐色砖块
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

    # 显示玩家生命值
    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {player_lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

def explode_bomb(bomb):
    global player_lives, enemy_lives, enemy_pos
    if bomb not in bombs:
        return  # 如果炸弹已经不在列表中，直接返回

    x, y = bomb['pos']
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 四个主要方向
    affected_tiles = [(x, y)]
    immediate_explosions = []

    for dx, dy in directions:
        for step in range(1, 5):  # 检查距离为1和2的格子
            nx, ny = x + dx * step, y + dy * step
            if 0 <= nx < num_cells and 0 <= ny < num_cells:

                if map_grid[nx][ny] == 4:  # 检查灰褐色砖块
                    map_grid[nx][ny] = 3  # 降级为Slate_Gray砖块
                    break  # 阻挡爆炸继续穿透

                elif map_grid[nx][ny] == 3:  # 检查Slate_Gray砖块
                    map_grid[nx][ny] = 1  # 降级为普通灰色砖块
                    break  # 阻挡爆炸继续穿透

                elif map_grid[nx][ny] == 2: # 遇到蓝色砖块，停止这个方向的破坏
                    break
                affected_tiles.append((nx, ny))
                if map_grid[nx][ny] == 1: # 灰色砖块被破坏
                    map_grid[nx][ny] = 0
                    break # 阻挡爆炸继续穿透
                else:
                    affected_tiles.append((nx, ny))  # 如果是空地，继续检查下一个格子

                # 检查是否触及其他炸弹
                for other_bomb in bombs:
                    if other_bomb['pos'] == [nx, ny] and other_bomb not in immediate_explosions:
                        immediate_explosions.append(other_bomb)
            else:
                break # 超出边界也停止检查

    bombs.remove(bomb)
    # 记录爆炸效果和持续时间
    explosions.append({'tiles': affected_tiles, 'end_time': pygame.time.get_ticks() + 500}) # 保持500毫秒

    # 检查玩家是否在爆炸范围内
    if tuple(player_pos) in affected_tiles:
        if player_lives < 10:  # 生命值为10时无敌，不减少生命值
            player_lives -= 1  # 生命值减一
            if player_lives <= 0:
                print("游戏结束！")
                pygame.quit()
                sys.exit()

    # 检查敌人是否在爆炸范围内
    if enemy_pos is not None and tuple(enemy_pos) in affected_tiles:
        if enemy_lives < 5:  # 5 表示无敌
            enemy_lives -= 1
            if enemy_lives <= 0:
                print("敌人被击败！")
                map_grid[enemy_pos[0]][enemy_pos[1]] = 0  # 移除敌人
                enemy_pos = None  # 敌人位置设为空

    # 立即引爆触及的炸弹
    for bomb_to_explode in immediate_explosions:
        explode_bomb(bomb_to_explode)

def move_player(dx, dy):
    global last_player_move_time, player_pos
    current_time = pygame.time.get_ticks()
    if current_time - last_player_move_time < player_move_delay:
        return  # 如果时间间隔不到设定的移动间隔，就不移动

    new_x = player_pos[0] + dx
    new_y = player_pos[1] + dy
    if 0 <= new_x < num_cells and 0 <= new_y < num_cells and map_grid[new_x][new_y] == 0:
        player_pos[0] = new_x
        player_pos[1] = new_y

    last_player_move_time = current_time  # 更新上次移动时间

def place_bomb():
    global last_bomb_place_time
    current_time = pygame.time.get_ticks()
    if current_time - last_bomb_place_time < bomb_place_delay:
        return  # 如果时间间隔不到设定的炸弹放置间隔，就不放置炸弹

    if map_grid[player_pos[0]][player_pos[1]] == 0 and not any(bomb['pos'] == player_pos for bomb in bombs):
        bombs.append({'pos': player_pos.copy(), 'time': pygame.time.get_ticks()})
        last_bomb_place_time = current_time  # 更新上次放置炸弹时间

def enemy_place_bomb():
    global last_enemy_bomb_place_time
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
        # 在敌人的当前位置放置炸弹
        bombs.append({'pos': enemy_pos.copy(), 'time': pygame.time.get_ticks()})
        last_enemy_bomb_place_time = current_time  # 更新上次放置炸弹的时间

# 查找地图上的敌人初始位置
def find_enemy_position(map_grid):
    for x in range(num_cells):
        for y in range(num_cells):
            if map_grid[x][y] == 5:
                return [x, y]
    return None  # 如果没有找到敌人

# 在主程序中初始化
enemy_pos = find_enemy_position(map_grid)
if enemy_pos is None:
    print("No enemy found on the map")
    sys.exit(1)  # 如果没有敌人就退出程序

# 敌人移动逻辑
enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))

path_update_delay = 3000  # 每3000毫秒更新一次路径
last_path_update_time = pygame.time.get_ticks()

def move_enemy():
    global enemy_pos, enemy_path, last_move_time, last_path_update_time, player_lives
    current_time = pygame.time.get_ticks()

    # 检查敌人是否存在
    if enemy_pos is None:
        return  # 如果敌人已经被击败，直接返回，不再执行敌人移动逻辑

    if current_time - last_move_time > enemy_move_delay:
        # 尝试重新计算路径
        enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))

        if enemy_path:
            next_pos = enemy_path.pop(0)  # 取出路径的下一个位置
            map_grid[enemy_pos[0]][enemy_pos[1]] = 0
            enemy_pos = list(next_pos)
            map_grid[enemy_pos[0]][enemy_pos[1]] = 5
            last_move_time = current_time

            # 检查敌人是否与玩家碰撞
            if enemy_pos == player_pos:
                if player_lives < 10:  # 如果玩家不是无敌状态
                    print("无敌敌人碰到玩家，游戏结束！")
                    pygame.quit()
                    sys.exit()
                else:
                    pass

            # 只有在路径可达时才放置炸弹
            if enemy_lives == 10 and current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
                enemy_place_bomb()

        else:  # 如果找不到通路，执行随机移动和放置炸弹
            random_move_enemy()
            if enemy_lives == 10 and current_time - last_enemy_bomb_place_time >= enemy_bomb_place_delay:
                enemy_place_bomb()

def random_move_enemy():
    global enemy_pos, last_move_time
    current_time = pygame.time.get_ticks()

    if current_time - last_move_time < enemy_move_delay:
        return

    # 尝试随机移动敌人到相邻的空格
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

last_player_pos = player_pos[:]  # 初始时复制玩家位置

def update_game_state():
    global last_player_pos, enemy_path
    if player_pos != last_player_pos:
        # 玩家位置发生变化，重新计算路径
        enemy_path = a_star_search(map_grid, tuple(enemy_pos), tuple(player_pos))
        last_player_pos = player_pos[:]  # 更新最后记录的玩家位置

clock = pygame.time.Clock()

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                place_bomb()

    # 获取按键状态
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        move_player(-1, 0)
    elif keys[pygame.K_RIGHT]:
        move_player(1, 0)
    elif keys[pygame.K_UP]:
        move_player(0, -1)
    elif keys[pygame.K_DOWN]:
        move_player(0, 1)

        # 长按空格键放置炸弹
    if keys[pygame.K_SPACE]:
        place_bomb()

    screen.fill(BLACK)  # 设置背景颜色
    move_enemy()  # Update enemy position based on player position
    draw_grid()
    pygame.display.flip()
    clock.tick(60)  # 控制游戏帧率

pygame.quit()
sys.exit()