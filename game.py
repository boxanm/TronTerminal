import random
import curses
import time

###COLORS
#Player 1 - white 0 248 236
#Player 2 - blue 22 20 18
#Player 3 - green 47 43 23
#Player 4 - violent 202 213 55

COLORS =  {
            0: [0, 248, 236],
            1: [22, 20, 18],
            2: [47, 43, 23],
            3: [202, 213, 55]
            }

class Player:
    def __init__(self, index):
        self.number = index
        self.bike = None
        self.score = 0
        if(index == 0):
            self.controls = ['<','>','/\\','\\/']
        elif(index==1):
            self.controls = ['a','d','w','s']
        elif(index==2):
            self.controls = ['j','l','i','k']
        elif(index==3):
            self.controls = ['v','n','g','b']
    def match_bike(self, bike):
        self.bike = bike
        self.bike.player = self
    def add_victory(self):
        self.score += 1
    def get_controls(self):
        return self.controls

class Position:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid

    def is_free(self):
        return self.grid[self.x][self.y] == 0
    def __str__(self):
        return str(self.x) + " " + str(self.y)
    def __eq__(self, other):
        if(other == None):
            return False
        return self.x == other.x and self.y == other.y

class Motorbike:
    def __init__(self, color, char, grid, position = None, direction = None):
        self.colors = COLORS[color]
        self.color_index = 0
        self.color = self.colors[self.color_index]
        self.char = char
        # 0 - left, 1 -  right, 2 - down, 3 - up
        if(direction == None):
            self.direction = random.randint(0,3)
        else:
            self.direction = direction
        self.prev_direction = self.direction
        if(position == None):
            self.position = Position(random.randint(10, len(grid)-10), random.randint(10, len(grid[0])-10), grid)
        else:
            self.position = position
        if(self.direction == 0):
            self.position_rear = Position(self.position.x, self.position.y-1, grid)
        elif(self.direction == 1):
            self.position_rear = Position(self.position.x, self.position.y+1, grid)
        elif(self.direction == 2):
            self.position_rear = Position(self.position.x-1, self.position.y, grid)
        elif(self.direction == 3):
            self.position_rear = Position(self.position.x+1, self.position.y, grid)

        self.position_last = Position(self.position_rear.x, self.position_rear.y, grid)
    def get_position(self):
        return self.position.x, self.position.y

    def move_row_down(self):
        self.position_last.x = self.position_rear.x
        self.position_last.y = self.position_rear.y
        self.position_rear.x = self.position.x
        self.position_rear.y = self.position.y
        self.position.x += 1
    def move_row_up(self):
        self.position_last.x = self.position_rear.x
        self.position_last.y = self.position_rear.y
        self.position_rear.x = self.position.x
        self.position_rear.y = self.position.y
        self.position.x -= 1
    def move_col_right(self):
        self.position_last.x = self.position_rear.x
        self.position_last.y = self.position_rear.y
        self.position_rear.x = self.position.x
        self.position_rear.y = self.position.y
        self.position.y += 1
    def move_col_left(self):
        self.position_last.x = self.position_rear.x
        self.position_last.y = self.position_rear.y
        self.position_rear.x = self.position.x
        self.position_rear.y = self.position.y
        self.position.y -= 1
    def render(self, win, counter, grid):
        win.attron(curses.color_pair(self.color))
        win.addch(self.position_last.x, self.position_last.y, self.char)
        win.addch(self.position_rear.x, self.position_rear.y, 'o')
        win.addch(self.position.x, self.position.y, 'o')
        win.attroff(curses.color_pair(self.color))

class MotorbikeGame(Motorbike):
    def __init__(self, color, char, number, grid, player, position = None, direction = None):
        super().__init__(color, char, grid, position, direction)
        self.player = player
        self.number = number
        self.is_alive = True

    def setDead(self):
        self.is_alive = False

    def check_collision(self):
        return not self.position.is_free()
    def move_row_down(self):
        if(self.is_alive):
            super().move_row_down()
    def move_row_up(self):
        if(self.is_alive):
            super().move_row_up()
    def move_col_right(self):
        if(self.is_alive):
            super().move_col_right()
    def move_col_left(self):
        if(self.is_alive):
            super().move_col_left()
    def render(self, win, counter, grid):
        if(self.is_alive):
            if(counter % 20 == 0 or counter % 20 == 1):
                win.attron(curses.color_pair(self.color))
                win.addch(self.position_last.x, self.position_last.y, ' ')
                win.addch(self.position_rear.x, self.position_rear.y, ' ')
                win.addch(self.position.x, self.position.y, 'o')
                win.attroff(curses.color_pair(self.color))

                grid[self.position_last.x][self.position_last.y] = 0
                grid[self.position_rear.x][self.position_rear.y] = 0

            else:
                win.attron(curses.color_pair(self.color))
                win.addch(self.position_last.x, self.position_last.y, self.char)
                win.addch(self.position_rear.x, self.position_rear.y, 'o')
                win.addch(self.position.x, self.position.y, 'o')
                win.attroff(curses.color_pair(self.color))

                grid[self.position_rear.x][self.position_rear.y] = 1
                grid[self.position.x][self.position.y] = 1
        else:
            if(self.color_index < len(self.colors)):
                self.color = self.colors[self.color_index]
                win.attron(curses.color_pair(self.color))
                if(self.color_index == 0):
                    self.position = self.position_rear
                    win.addch(self.position.x, self.position.y, curses.ACS_CKBOARD)

                elif(self.color_index == 1):
                    for r in range(self.position.x-1, self.position.x+2):
                        for c in range(self.position.y-1, self.position.y+2):
                            if r >= 0 and c >= 0 and r <= len(grid) and c <= len(grid[0]):
                                if not grid[r][c]:
                                    win.addch(r, c, curses.ACS_CKBOARD)

                elif(self.color_index == 2):
                    r = self.position.x - 2
                    for c in range(self.position.y-2, self.position.y+3):
                        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0]):
                            if not grid[r][c]:
                                win.addch(r, c, curses.ACS_CKBOARD)

                    r = self.position.x + 2
                    for c in range(self.position.y-2, self.position.y+3):
                        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0]):
                            if not grid[r][c]:
                                win.addch(r, c, curses.ACS_CKBOARD)

                    c = self.position.y - 2
                    for r in range(self.position.x-2, self.position.x+3):
                        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0]):
                            if not grid[r][c]:
                                win.addch(r, c, curses.ACS_CKBOARD)

                    c = self.position.y + 2
                    for r in range(self.position.x-2, self.position.x+3):
                        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0]):
                            if not grid[r][c]:
                                win.addch(r, c, curses.ACS_CKBOARD)

                win.attroff(curses.color_pair(self.color))
                self.color_index += 1

            elif(self.color_index == len(self.colors)):
                self.color_index += 1
                win.attron(curses.color_pair(self.colors[0]))
                win.addch(self.position.x, self.position.y, 'o')
                for r in range(self.position.x-2, self.position.x+3):
                    for c in range(self.position.y-2, self.position.y+3):
                        if r >= 0 and c >= 0 and r < len(grid) and c < len(grid[0]):
                            if not grid[r][c]:
                                win.addch(r, c, ' ')
                win.attroff(curses.color_pair(self.color))

class Game:
    def __init__(self, sc):
        self.sc = sc

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

        self.players_controls = {}
        self.chars = []
        self.grid = []
        self.bikes = []

        self.h, self.w = sc.getmaxyx()
        self.win = curses.newwin(self.h, self.w, 0, 0)
        self.win.keypad(1)
        curses.curs_set(0)

        self.chars = [curses.ACS_CKBOARD, '#', '*', '|']

        self.all_players_controls = [
                                    {curses.KEY_UP: 0, curses.KEY_LEFT: 0, curses.KEY_DOWN: 0, curses.KEY_RIGHT: 0},
                                    {ord('w'): 1, ord('a'): 1, ord('s'): 1, ord('d'): 1},
                                    {ord('i'): 2, ord('j'): 2, ord('k'): 2, ord('l'): 2},
                                    {ord('g'): 3, ord('v'): 3, ord('b'): 3, ord('n'): 3}
                                    ]

    def init_grid(self):
        self.grid = []
        for x in range(self.h):
            self.grid.append([])
            for y in range(self.w):
                if x == 0 or x == self.h-1 or y == 0 or y == self.w-1:
                    self.grid[x].append(1)
                else:
                    self.grid[x].append(0)

    def init_bikes(self, players):
        num_of_players = len(players)
        self.bikes = []
        for i in range(num_of_players):
            self.players_controls.update(self.all_players_controls[i])
            self.bikes.append(MotorbikeGame(i, self.chars[i], i, self.grid, players[i]))
            players[i].match_bike(self.bikes[-1])

    def render_bikes(self):
        for bike in self.bikes:
            bike.render(self.win, 0, self.grid)

    def play(self, players):
        num_of_players = len(players)

        self.win.clear()
        self.init_grid()
        self.init_bikes(players)
        self.render_bikes()
        prev_button_direction = 1
        button_direction = 1
        key = curses.KEY_RIGHT

        counter = 0
        num_of_players_alive = num_of_players



        self.win.border()
        self.win.refresh()

        while True:
            self.win.timeout(200)
            counter += 1

            next_key = self.win.getch()

            if next_key == -1:
                key = key
            else:
                key = next_key

            # 0-Left, 1-Right, 3-Up, 2-Down
            if key in self.players_controls.keys():
                player_index = self.players_controls[key]

                if keyLeft(key) and self.bikes[player_index].prev_direction != 1:
                    self.bikes[player_index].direction = 0
                elif keyRight(key) and self.bikes[player_index].prev_direction != 0:
                    self.bikes[player_index].direction = 1
                elif keyUp(key) and self.bikes[player_index].prev_direction != 2:
                    self.bikes[player_index].direction = 3
                elif keyDown(key) and self.bikes[player_index].prev_direction != 3:
                    self.bikes[player_index].direction = 2

            for bike in self.bikes:
                bike.prev_direction = bike.direction

                if bike.direction == 0:
                    bike.move_col_left()
                elif bike.direction == 1:
                    bike.move_col_right()
                elif bike.direction == 3:
                    bike.move_row_up()
                elif bike.direction == 2:
                    bike.move_row_down()

                if(bike.check_collision() and bike.is_alive):
                    bike.setDead()
                    num_of_players_alive -= 1
                    if(num_of_players_alive == 1):
                        for bike in self.bikes:
                            if bike.is_alive:
                                bike.player.add_victory()
                                winner = bike.player
                                break

                bike.render(self.win, counter, self.grid)


            if(num_of_players_alive == 0):
                break


        if(num_of_players == 1):
            winner = self.bikes[0].player
            winner.add_victory()
        for i in range(3):
            self.win.timeout(200)
            next_key = self.win.getch()
            winner.bike.render(self.win, 0, self.grid)


        self.game_over(winner)

    def game_over(self, winner):
        self.sc.clear()
        self.sc.addstr(round(self.h/2), round(self.w/2), "GAME OVER")
        self.sc.addstr(round(self.h/2)+2, round(self.w/2), "Player " + str(winner.number) + " won")
        self.sc.refresh()
        counter = 0
        while(True):
            key = self.sc.getch()
            if key != curses.ERR or counter == 3000/200:
                break
            self.sc.timeout(200)
            counter += 1
        self.sc.clear()

    def show_score(self):
        self.sc.clear()
        self.sc.addstr(round(self.h/2), round(self.w/2), "SCORE")
        for bike in self.bikes:
            self.sc.addstr(round(self.h/2)+2+bike.player.number, round(self.w/2), "Player " + str(bike.player.number) + " won " + str(bike.player.score) + " times")
        self.sc.refresh()
        counter = 0
        while(True):
            key = self.sc.getch()
            if key != curses.ERR or counter == 3000/200:
                break
            counter += 1
        self.sc.clear()

def keyUp(key):
    return (chr(key) == 'g' or chr(key) == 'i' or chr(key) == 'w' or key == curses.KEY_UP)

def keyDown(key):
    return (chr(key) == 'b' or chr(key) == 'k' or chr(key) == 's' or key == curses.KEY_DOWN)

def keyRight(key):
    return (chr(key) == 'n' or chr(key) == 'l' or chr(key) == 'd' or key == curses.KEY_RIGHT)

def keyLeft(key):
    return (chr(key) == 'v' or chr(key) == 'j' or chr(key) == 'a' or key == curses.KEY_LEFT)
