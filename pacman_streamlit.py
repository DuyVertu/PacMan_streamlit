import streamlit as st
from PIL import Image, ImageDraw
import random

# Kích thước màn hình
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
GRID_SIZE = 20

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)  # Màu vàng cho Pac-Man
GREEN = (0, 255, 0)  # Màu xanh cho Ghost

# Grid mẫu cho Pac-Man
grid = [
    ["#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", "#"],
    ["#", " ", "#", "#", " ", " ", "#"],
    ["#", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#"]
]

# Hàm vẽ grid
def draw_grid(pacman_x, pacman_y, ghost_x, ghost_y):
    img = Image.new('RGB', (len(grid[0]) * GRID_SIZE, len(grid) * GRID_SIZE), WHITE)
    draw = ImageDraw.Draw(img)

    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col] == "#":
                draw.rectangle([col * GRID_SIZE, row * GRID_SIZE, (col + 1) * GRID_SIZE, (row + 1) * GRID_SIZE], fill=BLUE)
            else:
                draw.rectangle([col * GRID_SIZE, row * GRID_SIZE, (col + 1) * GRID_SIZE, (row + 1) * GRID_SIZE], outline=BLACK)

    draw.ellipse([pacman_x * GRID_SIZE, pacman_y * GRID_SIZE, (pacman_x + 1) * GRID_SIZE, (pacman_y + 1) * GRID_SIZE], fill=YELLOW)
    draw.ellipse([ghost_x * GRID_SIZE, ghost_y * GRID_SIZE, (ghost_x + 1) * GRID_SIZE, (ghost_y + 1) * GRID_SIZE], fill=GREEN)

    return img

# Hàm di chuyển Pac-Man
def move_pacman(key, pacman_x, pacman_y):
    if key == "UP" and pacman_y > 0 and grid[pacman_y - 1][pacman_x] != "#":
        pacman_y -= 1
    elif key == "DOWN" and pacman_y < len(grid) - 1 and grid[pacman_y + 1][pacman_x] != "#":
        pacman_y += 1
    elif key == "LEFT" and pacman_x > 0 and grid[pacman_y][pacman_x - 1] != "#":
        pacman_x -= 1
    elif key == "RIGHT" and pacman_x < len(grid[0]) - 1 and grid[pacman_y][pacman_x + 1] != "#":
        pacman_x += 1
    return pacman_x, pacman_y

# Hàm di chuyển Ghost ngẫu nhiên
def move_ghost(ghost_x, ghost_y):
    direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
    if direction == "UP" and ghost_y > 0 and grid[ghost_y - 1][ghost_x] != "#":
        ghost_y -= 1
    elif direction == "DOWN" and ghost_y < len(grid) - 1 and grid[ghost_y + 1][ghost_x] != "#":
        ghost_y += 1
    elif direction == "LEFT" and ghost_x > 0 and grid[ghost_y][ghost_x - 1] != "#":
        ghost_x -= 1
    elif direction == "RIGHT" and ghost_x < len(grid[0]) - 1 and grid[ghost_y][ghost_x + 1] != "#":
        ghost_x += 1
    return ghost_x, ghost_y

# Hàm kiểm tra xem Pac-Man có chạm phải Ghost không
def check_game_over(pacman_x, pacman_y, ghost_x, ghost_y):
    return pacman_x == ghost_x and pacman_y == ghost_y

# Hàm hiển thị Game Over
def display_game_over():
    return "GAME OVER! Press ENTER to restart."

# Hàm chạy trò chơi
def game():
    # Khởi tạo session state nếu chưa có
    if 'pacman_x' not in st.session_state:
        st.session_state.pacman_x = 1
        st.session_state.pacman_y = 1
        st.session_state.ghost_x = 5
        st.session_state.ghost_y = 1

    pacman_x = st.session_state.pacman_x
    pacman_y = st.session_state.pacman_y
    ghost_x = st.session_state.ghost_x
    ghost_y = st.session_state.ghost_y

    # Điều khiển Pac-Man: Các nút điều khiển
    st.title("Pac-Man Game")

    # Sử dụng các nút bấm để di chuyển Pac-Man
    col1, col2, col3 = st.columns(3)

    # Mỗi cột là một nút điều khiển di chuyển
    with col1:
        if st.button("Move Up"):
            pacman_x, pacman_y = move_pacman("UP", pacman_x, pacman_y)
    with col2:
        if st.button("Move Left"):
            pacman_x, pacman_y = move_pacman("LEFT", pacman_x, pacman_y)
    with col3:
        if st.button("Move Right"):
            pacman_x, pacman_y = move_pacman("RIGHT", pacman_x, pacman_y)

    if st.button("Move Down"):
        pacman_x, pacman_y = move_pacman("DOWN", pacman_x, pacman_y)

    # Di chuyển Ghost
    ghost_x, ghost_y = move_ghost(ghost_x, ghost_y)

    # Kiểm tra Game Over
    if check_game_over(pacman_x, pacman_y, ghost_x, ghost_y):
        st.text(display_game_over())
        if st.button('Press ENTER to restart'):
            # Reset trò chơi
            st.session_state.pacman_x = 1
            st.session_state.pacman_y = 1
            st.session_state.ghost_x = 5
            st.session_state.ghost_y = 1
    else:
        # Cập nhật trạng thái của Pac-Man và Ghost
        st.session_state.pacman_x = pacman_x
        st.session_state.pacman_y = pacman_y
        st.session_state.ghost_x = ghost_x
        st.session_state.ghost_y = ghost_y

    # Vẽ lại grid và các đối tượng
    img = draw_grid(pacman_x, pacman_y, ghost_x, ghost_y)
    st.image(img)

# Chạy trò chơi
if __name__ == "__main__":
    game()
