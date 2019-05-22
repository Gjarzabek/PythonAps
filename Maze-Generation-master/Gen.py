# Maze generation
# Depth-first search with stack backtracker

rows = 20
column = 20
size = 38


from random import *
from tkinter import  *


def coordinates(x, y):
    return (x * size, y * size)

class Cell(object):

    def __init__(self, i, j):
        self.x = i
        self.y = j
        self.visited = False
        self.walls = (True, True, True, True) #     left, right, up, down
        self.lines_ids = [0 for i in range(4)]

    def show(self, canv):
        for i in range(2):
            if self.walls[i]:
                self.lines_ids[i] = canv.create_line(coordinates(self.x + i, self.y + i),
                                                     coordinates(self.x + i, self.y + i + 1), fill="white")
            if self.walls[i+2]:
                self.lines_ids[i+2] = canv.create_line(coordinates(self.x + i, self.y + i),
                                                       coordinates(self.x + i + 1, self.y + i), fill="white")

    def del_wall(self, canv,index):
        canv.delete(self.lines_ids[index])


class Maze(Tk):

    def __init__(self):
        super().__init__()
        self.minsize(width=column * size, height=rows * size)
        self.maxsize(width=column * size, height=rows * size)
        self.canvas = Canvas(self, width=column * size, height=rows * size)
        self.canvas.pack()
        self.maze = []
        self.background = []

        for i in range(column):
            for j in range(rows):
                self.maze.append(Cell(i, j))

        self.all_cells = len(self.maze)
        self.visited_cells = 0
        self.stack = []
        self.current = self.maze[0]
        self.current_id_img = self.canvas.create_rectangle(coordinates(0,0), coordinates(1,1), fill="#330033")

    @staticmethod
    def index(i, j):
        return i*column + j

    def draw_background(self):
        for i in range(column):
            for j in range(rows):
                id = self.canvas.create_rectangle(coordinates(i,j),coordinates(i+1,j+1),
                                                  fill="black", outline="")
                self.background.append(id)

    def draw_maze(self):
        for cell in self.maze:
            cell.show(self.canvas)

    def destroy_wall(self):
        pass

    def add(self, first):
        first.visited = True
        self.visited_cells += 1
        x = first.x
        y = first.y
        id = Maze.index(x, y)
        self.canvas.delete(self.background[id])
        self.background[id] = self.canvas.create_rectangle(coordinates(x,y),coordinates(x+1,y+1),
                                                  fill="purple", outline="white")

    def has_unvisited(self, current: Cell):
        has = False
        neigbours = ((1, 0), (-1, 0), (0, 1), (0, -1))
        for v in neigbours:
            if current.x + v[0] > -1 and current.x + v[0] < column:
                if current.y + v[1] > -1 and current.y + v[1] < rows:
                    new: Cell = self.maze[Maze.index(current.x + v[0], current.y + v[1])]
                    if not new.visited:
                        has = True
        return has


    def neig_choose(self, current: Cell):
        neigbours = ((1, 0), (-1, 0), (0, 1), (0, -1))
        index = randint(0,3)
        in_tab = (current.x + neigbours[index][0], current.y + neigbours[index][1])
        while in_tab[0] < 0 or in_tab[0] > column - 1 or in_tab[1] < 0 or in_tab[1] > rows - 1 or self.maze[Maze.index(in_tab[0], in_tab[1])].visited:
            index = randint(0, 3)
            in_tab = (current.x + neigbours[index][0], current.y + neigbours[index][1])
        return self.maze[Maze.index(in_tab[0], in_tab[1])]

    def remove_wall(self, akt, next):
        dir = {(1, 0): (next.x, next.y, next.x, next.y + 1),
               (-1, 0): (akt.x, akt.y, akt.x, akt.y + 1),
               (0, 1): (next.x, next.y, next.x + 1, next.y),
               (0, -1): (akt.x, akt.y, akt.x + 1, akt.y)}
        v = (next.x - akt.x, next.y - akt.y)
        draw_from = coordinates(dir[v][0], dir[v][1])
        draw_to = coordinates(dir[v][2], dir[v][3])
        self.canvas.create_line(draw_from, draw_to, fill="purple")

    def generate(self):
        if self.visited_cells < self.all_cells:
            if self.has_unvisited(self.current):
                self.stack.append(self.current)
                next = self.neig_choose(self.current)
                self.add(next)
                self.remove_wall(self.current, next)
                self.current = next
                self.canvas.delete(self.current_id_img)
                self.current_id_img = self.canvas.create_rectangle(coordinates(next.x , next.y),
                                                                   coordinates(next.x + 1, next.y + 1),
                                                                   fill="#9966FF", outline="")
            elif len(self.stack) > 0:
                next = self.stack.pop()
                #while not self.has_unvisited(next):
                 #   next = self.stack.pop()
                self.canvas.delete(self.current_id_img)
                self.current_id_img = self.canvas.create_rectangle(coordinates(next.x , next.y),
                                                                   coordinates(next.x + 1, next.y + 1),
                                                                   fill="#9966FF", outline="")
                self.current = next

            self.after(25, self.generate)


m = Maze()
m.draw_background()
m.draw_maze()
m.add(m.current)
m.generate()
#self.canvas.create_line(coordinates(2, 2.03), coordinates(2, 2.99), fill="purple")
m.mainloop()