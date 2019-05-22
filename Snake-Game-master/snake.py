#   Grzegorz Jarzabek
#       15.11.2018
# ********Snake**********

from tkinter import *

import sys

import random as rn

# Parametry projektu

WIDTH: int = 880  # szerokosc okna
HEIGHT: int = 480  # wysokosc okna
GAME_NAME: str = "Snake by G.J"  # nazwa okna
ELEMENT_SIZE: int = 40  # wielkosc jednego elementu weza/pozywienia 40x40
SNAKE_SPEED: int = 205  # szybkosc weza
COLUMNS: int = 22
ROWS: int = 12


class Cube(object):

    def __init__(self, xe, ye):
        self.x = int(xe)
        self.y = int(ye)


class Head(Cube):

    def __init__(self, xe, ye):
        super().__init__(xe, ye)


class Food(Cube):

    def __init__(self, xe, ye):
        super().__init__(xe, ye)

    def spawn(self):
        self.x = rn.randint(1, COLUMNS - 2)
        self.y = rn.randint(1, ROWS - 2)


class Snake(object):

    def __init__(self, field):
        self.field = field
        self.head = Head(WIDTH / 2, HEIGHT / 2)
        field[int(WIDTH / 2 / ELEMENT_SIZE)][int(HEIGHT / 2 / ELEMENT_SIZE)] = 1
        self.body = [self.head]
        self.pictures_list = [0] * 4
        self.current_direction = 0
        self.directions = [[1, 0], [-1, 0], [0, -1], [0, 1]]
        for i in range(3):
            x = int(WIDTH / 2 - (i + 1) * ELEMENT_SIZE)
            y = int(HEIGHT / 2)
            self.body.append(Cube(x, y))
            field[int(x / ELEMENT_SIZE)][int(y / ELEMENT_SIZE)] = 1


class GameField(Frame):

    def __init__(self, container, food_image, app):
        super().__init__(container)
        self.score = 0
        self.app = app
        self.game_field = Canvas(self, width=WIDTH, height=HEIGHT)
        self.game_field.create_rectangle(0, 0, WIDTH, HEIGHT, fill="#000000")
        self.finish = False # true jesli koniec gry

        self.game_field.create_rectangle(0, 0, WIDTH, ELEMENT_SIZE, fill="#2D3B2D", outline="")
        self.game_field.create_rectangle(0, HEIGHT - ELEMENT_SIZE, WIDTH, HEIGHT, fill="#2D3B2D", outline="")
        self.game_field.create_rectangle(0, 0, ELEMENT_SIZE, HEIGHT, fill="#2D3B2D", outline="")
        self.game_field.create_rectangle(WIDTH - ELEMENT_SIZE, 0, WIDTH, HEIGHT, fill="#2D3B2D", outline="")
        self.text = self.game_field.create_text((690, 8), text=f"Score: {self.score}", font=("Wendy One", 28), anchor=NW)

        self.pause_id = PhotoImage(file="pause.png")
        self.resume_id = PhotoImage(file="resume.png")
        self.button1 = Button(self, image=self.pause_id, highlightthickness=0, bd=0, anchor=NW)
        self.game_field.bind_all("<KeyPress-space>", self.pause)
        self.button1_id = self.game_field.create_window(40, 9.1, anchor=NW, window=self.button1)
        self.pause_butt = False

        self.direction_change = True
        self.pause = False

        self.game_field.bind_all("<KeyPress-Left>", self.change_direction)
        self.game_field.bind_all("<KeyPress-Right>", self.change_direction)
        self.game_field.bind_all("<KeyPress-Up>", self.change_direction)
        self.game_field.bind_all("<KeyPress-Down>", self.change_direction)

        self.key_codes = {37: 1, 38: 2, 39: 0, 40: 3}

        self.food_image = food_image
        self.game_field.pack()

        # tablica mowiaca o wolnym miejscu na planszy, 0- wolne, 1 - cialo snake'a, 2 - jedzenie
        self.spaces = [[0] * ROWS for i in range(COLUMNS)]
        for i in range(ROWS):
            self.spaces[0][i] = 1
            self.spaces[COLUMNS - 1][i] = 1
        for i in range(1, COLUMNS - 1):
            self.spaces[i][0] = 1
            self.spaces[i][ROWS - 1] = 1

        self.snake = Snake(self.spaces)
        self.food = Food(COLUMNS / 2 + 4, ROWS / 2)
        self.food_on_field = self.place_food()
        self.draw_snake()

        self.game_field.pack()
        self.timer = 3
        self.id_text = None

    def delay(self):
        if self.timer >= 1:
            if self.id_text is not None:
                self.game_field.delete(self.id_text)
            self.id_text = self.game_field.create_text((WIDTH/2, HEIGHT/2), text=f"{self.timer}", font=("Wendy One", 60), fill="red", anchor=NW)
            self.timer -= 1
            self.app.after(700, self.delay)
        else:
            self.game_field.delete(self.id_text)
            self.run()

    def pause(self, event):
        if self.pause:
            self.pause = False
            self.button1.config(image=self.pause_id)
            self.run()
        else:
            self.pause = True
            self.button1.config(image=self.resume_id)

    def change_direction(self, event):
        snake = self.snake
        if self.direction_change:
            index = self.key_codes[event.keycode]
            if snake.current_direction > 1:
                if index < 2:
                    snake.current_direction = index
                    self.direction_change = False
            else:
                if index > 1:
                    snake.current_direction = index
                    self.direction_change = False
        else:
            pass

    def end_game(self):
        self.finish = True
        self.score = 0

    def draw_snake(self):
        length = len(self.snake.body)
        for i in range(length):
            self.snake.pictures_list[i] = self.game_field.create_rectangle(self.snake.body[i].x,
                                                                           self.snake.body[i].y,
                                                                           self.snake.body[i].x + ELEMENT_SIZE,
                                                                           self.snake.body[i].y + ELEMENT_SIZE,
                                                                           fill="#ffffff")  # , outline="white")

    def move_snake(self):
        snake = self.snake

        new_x: int = int(snake.head.x + snake.directions[snake.current_direction][0] * ELEMENT_SIZE)
        new_y: int = int(snake.head.y + snake.directions[snake.current_direction][1] * ELEMENT_SIZE)
        growth = False

        if self.spaces[int(new_x / ELEMENT_SIZE)][int(new_y / ELEMENT_SIZE)] == 1:
            self.end_game()
            return
        elif self.spaces[int(new_x / ELEMENT_SIZE)][int(new_y / ELEMENT_SIZE)] == 2:
            growth = True
            self.delete_food()
            self.score += 1
            self.game_field.delete(self.text)
            self.text = self.game_field.create_text((690, 8), text=f"Score: {self.score}", font=("Wendy One", 28),
                                                    anchor=NW)
        if growth:
            self.game_field.delete(self.food_on_field)
            snake.body.insert(1, Cube(snake.head.x, snake.head.y))
            snake.pictures_list.append(1)
        else:
            body_len = len(snake.body)
            self.spaces[int(snake.body[body_len - 1].x / ELEMENT_SIZE)][
                int(snake.body[body_len - 1].y / ELEMENT_SIZE)] = 0
            for i in range(body_len - 1, 0, -1):
                snake.body[i].x = snake.body[i - 1].x
                snake.body[i].y = snake.body[i - 1].y

        self.spaces[int(new_x / ELEMENT_SIZE)][int(new_y / ELEMENT_SIZE)] = 1
        snake.head.x = new_x
        snake.head.y = new_y
        if growth:
            self.food.spawn()
            while self.spaces[self.food.x][self.food.y] != 0:
                self.food.spawn()
            self.spaces[self.food.x][self.food.y] = 2
            self.food_on_field = self.place_food()

    def place_food(self):
        self.spaces[self.food.x][self.food.y] = 2
        return self.game_field.create_image((self.food.x * ELEMENT_SIZE, self.food.y * ELEMENT_SIZE),
                                            image=self.food_image, anchor=NW)

    def delete_snake(self):
        for i in range(len(self.snake.pictures_list)):
            self.game_field.delete(self.snake.pictures_list[i])

    def delete_food(self):
        self.game_field.delete(self.food_on_field)

    def action(self):
        self.delete_snake()
        self.move_snake()
        self.draw_snake()
        self.direction_change = True

    def run(self):

        if self.timer >= 1:
            self.delay()
        else:
            if self.pause:
                pass
            elif not self.finish:
                self.action()
                self.app.after(SNAKE_SPEED, self.run)
            else:
                self.app.score = len(self.snake.body)
                self.app.finish_play()


class StartMenu(Frame):
    def __init__(self, root, app):
        super().__init__(root)
        self.start_menu_image = PhotoImage(file="b_last.png")
        self.start_menu_field = Label(self, image=self.start_menu_image)

        self.butt1_image = PhotoImage(file="butt1.png")
        self.butt2_image = PhotoImage(file="butt2.png")
        self.play_butt = Button(self, image=self.butt1_image, highlightthickness=0, bd=0, command=app.play)
        self.exit_butt = Button(self, image=self.butt2_image, highlightthickness=0, bd=0, command=sys.exit)

        self.start_menu_field.pack()
        self.play_butt.place(x=318.1, y=123.5)
        self.exit_butt.place(x=318.1, y=283)


class AfterGame(Frame):
    def __init__(self, container, root):
        super().__init__(container)
        self.back_img_id = PhotoImage(file="after.png")
        self.background = Canvas(self, width=WIDTH, height=HEIGHT)
        self.background.pack()
        self.background.create_image((0, 0), image=self.back_img_id, anchor=NW)
        self.img_id = PhotoImage(file="dalej.png")
        button1 = Button(self, image=self.img_id, command=root.show_start, highlightthickness=0, bd=0, anchor=NW)
        self.button1_id = self.background.create_window(330.5, 342 , anchor=NW, window=button1)
        self.score_id = self.background.create_text((395, 205.5), anchor=NW, text=0, font=("Wendy One", 100), fill="white")

    def put_score(self, score):
        self.background.delete(self.score_id)
        x = 376
        if score < 10:
            x = 395
        self.score_id = self.background.create_text((x, 200.5), anchor=NW, text=score, font=("Wendy One", 100), fill="white")


class RunApp(Tk):
    def __init__(self):
        super().__init__()

        self.title(GAME_NAME)
        self.geometry(F"{WIDTH}x{HEIGHT}")
        self.maxsize(width=WIDTH,height=HEIGHT)
        self.minsize(width=WIDTH, height=HEIGHT)
        self.iconbitmap("icona.ico")
        self.food_image = PhotoImage(file="food.png")

        self.container = Frame(self)

        self.gf = GameField(self.container, self.food_image, self)
        self.sm = StartMenu(self.container, self)
        self.after_game = AfterGame(self.container, self)

        self.sm.pack()
        self.gf.pack()

        self.container.pack()

    def play(self):
        self.sm.pack_forget()
        self.gf.pack()
        self.gf.run()

    def finish_play(self):
        self.after_game.put_score(len(self.gf.snake.body))
        self.gf.destroy()
        self.gf = GameField(self.container, self.food_image, self)
        self.after_game.pack()

    def show_start(self):
        self.after_game.pack_forget()
        self.sm.pack()


r = RunApp()
r.mainloop()
