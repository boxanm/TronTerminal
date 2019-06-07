import random
import curses
import time

def render(player, win, counter, grid):
    if(counter % 20 == 0 or counter % 20 == 1):
        win.attron(player.color)
        win.addch(player.position_last.x, player.position_last.y, ' ')
        win.addch(player.position_rear.x, player.position_rear.y, ' ')
        win.addch(player.position.x, player.position.y, 'o')
        win.attroff(player.color)

        grid[player.position_last.x][player.position_last.y] = 0
        grid[player.position_rear.x][player.position_rear.y] = 0

    else:
        win.attron(player.color)
        win.addch(player.position_last.x, player.position_last.y, player.char)
        win.addch(player.position_rear.x, player.position_rear.y, 'o')
        win.addch(player.position.x, player.position.y, 'o')
        win.attroff(player.color)

        grid[player.position_rear.x][player.position_rear.y] = 1
        grid[player.position.x][player.position.y] = 1

class Position:
    def __init__(self, x, y, grid):
        self.x = x
        self.y = y
        self.grid = grid

    def is_free(self):
        return self.grid[self.x][self.y] == 0

class Player:
    def __init__(self, color, char, width, height, number, grid):
        self.number = number
        self.color = color
        self.char = char
        # 0-Up 1-Down, 2-Right, 3-Left
        self.direction = random.randint(0,3)
        self.prev_direction = self.direction
        self.position = Position(random.randint(10, height-10), random.randint(10, width-10), grid)
        if(self.direction == 0):
            self.position_rear = Position(self.position.x, self.position.y-1, grid)
        elif(self.direction == 1):
            self.position_rear = Position(self.position.x, self.position.y+1, grid)
        elif(self.direction == 2):
            self.position_rear = Position(self.position.x-1, self.position.y, grid)
        elif(self.direction == 3):
            self.position_rear = Position(self.position.x+1, self.position.y, grid)
        self.is_alive = True

        self.position_last = Position(self.position_rear.x, self.position_rear.y, grid)

    def check_collision(self):
        return not self.position.is_free()

    def get_position(self):
        return self.position.x, self.position.y

    def move_x_plus(self):
        if(self.is_alive):
            self.position_last.x = self.position_rear.x
            self.position_last.y = self.position_rear.y
            self.position_rear.x = self.position.x
            self.position_rear.y = self.position.y
            self.position.x += 1
    def move_x_minus(self):
        if(self.is_alive):
            self.position_last.x = self.position_rear.x
            self.position_last.y = self.position_rear.y
            self.position_rear.x = self.position.x
            self.position_rear.y = self.position.y
            self.position.x -= 1
    def move_y_plus(self):
        if(self.is_alive):
            self.position_last.x = self.position_rear.x
            self.position_last.y = self.position_rear.y
            self.position_rear.x = self.position.x
            self.position_rear.y = self.position.y
            self.position.y += 1
    def move_y_minus(self):
        if(self.is_alive):
            self.position_last.x = self.position_rear.x
            self.position_last.y = self.position_rear.y
            self.position_rear.x = self.position.x
            self.position_rear.y = self.position.y
            self.position.y -= 1
    def setDead(self):
        self.is_alive = False
    def getColor(self):
        return self.color

class Game:
    def __init__(self, sc, number_of_players):
        self.sc = sc
        self.num_of_players = number_of_players

        self.players_controls = {}
        self.colors = []
        self.chars = []
        self.grid = []
        self.players = []

        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)

        self.colors.append(curses.color_pair(1))
        self.colors.append(curses.color_pair(2))
        self.colors.append(curses.color_pair(3))

        self.h, self.w = sc.getmaxyx()
        self.win = curses.newwin(self.h, self.w, 0, 0)
        self.win.keypad(1)
        curses.curs_set(0)

        self.chars = [curses.ACS_CKBOARD, '#', '*']

        self.player1_controls = {curses.KEY_UP: 0, curses.KEY_LEFT: 0, curses.KEY_DOWN: 0, curses.KEY_RIGHT: 0}
        self.player2_controls = {ord('w'): 1, ord('a'): 1, ord('s'): 1, ord('d'): 1}
        self.player3_controls = {ord('i'): 2, ord('j'): 2, ord('k'): 2, ord('l'): 2}

    def init_grid(self):
        self.grid = []
        for x in range(self.h):
            self.grid.append([])
            for y in range(self.w):
                if x == 0 or x == self.h-1 or y == 0 or y == self.w-1:
                    self.grid[x].append(1)
                else:
                    self.grid[x].append(0)

    def init_players(self):
        self.players = []
        if(self.num_of_players == 1):
            self.players_controls.update(self.player1_controls)
        elif(self.num_of_players == 2):
            self.players_controls.update(self.player1_controls)
            self.players_controls.update(self.player2_controls)
        elif(self.num_of_players == 3):
            self.players_controls.update(self.player1_controls)
            self.players_controls.update(self.player2_controls)
            self.players_controls.update(self.player3_controls)
        for i in range(self.num_of_players):
            self.players.append(Player(self.colors[i], self.chars[i], self.w, self.h, i, self.grid))

    def play(self):
        self.win.clear()
        self.init_grid()
        self.init_players()
        for player in self.players:
            render(player, self.win, 0, self.grid)

        prev_button_direction = 1
        button_direction = 1
        key = curses.KEY_RIGHT

        counter = 0
        num_of_players_alive = self.num_of_players

        self.win.refresh()

        while True:
            self.win.timeout(100)

            counter += 1
            if(num_of_players_alive == 0):
                break

            next_key = self.win.getch()

            if next_key == -1:
                key = key
            else:
                key = next_key

            # 0-Left, 1-Right, 3-Up, 2-Down
            if key in self.players_controls.keys():
                player_index = self.players_controls[key]

                if (chr(key) == 'j' or chr(key) == 'a' or key == curses.KEY_LEFT) and self.players[player_index].prev_direction != 1:
                    self.players[player_index].direction = 0
                elif (chr(key) == 'l' or chr(key) == 'd' or key == curses.KEY_RIGHT) and self.players[player_index].prev_direction != 0:
                    self.players[player_index].direction = 1
                elif (chr(key) == 'i' or chr(key) == 'w' or key == curses.KEY_UP) and self.players[player_index].prev_direction != 2:
                    self.players[player_index].direction = 3
                elif (chr(key) == 'k' or chr(key) == 's' or key == curses.KEY_DOWN) and self.players[player_index].prev_direction != 3:
                    self.players[player_index].direction = 2

            for player in self.players:
                player.prev_direction = player.direction

                if player.direction == 0:
                    player.move_y_minus()
                elif player.direction == 1:
                    player.move_y_plus()
                elif player.direction == 3:
                    player.move_x_minus()
                elif player.direction == 2:
                    player.move_x_plus()

                if(player.check_collision() and player.is_alive):
                    player.setDead()
                    num_of_players_alive -= 1
                if player.is_alive:
                    render(player, self.win, counter, self.grid)

        self.game_over()

    def game_over(self):
        self.sc.clear()
        self.sc.addstr(round(self.h/2), round(self.w/2), "GAME OVER")
        self.sc.refresh()
        time.sleep(1)
        self.sc.clear()
