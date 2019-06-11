#!/usr/bin/env python2

import curses
from curses import panel
from Game import Game, Player

class TextField(object):

        def __init__(self, stdscreen):
            self.window = stdscreen.subwin(0,0)
            self.window.keypad(1)

        def display(self, string):
            self.window.clear()

            self.window.refresh()
            curses.doupdate()
            self.window.addstr(1, 1, string, curses.A_NORMAL)
            self.window.getch()

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
        self.game.play(self.players)

if __name__ == '__main__':
    curses.wrapper(MyApp)
