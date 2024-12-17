import tkinter as tk
import random


# Create the main window
root = tk.Tk()
root.title("シューティングゲーム")
canvas = tk.Canvas(root, width=500, height=400, bg="black")
canvas.pack()

# Game state variables
player_width = 50
player_height = 30
player = None  # Player created when the game starts
bullets = []
enemies = []
score = 0
lives = 1  # ライフを1に固定
difficulty_level = "Medium"  # Default difficulty


# Update the score display
def update_score_display():
    canvas.itemconfig(score_text, text=f"Score: {score}")
    if score >= 1000:  # スコアが1000に達した場合、ゲームクリア
        game_clear()


# Update the life display
def update_lives_display():
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")


# Handle player movement
def move_left(event):
    canvas.move(player, -20, 0)
    if canvas.coords(player)[0] < 0:  # Prevent going out of bounds
        canvas.move(player, 20, 0)


def move_right(event):
    canvas.move(player, 20, 0)
    if canvas.coords(player)[2] > 500:  # Prevent going out of bounds
        canvas.move(player, -20, 0)


# Fire a bullet
def shoot(event):
    bullet = canvas.create_oval(
        canvas.coords(player)[0] + 20, canvas.coords(player)[1] - 10,
        canvas.coords(player)[2] - 20, canvas.coords(player)[1] - 2, fill="yellow"
    )
    bullets.append(bullet)


# Create enemies
def create_enemy():
    x_pos = random.randint(0, 450)
    # Adjusted enemy type probabilities
    enemy_type = random.choices(["red", "green", "purple"], weights=[60, 30, 10], k=1)[0]
    if enemy_type == "purple":
        enemy_speed = random.randint(2, 4)
        # 紫色の三角形を描画
        points = [x_pos, 0, x_pos + 15, 30, x_pos - 15, 30]
        enemy = canvas.create_polygon(points, fill="purple")
    else:
        # 赤または緑の四角形
        enemy_speed = random.randint(1, 3)
        enemy = canvas.create_rectangle(x_pos, 0, x_pos + 30, 30, fill=enemy_type)

    enemies.append({"id": enemy, "type": enemy_type, "speed": enemy_speed})


# Move enemies and handle collisions
def move_enemies():
    global lives, score
    for enemy in enemies[:]:  # Ensure safe iteration
        canvas.move(enemy["id"], 0, enemy["speed"])  # Move the enemies
        if canvas.coords(enemy["id"])[3] > 400:  # If it reaches the bottom of the canvas
            canvas.delete(enemy["id"])
            enemies.remove(enemy)
            lives -= 1
            update_lives_display()
            if lives <= 0:
                game_over()
        for bullet in bullets[:]:
            if (
                canvas.coords(bullet)[2] > canvas.coords(enemy["id"])[0]
                and canvas.coords(bullet)[0] < canvas.coords(enemy["id"])[2]
                and canvas.coords(bullet)[1] < canvas.coords(enemy["id"])[3]
            ):
                canvas.delete(bullet)
                bullets.remove(bullet)
                canvas.delete(enemy["id"])
                enemies.remove(enemy)
                
                # 当たった敵の種類でスコア加算
                if enemy["type"] == "purple":  # 紫色の敵は50点
                    score += 50
                elif enemy["type"] == "green":  # 緑色の敵は30点
                    score += 30
                else:  # 赤色の敵は10点
                    score += 10
                
                update_score_display()
                break
    root.after(50, move_enemies)


# Move bullets
def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -5)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    root.after(50, move_bullets)


# Create a wave of enemies
def enemy_wave():
    if difficulty_level == "Easy":
        delay = 1500
    elif difficulty_level == "Medium":
        delay = 1000
    else:
        delay = 700
    create_enemy()  # Create a new enemy
    root.after(delay, enemy_wave)  # Set the delay for next enemy


# Handle Game Over
def game_over():
    canvas.create_text(250, 200, text="GAME OVER", fill="white", font=("Helvetica", 20))
    root.after(2000, root.destroy)


# Handle Game Clear
def game_clear():
    canvas.create_text(250, 200, text="GAME CLEAR!", fill="white", font=("Helvetica", 20))
    root.after(2000, root.destroy)


# Start the game logic
def start_game():
    global player, score_text, lives_text
    canvas.delete("all")  # Clear menu
    player = canvas.create_rectangle(225, 350, 275, 380, fill="blue")  # Create player
    root.bind("<Left>", move_left)  # Left key event
    root.bind("<Right>", move_right)  # Right key event
    root.bind("<space>", shoot)  # Space key event
    score_text = canvas.create_text(50, 10, text=f"Score: {score}", fill="white", font=("Helvetica", 12))
    lives_text = canvas.create_text(400, 10, text=f"Lives: {lives}", fill="white", font=("Helvetica", 12))
    move_enemies()
    move_bullets()
    enemy_wave()


# Menu screen for difficulty selection
def create_menu():
    def set_difficulty_and_start(level):
        global difficulty_level
        difficulty_level = level  # Set difficulty
        start_game()

    # Clear menu area
    canvas.delete("all")
    canvas.create_text(250, 100, text="難易度選択", fill="white", font=("Helvetica", 16))

    # Difficulty buttons
    easy_button = tk.Button(root, text="初級 (Easy)", command=lambda: set_difficulty_and_start("Easy"))
    medium_button = tk.Button(root, text="中級 (Medium)", command=lambda: set_difficulty_and_start("Medium"))
    hard_button = tk.Button(root, text="上級 (Hard)", command=lambda: set_difficulty_and_start("Hard"))

    # Pack buttons
    easy_button.pack()
    medium_button.pack()
    hard_button.pack()


# Create and show the menu
create_menu()

root.mainloop()
