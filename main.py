import pygame
import random

# 初始化 Pygame
pygame.init()

# 定义常量
WIDTH,HEIGHT = 800,800
TILE_SIZE = 110
BLOCK_SIZE = TILE_SIZE
TOTAL_BLOCKS = 9
BLOCK_SPACING = 30
MAX_SLOTS = 6
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PINK = (240, 145, 160)
BUTTON_COLOR = (246, 190, 200)
TEXT_COLOR = (0, 0, 0)


# 创建窗口
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("yummy")

# 加载图案图片
patterns = [
    pygame.transform.scale(
        pygame.image.load(f"photo/food{i}.jpg"), (TILE_SIZE, TILE_SIZE)
    )
    for i in range(1, 7)
]

# 加载和缩放背景图像的函数
def load_and_scale_image(file_path, size):
    try:
        image = pygame.image.load(file_path)
        return pygame.transform.scale(image, size)
    except pygame.error as e:
        print(f"Failed to load image {file_path}: {e}")
        return None

# 加载背景图像:
menu_background = load_and_scale_image("photo/背景1.jpg", (WIDTH, HEIGHT))
gameBoard = load_and_scale_image("photo/背景2.jpg", (WIDTH, HEIGHT))

# 游戏状态初始化，add_new_tile 函数
def add_new_tile(block_index):
    current_tile, current_layers = blocks[block_index]
    if current_layers > 0:
        # 随机选择一个位置来移除图案
        random_index = random.randint(0, current_layers - 1)
        new_tile = current_tile[:random_index] + current_tile[random_index + 1:]
        blocks[block_index] = (new_tile, current_layers - 1)

# 创建游戏板
def generate_blocks(patterns):
    blocks = []
    all_patterns = []
    for i in range(9):
        pattern = random.choice(patterns)
        all_patterns.extend([pattern] * 3)
    random.shuffle(all_patterns)
    for i in range(0, len(all_patterns), 3):
        block_patterns = all_patterns[i:i + 3]
        block = (block_patterns, 3)
        blocks.append(block)
    return blocks

blocks = generate_blocks(patterns)
slots = []
game_active = False
time_left = 60 * 1000  # 默认第一关60s
start_time = None
game_result = None
difficulty = None  # 记录当前难度

# 按钮函数
def draw_rounded_rect(surface, color, rect, radius):
    """ 绘制圆角矩形 """
    x, y, width, height = rect
    radius = min(radius, height // 2, width // 2)
    # 绘制矩形
    pygame.draw.rect(surface, color, (x + radius, y, width - 2 * radius, height))
    pygame.draw.rect(surface, color, (x, y + radius, width, height - 2 * radius))
    # 绘制圆角
    pygame.draw.circle(surface, color, (x + radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + radius), radius)
    pygame.draw.circle(surface, color, (x + radius, y + height - radius), radius)
    pygame.draw.circle(surface, color, (x + width - radius, y + height - radius), radius)

def draw_button(text, x, y, width, height, active):
    font = pygame.font.SysFont("Microsoft YaHei", 40)
    color = BUTTON_COLOR
    radius = 10  # 圆角半径
    draw_rounded_rect(screen, color, (x, y, width, height), radius)
    text_surf = font.render(text, True, TEXT_COLOR)
    text_rect = text_surf.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surf, text_rect)

#绘制菜单
def draw_menu():
    screen.blit(menu_background, (0, 0))
    start_button = pygame.Rect(360, 330, 200, 60)
    quit_button = pygame.Rect(360, 430, 200, 60)
    mouse_pos = pygame.mouse.get_pos()
    draw_button("开始游戏", start_button.x, start_button.y, start_button.width, start_button.height, start_button.collidepoint(mouse_pos))
    draw_button("退出游戏", quit_button.x, quit_button.y, quit_button.width, quit_button.height, quit_button.collidepoint(mouse_pos))
    return start_button, quit_button

# 绘制关卡选择界面
def draw_difficulty_selection():
    screen.blit(menu_background, (0, 0))
    easy_button = pygame.Rect(360, 300, 200, 60)
    medium_button = pygame.Rect(360, 380, 200, 60)
    hard_button = pygame.Rect(360, 460, 200, 60)
    mouse_pos = pygame.mouse.get_pos()

    draw_button("第一关", easy_button.x, easy_button.y, easy_button.width, easy_button.height,
                easy_button.collidepoint(mouse_pos))
    draw_button("第二关", medium_button.x, medium_button.y, medium_button.width, medium_button.height,
                medium_button.collidepoint(mouse_pos))
    draw_button("第三关", hard_button.x, hard_button.y, hard_button.width, hard_button.height,
                hard_button.collidepoint(mouse_pos))

    return easy_button, medium_button, hard_button

# 游戏界面
def draw_board():
    # 关卡标题
    font = pygame.font.SysFont("Microsoft YaHei", 40)
    if difficulty == "easy":
        title_text = font.render("第一关", True, BLACK)
    elif difficulty == "medium":
        title_text = font.render("第二关", True, BLACK)
    elif difficulty == "hard":
        title_text = font.render("第三关", True, BLACK)
    title_rect = title_text.get_rect(center=(WIDTH // 2, 50))
    screen.blit(title_text, title_rect)
    if 'gameBoard' in globals():
        screen.blit(gameBoard, (0, 0))
        block_width = BLOCK_SIZE + BLOCK_SPACING
        num_cols = 3  # 更新列数为 3
        num_rows = 3  # 更新行数为 3
        start_x = (WIDTH - (block_width * num_cols)) // 2
        start_y = (HEIGHT - (block_width * num_rows)) // 2
        for i, (tiles, layers) in enumerate(blocks):
            row = i // num_cols
            col = i % num_cols
            base_x = start_x + col * block_width
            base_y = start_y + row * block_width
            # 绘制最顶层的块
            if layers > 0:
                screen.blit(tiles[-1], (base_x, base_y))

# 倒计时
def draw_timer(time_left):
    font = pygame.font.SysFont("Microsoft YaHei", 40)
    minutes = time_left // 60000
    seconds = (time_left % 60000) // 1000
    time_text = f"{minutes:02}:{seconds:02}"
    timer_surf = font.render(time_text, True, BLACK)
    screen.blit(timer_surf, (WIDTH - 450, 100))

# 绘制卡槽
def draw_slots():
    slot_x = 50
    slot_y = HEIGHT - TILE_SIZE - 50
    slot_width = TILE_SIZE + 10
    slot_height = TILE_SIZE
    for i in range(MAX_SLOTS):
        pygame.draw.rect(screen, PINK, (slot_x + i * slot_width, slot_y, slot_width, slot_height))
    for i, tile in enumerate(slots):
        if i < MAX_SLOTS:
            screen.blit(tile, (slot_x + i * slot_width + 5, slot_y + 5))

# 检查并消除卡槽中三个一样的图案
def check_and_remove_matching():
    global slots
    new_slots = []
    i = 0
    while i < len(slots):
        if i <= len(slots) - 3 and slots[i] == slots[i + 1] == slots[i + 2]:
            i += 3  # 跳过匹配的三个图案
        else:
            new_slots.append(slots[i])
            i += 1
    slots = new_slots


# 绘制结果界面
def draw_result_screen(message):
    screen.blit(gameBoard, (0, 0))
    font = pygame.font.SysFont("Microsoft YaHei", 60)
    result_text = font.render(message, True, BLACK)
    text_rect = result_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(result_text, text_rect)

    restart_button = pygame.Rect(300, 500, 200, 50)
    quit_button = pygame.Rect(300, 600, 200, 50)
    mouse_pos = pygame.mouse.get_pos()

    draw_button("重新开始", restart_button.x, restart_button.y, restart_button.width, restart_button.height,
                restart_button.collidepoint(mouse_pos))
    draw_button("退出游戏", quit_button.x, quit_button.y, quit_button.width, quit_button.height,
                quit_button.collidepoint(mouse_pos))

    return restart_button, quit_button


# 主游戏循环
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(FPS)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not game_active:
                if difficulty is None:
                    start_button, quit_button = draw_menu()
                    if start_button.collidepoint(mouse_pos):
                        difficulty = "select"
                    elif quit_button.collidepoint(mouse_pos):
                        running = False
                elif difficulty == "select":
                    easy_button, medium_button, hard_button = draw_difficulty_selection()
                    if easy_button.collidepoint(mouse_pos):
                        difficulty = "easy"
                        time_left = 60 * 1000
                    elif medium_button.collidepoint(mouse_pos):
                        difficulty = "medium"
                        time_left = 50 * 1000
                    elif hard_button.collidepoint(mouse_pos):
                        difficulty = "hard"
                        time_left = 40 * 1000

                    if difficulty:
                        game_active = True
                        start_time = pygame.time.get_ticks()
                        blocks = generate_blocks(patterns)
                        slots.clear()

            else:
                if game_result is None:
                    pos_x, pos_y = event.pos
                    block_width = BLOCK_SIZE + BLOCK_SPACING
                    num_columns = 3
                    block_idx = ((pos_x - (WIDTH - (block_width * num_columns)) // 2) // block_width) + \
                                  ((pos_y - (HEIGHT - (block_width * num_columns)) // 2) // block_width) * num_columns

                    if 0 <= block_idx < TOTAL_BLOCKS and len(slots) < MAX_SLOTS:
                        current_tiles, _ = blocks[block_idx]
                        if current_tiles:
                            slots.append(current_tiles[-1])
                            add_new_tile(block_idx)
                            check_and_remove_matching()

                            if len(slots) >= MAX_SLOTS:
                                game_result = "LOSE"
                                game_active = False
                            elif all(layer_count == 0 for _, layer_count in blocks):
                                game_result = "WIN"
                                game_active = False

    if game_active:
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - start_time
        time_left = max(0, time_left - elapsed_time)
        start_time = current_time

        if time_left <= 0:
            game_result = "LOSE"
            game_active = False

        screen.fill(WHITE)
        draw_board()
        draw_slots()
        draw_timer(time_left)

    else:
        if game_result in ["WIN", "LOSE"]:
            message = "恭喜通关" if game_result == "WIN" else "遗憾退场"
            restart_button, quit_button = draw_result_screen(message)

            if pygame.mouse.get_pressed()[0]:
                if restart_button.collidepoint(mouse_pos):
                    difficulty = "select"
                    game_result = None
                elif quit_button.collidepoint(mouse_pos):
                    running = False
        else:
            if difficulty == "select":
                draw_difficulty_selection()
            else:
                draw_menu()

    pygame.display.update()

pygame.quit()
