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
player = None
bullets = []
enemies = []
score = 0
lives = 3  # 初期ライフ設定
difficulty_level = "Medium"


# Update the score display
def update_score_display():
    canvas.itemconfig(score_text, text=f"Score: {score}")


# Update the life display
def update_lives_display():
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")


# Handle player movement
def move_left(event):
    canvas.move(player, -20, 0)
    if canvas.coords(player)[0] < 0:
        canvas.move(player, 20, 0)


def move_right(event):
    canvas.move(player, 20, 0)
    if canvas.coords(player)[2] > 500:
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
    enemy_type = random.choices(["red", "green", "purple"], weights=[60, 30, 10], k=1)[0]
    
    # Adjusted difficulty: slower speeds for enemies
    if enemy_type == "purple":
        enemy_speed = random.randint(1, 3)  # Slower speed
        points = [x_pos, 0, x_pos + 15, 30, x_pos - 15, 30]
        enemy = canvas.create_polygon(points, fill="purple")
    else:
        enemy_speed = random.randint(1, 2)  # Slower speed
        enemy = canvas.create_rectangle(x_pos, 0, x_pos + 30, 30, fill=enemy_type)

    enemies.append({"id": enemy, "type": enemy_type, "speed": enemy_speed})


# Handle collisions and bullet movement
def move_bullets():
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -5)  # 弾丸を上に動かす
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)
    root.after(50, move_bullets)  # 弾丸ループ


# Move enemies and handle collision
def move_enemies():
    global lives, score
    for enemy in enemies[:]:
        canvas.move(enemy["id"], 0, enemy["speed"])
        if canvas.coords(enemy["id"])[3] > 400:
            # 敵が画面の下まで到達した場合
            canvas.delete(enemy["id"])
            enemies.remove(enemy)
            lives -= 1
            update_lives_display()
            
            # ゲームオーバーのチェック
            if lives <= 0:
                game_over()
                return  # これ以上処理を行わない

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
                score += 10
                update_score_display()
                break

    root.after(50, move_enemies)  # 敵のループを継続


# Enemy spawning loop with adjusted difficulty
def enemy_wave():
    if lives > 0:  # ゲームが進行中のみ敵を生成
        create_enemy()
        root.after(800, enemy_wave)  # 敵出現間隔


# Game Over
def game_over():
    canvas.create_text(250, 200, text="GAME OVER", fill="white", font=("Helvetica", 24))
    print("GAME OVER - ライフが0になりました")  # ログ出力
    root.after(2000, root.destroy)  # 2秒後にアプリを終了


# Main game start logic
def start_game():
    global player, score_text, lives_text, lives
    canvas.delete("all")
    
    # Reset state
    lives = 3  # 明示的にライフを3に設定
    bullets.clear()
    enemies.clear()
    
    # Draw initial game elements
    player = canvas.create_rectangle(225, 350, 275, 380, fill="blue")
    root.bind("<Left>", move_left)
    root.bind("<Right>", move_right)
    root.bind("<space>", shoot)
    
    # Set up the score and lives UI
    score_text = canvas.create_text(50, 10, text=f"Score: {score}", fill="white", font=("Helvetica", 12))
    lives_text = canvas.create_text(400, 10, text=f"Lives: {lives}", fill="white", font=("Helvetica", 12))
    
    # Update the lives display explicitly
    update_lives_display()
    
    # Start game logic
    move_bullets()
    move_enemies()
    enemy_wave()


start_game()
root.mainloop()
