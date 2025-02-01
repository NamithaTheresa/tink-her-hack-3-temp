import tkinter as tk
from tkinter import messagebox
import random

# Initialize the main window
root = tk.Tk()
root.title("Ultimate Game Hub")
root.geometry("800x600")
root.resizable(False, False)

# Frame to hold games
game_frame = tk.Frame(root)
game_frame.pack(pady=20)

# ========================== Catch the Ball Game ==========================

def catch_the_ball_game():
    # Clear previous game components
    for widget in game_frame.winfo_children():
        widget.destroy()

    # Set up canvas for the Catch the Ball game
    canvas = tk.Canvas(game_frame, width=400, height=400, bg="lightblue")
    canvas.pack()

    # Paddle
    paddle = canvas.create_rectangle(150, 380, 250, 390, fill="black")

    # Ball
    ball = canvas.create_oval(190, 10, 210, 30, fill="red")

    # Ball movement
    ball_speed = [3, 4]  # [x-speed, y-speed]
    score = 0

    # Score display
    score_label = tk.Label(game_frame, text=f"Score: {score}", font=("Arial", 14))
    score_label.pack()

    def move_ball():
        """Moves the ball and checks for collisions."""
        nonlocal score
        x1, y1, x2, y2 = canvas.coords(ball)
        if x1 <= 0 or x2 >= 400:
            ball_speed[0] = -ball_speed[0]
        if y1 <= 0:
            ball_speed[1] = -ball_speed[1]
        
        # Paddle collision
        px1, py1, px2, py2 = canvas.coords(paddle)
        if py1 <= y2 <= py2 and px1 <= x1 <= px2:
            ball_speed[1] = -ball_speed[1]
            score += 1  # Increase score when the ball hits the paddle
            score_label.config(text=f"Score: {score}")

        # Game over condition
        if y2 >= 400:
            canvas.create_text(200, 200, text="Game Over!", font=("Arial", 20), fill="red")
            canvas.create_text(200, 250, text=f"Final Score: {score}", font=("Arial", 14), fill="black")
            restart_button.pack()  # Show restart button
            return  # Stop the game
        
        canvas.move(ball, ball_speed[0], ball_speed[1])
        root.after(30, move_ball)

    def move_paddle(event):
        """Moves the paddle left and right."""
        x1, _, x2, _ = canvas.coords(paddle)
        if event.keysym == "Left" and x1 > 0:
            canvas.move(paddle, -20, 0)
        elif event.keysym == "Right" and x2 < 400:
            canvas.move(paddle, 20, 0)

    def restart_game():
        """Restarts the game by resetting ball position and score."""
        nonlocal score, ball_speed
        score = 0
        score_label.config(text=f"Score: {score}")
        canvas.coords(ball, 190, 10, 210, 30)
        canvas.coords(paddle, 150, 380, 250, 390)
        ball_speed = [3, 4]  # Reset ball speed
        restart_button.pack_forget()  # Hide restart button
        move_ball()

    # Restart button
    restart_button = tk.Button(game_frame, text="Restart", font=("Arial", 14), command=restart_game)

    # Bind keyboard events
    root.bind("<Left>", move_paddle)
    root.bind("<Right>", move_paddle)

    # Start the game loop
    move_ball()

# ========================== Tic-Tac-Toe Game ==========================

def tic_tac_toe_game():
    # Clear previous game components
    for widget in game_frame.winfo_children():
        widget.destroy()

    # Tic-Tac-Toe setup
    board = ["", "", "", "", "", "", "", "", ""]
    current_player = "X"
    game_active = True

    def render_board():
        for i in range(9):
            button = tk.Button(game_frame, text=board[i], font=("Arial", 24), width=10, height=3, bg="#ADD8E6",
                               command=lambda i=i: make_move(i))
            button.grid(row=i // 3, column=i % 3, padx=5, pady=5)

    def make_move(index):
        nonlocal current_player
        if board[index] == "" and game_active:
            board[index] = current_player
            current_player = "O" if current_player == "X" else "X"
            render_board()
            check_winner()

    def check_winner():
        nonlocal game_active
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],
            [0, 3, 6], [1, 4, 7], [2, 5, 8],
            [0, 4, 8], [2, 4, 6]
        ]
        for combo in winning_combinations:
            if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != "":
                game_active = False
                messagebox.showinfo("Game Over", f"{board[combo[0]]} wins!")
                return
        if "" not in board:
            game_active = False
            messagebox.showinfo("Game Over", "It's a tie!")

    render_board()

# ========================== Snake Game ==========================

def snake_game():
    # Clear previous game components
    for widget in game_frame.winfo_children():
        widget.destroy()

    # Snake Game setup
    canvas = tk.Canvas(game_frame, width=400, height=400, bg="black")
    canvas.pack()

    # Snake variables
    snake = [(100, 100), (90, 100), (80, 100)]
    direction = 'Right'
    food = [(random.randint(0, 39) * 10, random.randint(0, 39) * 10)]
    score = 0

    def draw_snake():
        for segment in snake:
            canvas.create_rectangle(segment[0], segment[1], segment[0] + 10, segment[1] + 10, fill="green")

    def draw_food():
        canvas.create_rectangle(food[0][0], food[0][1], food[0][0] + 10, food[0][1] + 10, fill="red")

    def move_snake():
        nonlocal score
        head_x, head_y = snake[0]
        if direction == 'Right':
            head_x += 10
        elif direction == 'Left':
            head_x -= 10
        elif direction == 'Up':
            head_y -= 10
        elif direction == 'Down':
            head_y += 10
        new_head = (head_x, head_y)
        snake = [new_head] + snake[:-1]

        # Check collision with wall or self
        if head_x < 0 or head_x >= 400 or head_y < 0 or head_y >= 400 or new_head in snake[1:]:
            canvas.create_text(200, 200, text="Game Over!", font=("Arial", 20), fill="red")
            return

        # Check if snake eats food
        if new_head == food[0]:
            snake.append(snake[-1])
            food[0] = (random.randint(0, 39) * 10, random.randint(0, 39) * 10)
            score += 1
            canvas.create_text(200, 20, text=f"Score: {score}", font=("Arial", 14), fill="white")
        
        canvas.delete("all")
        draw_snake()
        draw_food()
        root.after(100, move_snake)

    def change_direction(event):
        nonlocal direction
        if event.keysym == 'Left' and direction != 'Right':
            direction = 'Left'
        elif event.keysym == 'Right' and direction != 'Left':
            direction = 'Right'
        elif event.keysym == 'Up' and direction != 'Down':
            direction = 'Up'
        elif event.keysym == 'Down' and direction != 'Up':
            direction = 'Down'

    root.bind("<Left>", change_direction)
    root.bind("<Right>", change_direction)
    root.bind("<Up>", change_direction)
    root.bind("<Down>", change_direction)

    move_snake()

# ========================== Game Switcher ==========================

def switch_game(game_name):
    if game_name == "Catch the Ball":
        catch_the_ball_game()
    elif game_name == "Tic-Tac-Toe":
        tic_tac_toe_game()
    elif game_name == "Snake":
        snake_game()

# ========================== Landing Page ==========================

def create_landing_page():
    # Clear any existing games
    for widget in game_frame.winfo_children():
        widget.destroy()

    # Heading
    title_label = tk.Label(game_frame, text="Welcome to Ultimate Game Hub", font=("Arial", 24), bg="lightblue")
    title_label.pack(pady=20)

    # Game Selection Buttons
    button_frame = tk.Frame(game_frame)
    button_frame.pack()

    catch_button = tk.Button(button_frame, text="Catch the Ball", font=("Arial", 14), width=20, height=2,
                             command=lambda: switch_game("Catch the Ball"))
    catch_button.grid(row=0, column=0, padx=10, pady=10)

    tic_button = tk.Button(button_frame, text="Tic-Tac-Toe", font=("Arial", 14), width=20, height=2,
                           command=lambda: switch_game("Tic-Tac-Toe"))
    tic_button.grid(row=0, column=1, padx=10, pady=10)

    snake_button = tk.Button(button_frame, text="Snake", font=("Arial", 14), width=20, height=2,
                             command=lambda: switch_game("Snake"))
    snake_button.grid(row=1, column=0, padx=10, pady=10)

# ========================== Main Execution ==========================

create_landing_page()

# Run the main loop
root.mainloop()
