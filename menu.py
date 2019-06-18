#!/usr/bin/env python2

import curses
from curses import panel
from game import Game, Player, Position, Motorbike

COLORS =  {
            0: [0, 248, 236],
            1: [22, 20, 18],
            2: [47, 43, 23],
            3: [202, 213, 55]
            }

class TextField(object):

    def __init__(self, stdscreen):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(1)

    def display(self, string):
        self.window.clear()

        self.window.refresh()
        curses.doupdate()
        self.window.addstr(1, 1, string, curses.A_NORMAL)
        counter = 0
        while(True):
            key = self.window.getch()
            if key != curses.ERR or counter == 3000/200:
                break
            counter += 1

        self.window.clear()
        self.window.refresh()
        curses.doupdate()

class Menu(object):

    def __init__(self, items, stdscreen):
        self.window = stdscreen.subwin(0,0)
        self.window.keypad(1)
        self.panel = panel.new_panel(self.window)
        self.panel.hide()
        panel.update_panels()

        self.position = 0
        self.items = items
        self.items.append(('Exit','exit'))

    def navigate(self, n):
        self.position += n
        if self.position < 0:
            self.position = len(self.items)-1
        elif self.position >= len(self.items):
            self.position = 0

    def display(self):
        self.panel.top()
        self.panel.show()
        self.window.clear()

        while True:
            self.window.refresh()
            curses.doupdate()
            for index, item in enumerate(self.items):
                if index == self.position:
                    mode = curses.A_REVERSE
                else:
                    mode = curses.A_NORMAL

                msg = '%d. %s' % (index+1, item[0])
                self.window.addstr(1+index, 1, msg, mode)

            key = self.window.getch()

            if key in [curses.KEY_ENTER, ord('\n')]:
                if self.position == len(self.items)-1:
                    break
                else:
                    if self.items[self.position][2] != None:
                        self.items[self.position][1](self.items[self.position][2])
                    else:
                        self.items[self.position][1]()


            elif key == curses.KEY_UP:
                self.navigate(-1)

            elif key == curses.KEY_DOWN:
                self.navigate(1)

        self.window.clear()
        self.panel.hide()
        panel.update_panels()
        curses.doupdate()

class MyApp(object):

    def __init__(self, stdscreen):
        self.screen = stdscreen
        self.h, self.w = self.screen.getmaxyx()

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        curses.curs_set(0)

        ws = WelcomeScreen(stdscreen)
        ws.display()

        self.players = []
        self.num_of_players = 1
        curses.curs_set(0)

        self.textfield = TextField(self.screen)

        submenu_items = [
                ('1 player',  self.set_number_of_players, 1),
                ('2 players', self.set_number_of_players, 2),
                ('3 players', self.set_number_of_players, 3),
                ('4 players', self.set_number_of_players, 4)
                ]
        submenu = Menu(submenu_items, self.screen)
        self.game = Game(self.screen)

        main_menu_items = [
                ('Set number of players', submenu.display, None),
                ('Show score', self.game.show_score, None),
                ('Play game', self.play_game, None)
                ]
        main_menu = Menu(main_menu_items, self.screen)
        main_menu.display()

    def set_number_of_players(self, num):
        self.num_of_players = num
        self.players = []
        for i in range(num):
            self.players.append(Player(i))

        msg = 'Number of players set to %d.' % self.num_of_players
        self.textfield.display(msg)

    def play_game(self):
        if self.players == []:
            self.set_number_of_players(self.num_of_players)
        self.display_controls_all()
        self.game.play(self.players)

    def display_controls_all(self):
        self.screen.clear()
        self.screen.refresh()
        for i, player in enumerate(self.players):
            self.display_controls(player.get_controls(), i, COLORS[i][0])
        counter = 0
        while(True):
            key = self.screen.getch()
            if key != curses.ERR or counter == 3000/200:
                break
            counter += 1

        self.screen.clear()
        self.screen.refresh()

    def display_controls(self, controls, index, color):
        if index == 0:
            self.screen.addstr(3, 3, controls[0], curses.color_pair(color))
            self.screen.addstr(3, 9, controls[1], curses.color_pair(color))
            self.screen.addstr(2, 6, controls[2], curses.color_pair(color))
            self.screen.addstr(3, 6, controls[3], curses.color_pair(color))
        elif index == 1:
            self.screen.addstr(3, 15, controls[0], curses.color_pair(color))
            self.screen.addstr(3, 21, controls[1], curses.color_pair(color))
            self.screen.addstr(2, 18, controls[2], curses.color_pair(color))
            self.screen.addstr(3, 18, controls[3], curses.color_pair(color))
        elif index == 2:
            self.screen.addstr(12, 3, controls[0], curses.color_pair(color))
            self.screen.addstr(12, 9, controls[1], curses.color_pair(color))
            self.screen.addstr(11, 6, controls[2], curses.color_pair(color))
            self.screen.addstr(12, 6, controls[3], curses.color_pair(color))
        elif index == 3:
            self.screen.addstr(12, 15, controls[0], curses.color_pair(color))
            self.screen.addstr(12, 21, controls[1], curses.color_pair(color))
            self.screen.addstr(11, 18, controls[2], curses.color_pair(color))
            self.screen.addstr(12, 18, controls[3], curses.color_pair(color))
        self.screen.refresh()

class WelcomeScreen(object):
    def __init__(self, stdscreen):
        self.screen = stdscreen

        self.h, self.w = self.screen.getmaxyx()
        self.screen.clear()
        self.screen.refresh()

        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)
        curses.curs_set(0)
        self.welcomeText = open('res/welcome.txt', 'r').read()

        self.welcome_h = len(self.welcomeText.splitlines())
        self.welcome_w = len(max(self.welcomeText.splitlines(), key=len))

        self.welcome_x = round((self.w / 2 - self.welcome_w / 2))
        self.welcome_y = round((self.h / 2 - self.welcome_h / 2))

        center_x_left = round((self.w - self.welcome_w)/4)
        center_x_right = self.w - center_x_left
        center_y_top = round((self.h - self.welcome_h)/4)
        center_y_bot = self.h - center_y_top
        positions = []
        positions.append(Position(center_y_top, round(self.w/2), []))
        positions.append(Position(center_y_bot, round(self.w/2), []))
        positions.append(Position(round(self.h/2), center_x_left, []))
        positions.append(Position(round(self.h/2), center_x_right, []))

        self.pos_right_bot = Position(center_y_bot, center_x_right, [])

        self.pos_left_top = Position(center_y_top, center_x_left, [])
        self.pos_right_top = Position(center_y_top, center_x_right, [])
        self.pos_left_bot = Position(center_y_bot, center_x_left, [])

        self.bikes = []
        for i, pos in enumerate(positions):
            self.bikes.append(Motorbike(i, curses.ACS_CKBOARD, [], position = pos, direction = i))


    def display(self):
        for y, line in enumerate(self.welcomeText.splitlines()):
            self.screen.addstr(y+self.welcome_y, self.welcome_x, line)
        curses.halfdelay(1)
        curses.noecho()
        while(True):
            self.screen.timeout(100)
            for bike in self.bikes:
                bike.render(self.screen, 0, [])
                if bike.direction == 0:
                    bike.move_col_left()
                elif bike.direction == 1:
                    bike.move_col_right()
                elif bike.direction == 3:
                    bike.move_row_up()
                elif bike.direction == 2:
                    bike.move_row_down()

                if(bike.position == self.pos_left_top):#change direction to down
                    bike.direction = 2
                elif(bike.position == self.pos_right_top):#change direction to left
                    bike.direction = 0
                elif(bike.position == self.pos_right_bot):#change direction to up
                    bike.direction = 3
                elif(bike.position == self.pos_left_bot):#change direction to right
                    bike.direction = 1
            key = self.screen.getch()
            if(key != curses.ERR):
                break

        self.screen.clear()
        self.screen.refresh()

if __name__ == '__main__':
    curses.wrapper(MyApp)
