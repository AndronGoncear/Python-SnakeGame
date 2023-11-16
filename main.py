from tkinter import *
import random
import pygame

pygame.init()
eat_sound = pygame.mixer.Sound("eat.wav")
game_over_sound = pygame.mixer.Sound("game_over.wav")
GAME_WIDTH = 720
GAME_HEIGHT = 660
SPACE_SIZE = 30
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
game_running = False
level = 1
speed = 100


class Snake():
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

    def move(self, x, y):
        for i, square in enumerate(self.squares):
            new_x = self.coordinates[i][0] + x
            new_y = self.coordinates[i][1] + y
            canvas.move(square, x, y)
            self.coordinates[i] = [new_x, new_y]


class Food():
    def __init__(self):
        self.coordinates = []
        self.place_food()

    def place_food(self):
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")


def increase_difficulty():

    global speed
    speed -= 10


def next_turn():
    global game_running, snake, food, level
    if game_running:
        x, y = snake.coordinates[0]
        if (direction == "up"):
            y -= SPACE_SIZE
        elif (direction == "down"):
            y += SPACE_SIZE
        elif (direction == "left"):
            x -= SPACE_SIZE
        elif (direction == "right"):
            x += SPACE_SIZE

        snake.coordinates.insert(0, (x, y))
        square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
        snake.squares.insert(0, square)
        if hasattr(food, "coordinates") and x == food.coordinates[0] and y == food.coordinates[1]:
            global score
            score += 1
            eat_sound.play()
            label.config(text=f"Score: {score}  Level: {level}")
            canvas.delete("food")
            food.place_food()
            canvas.delete(snake.squares[-1])
            del snake.coordinates[-1]
            if score % 5 == 0:
                level += 1
                increase_difficulty()



        else:
            del snake.coordinates[-1]
            canvas.delete(snake.squares[-1])
            del snake.squares[-1]
        if check_collisions(snake):
            game_running = False
            game_over()
        else:
            window.after(speed, next_turn)


def change_direction(new_direction):
    global direction
    if new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction
    elif new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction


def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH:

        return True
    elif y < 0 or y >= GAME_HEIGHT:

        return True
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def start_game():
    global game_running, score,level
    global snake, food
    if not game_running:
        game_running = True
        score = 0
        level = 1
        label.config(text=f"Score: {score}  Level: {level}")
        canvas.delete("all")
        snake = Snake()
        food = Food()
        next_turn()


def stop_game():
    global game_running
    if game_running:
        game_running = False
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                           font=("Consolas", 30), text="Game Paused", fill="white", tag="paused")
    else:
        canvas.delete("paused")
        game_running = True
        resume_game()


def restart_game():
    global game_running, score, snake, food,level
    stop_game()
    canvas.delete(ALL)
    label.config(text="Press 'Start' to play")
    canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2, font=("Consolas", 30),
                       text="Press 'Start' to play", fill="white", tag="startscreen")
    game_running = False
    score = 0
    label.config(text=f"Score: {score}  Level: {level}")
    if snake:
        canvas.delete("snake")
    if food:
        canvas.delete("food")
    snake = None
    food = None


def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width() / 2, canvas.winfo_height() / 2,
                       font=("Consolas", 70), text="Game Over!!!", fill="red", tag="gameover")
    game_over_sound.play()


def pause_game():
    global game_running
    if game_running:
        game_running = False
        canvas.create_text(GAME_WIDTH / 2, GAME_HEIGHT / 2,
                           font=("Consolas", 30), text="Game Paused", fill="white", tag="paused")
    else:
        canvas.delete("paused")
        game_running = True
        resume_game()


def resume_game():
    global game_running
    if game_running:
        window.after(speed, next_turn)


window = Tk()
window.title("SNAKE_GAME")
window.resizable(False, False)
score = 0
direction = 'down'

label = Label(window, text="Press 'Start' to play!!!", font=("Consolas", 30))
label.pack()

canvas = Canvas(window, background=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))

window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))

window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))

window.bind("<a>", lambda event: change_direction("left"))
window.bind("<d>", lambda event: change_direction("right"))
window.bind("<w>", lambda event: change_direction("up"))
window.bind("<s>", lambda event: change_direction("down"))

window.bind("<Return>", lambda event: start_game())
window.bind("<Escape>", lambda event: stop_game())
window.bind("<r>", lambda event: restart_game())
window.bind("<p>", lambda event: pause_game())

snake = Snake()
food = Food()
next_turn()
window.mainloop()
pygame.quit()
