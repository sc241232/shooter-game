シューティングゲーム終.py
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
lives = 1  # 初期ライフ設定
restart_button = None  # ボタンをグローバル変数として管理
start_button = None  # ゲーム開始ボタンのための変数

# ルール説明の画面
def show_rules():
    canvas.delete("all")  # 画面をクリア
    canvas.create_text(250, 50, text="シューティングゲーム", fill="white", font=("Helvetica", 24))
    canvas.create_text(250, 100, text="ゲームのルール:", fill="white", font=("Helvetica", 16))
    canvas.create_text(250, 130, text="1. 青い的を動かして敵を避け、弾を発射してください。", fill="white", font=("Helvetica", 14))
    canvas.create_text(250, 160, text="2. 赤、緑、紫の敵が出てきます。紫は得点が高い！", fill="white", font=("Helvetica", 14))
    canvas.create_text(250, 190, text="3. 画面下に到達した敵を避けつつ撃退しましょう。", fill="white", font=("Helvetica", 14))
    canvas.create_text(250, 220, text="4. 画面左・右キーで移動、スペースキーで弾を発射！", fill="white", font=("Helvetica", 14))
    canvas.create_text(250, 260, text="5. ゲームが終了したら、再スタートボタンを押してね！", fill="white", font=("Helvetica", 14))
    
    # ゲームスタートボタンの表示
    global start_button
    if start_button is not None:
        start_button.destroy()  # 以前のボタンを削除

    start_button = tk.Button(root, text="ゲームスタート", command=start_game)
    start_button.place(x=200, y=300)  # ボタンの位置を調整

# Update the score display
def update_score_display():
    canvas.itemconfig(score_text, text=f"Score: {score}")

# Update the life display
def update_lives_display():
    canvas.itemconfig(lives_text, text=f"Lives: {lives}")

# Handle player movement
def move_left(event):
    canvas.move(player, -20, 0)
    x1, _, x2, _ = canvas.coords(player)
    if x1 < 0:
        canvas.move(player, 20, 0)

def move_right(event):
    canvas.move(player, 20, 0)
    _, _, x2, _ = canvas.coords(player)
    if x2 > 500:
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
    enemy_speed = random.randint(1, 2)  # 速さは常に1〜2の範囲
    if enemy_type == "purple":
        points = [x_pos, 0, x_pos + 15, 30, x_pos - 15, 30]
        enemy = canvas.create_polygon(points, fill="purple")
    else:
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
        root.after(800 - (score // 100), enemy_wave)  # Increase frequency as score increases

# Game Over
def game_over():
    # Display GAME OVER text
    canvas.create_text(250, 150, text="GAME OVER", fill="white", font=("Helvetica", 24))

    # Display score
    canvas.create_text(250, 200, text=f"Your Score: {score}", fill="white", font=("Helvetica", 14))

    # Show the restart button after 2 seconds
    root.after(2000, show_restart_button)

# Show the restart button after 2 seconds
def show_restart_button():
    global restart_button
    if restart_button is not None:
        restart_button.destroy()  # 前回のボタンを削除

    restart_button = tk.Button(root, text="もう一度ゲームをする", command=restart_game)
    restart_button.place(x=200, y=250)  # ボタンの位置を調整

# Restart the game
def restart_game():
    global score, lives, restart_button
    score = 0
    lives = 1  # ライフを1にリセット
    canvas.delete("all")  # Clear the canvas before starting a new game
    if restart_button is not None:
        restart_button.destroy()  # Remove restart button
    start_game()  # Start the game again

# Main game start logic
def start_game():
    global player, score_text, lives_text, lives, restart_button, start_button
    # ゲームスタートボタンを非表示にする
    if start_button is not None:
        start_button.destroy()  # ボタンを削除

    canvas.delete("all")

    # Reset state
    lives = 1  # 明示的にライフを1に設定
    bullets.clear()
    enemies.clear()
    score = 0  # ゲーム開始時にスコアもリセット

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

# 最初にルール説明を表示
show_rules()

root.mainloop()