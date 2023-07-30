import pygame
import math
from queue import PriorityQueue
import pygame_menu

# Screen parameters
WIDTH = 600
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* algo viz")

# Colors codes
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


# Single node class

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_close(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = ORANGE

    def make_end(self):
        self.color = TURQUOISE

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])

    def __lt__(self, other):
        return False


# herestic function

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Path reconstruction

def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        if (not current.is_start()):
            current.make_path()
        draw()


# main algorithm

def AStarAlgorithm(draw, grid, start, end):
    draw()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # assume all edges are equal to 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False


def DijkstraAlgorithm(draw, grid, start, end):
    draw()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # assume all edges are equal to 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score

                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((0, count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        if current != start:
            current.make_closed()
    return False


def algorithm(draw, grid, start, end, algoType):
    if algoType == 0:
        AStarAlgorithm(draw, grid, start, end)
    else:
        DijkstraAlgorithm(draw, grid, start, end)


# building the base grid

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            if i == 0 or i == rows - 1 or j == 0 or j == rows - 1:
                node.make_barrier()
            grid[i].append(node)
    return grid


# Drawing the grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


# drawing each frame

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


# Getting correct clicked row and col

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    col = x // gap
    return row, col


# Main function

def main(win, width, algoType):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                if not (row == 0 or row == ROWS - 1 or col == 0 or col == ROWS - 1):
                    node = grid[row][col]
                    if not start and node != end:
                        start = node
                        start.make_start()
                    elif not end and node != start:
                        end = node
                        end.make_end()
                    elif node != end and node != start:
                        node.make_barrier()
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end, algoType)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_BACKSPACE:
                    run = False

    showMainMenu()


def startAStarAlgo():
    main(WIN, WIDTH, 0)


def startDijkstraAlgo():
    main(WIN, WIDTH, 1)


def showHelp():
    menu.close()
    helpMenu.mainloop(WIN)


def showMainMenu():
    helpMenu.close()
    menu.mainloop(WIN)


pygame.init()

# Help Menu
HELP = "Add start,end and block nodes with Left Mouse "\
       "Press <Space> to start and <C> to clear the screen "\
       "Press <BackSpace> to return to main menu "

helpMenu = pygame_menu.Menu('Help Menu', WIDTH, WIDTH,
                            theme=pygame_menu.themes.THEME_DARK)
helpMenu.add.button("Main menu", showMainMenu)
helpMenu.add.vertical_margin(50)
helpMenu.add.label("Add start,end and block nodes with Left Mouse",max_char=-1,font_size=18)
helpMenu.add.label("Press <Space> to start and <C> to clear the screen",max_char=-1,font_size=18)
helpMenu.add.label("Press <BackSpace> to return to main menu",max_char=-1,font_size=18)

helpMenu.add.vertical_margin(50)
helpMenu.add.label("More info here")
helpMenu.add.url("https://en.wikipedia.org/wiki/A*_search_algorithm", "A* Algorithm")
helpMenu.add.url("https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm", "Dijkstra's Algorithm")

# Main Menu
menu = pygame_menu.Menu('Welcome', WIDTH, WIDTH,
                        theme=pygame_menu.themes.THEME_DARK)
menu.add.label('Pathfinding Visualizer')
menu.add.vertical_margin(100)
menu.add.button('A* algorithm', startAStarAlgo)
menu.add.button("Dijkstra's algorithm", startDijkstraAlgo)
menu.add.button('Help', showHelp)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.add.vertical_margin(100)
menu.add.url("https://www.linkedin.com/in/semeh-chriha/","My LinkedIn")
menu.mainloop(WIN)
