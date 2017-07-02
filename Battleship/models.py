# -*- coding: utf-8 -*-

from time import sleep
import sys

from constants import *


def typewriter(line):
    for letter in line:
        print(letter, end='')
        sys.stdout.flush()
        sleep(0.03)


class Grid(list):

    def print(self):
        """prints the grid prettily, returns None"""
        row_separator = '  +---+---+---+---+---+---+---+---+---+---+'
        print('    a   b   c   d   e   f   g   h   i   j  ')
        for row in range(1, 11):
            print(row_separator)
            piped_line = ' | '.join(self[row * 10 - 10:row * 10])
            print('{:2}{}{}{}'.format(str(row), '| ', piped_line, ' |'))
        print(row_separator)

    @staticmethod
    def get_index(square):
        """
        Turns string index like 'a1' to numeric index like 0.
        Args: square: a string like 'a1'
        returns: int, if string was a valid index
        """
        list_of_indeces = []
        for row in range(1, 11):
            for letter in list(map(chr, range(97, 107))):
                list_of_indeces.append(letter + str(row))
        if square.lower() in list_of_indeces:
            return list_of_indeces.index(square)

    @staticmethod
    def check_index(square):
        """
        Uses the get_index function to see 
        if there is such a square on the grid.
        Prompts a user to input correct coordinates, if there is not.
        Returns: square index (int)
        """
        while Grid.get_index(square) not in range(101):
                square = input('Enter a valid square coordinates, like a1 or j10: ')
        return Grid.get_index(square)

    @staticmethod
    def offset_values(deck):
        offset_list = [-1, 1, 10, -10, 11, -11, 9, -9]

        if deck // 10 == 0 and deck % 10 == 0:
            offset_list = [1, 10, 11]
        
        elif deck // 10 == 9 and deck % 10 == 0:
            offset_list = [1, -10, -9]

        elif deck // 10 == 0 and deck % 10 == 9:
            offset_list = [-1, 9, 10]
            
        elif deck // 10 == 9 and deck % 10 == 9:
            offset_list = [-1, -10, -11] 

        elif deck // 10 == 0:
            offset_list = [1, -1, 9, 10, 11]

        elif deck // 10 == 9:
            offset_list = [1, -1, -9, -10, -11]

        elif deck % 10 == 0:
            offset_list = [1, 10, -10, 11, -9]
        
        elif deck % 10 == 9:
            offset_list = [-1, 10, -10, -11, 9]

        

        return offset_list


class Player(Grid):
    def __init__(self, name):
        self.name = name
        self.homegrid = Grid(' ' * 100)
        self.foegrid = Grid(' ' * 100)
        self.ships = {
                      "four-decker": [[]],
                      "three-decker": [[], []],
                      "two-decker": [[], [], []],
                      "single-decker": [[], [], [], []],
                      }

    def arrange_home_ships(self):
        """
        return: None, runs a loop to get the indeces for all the ships,
        and places DECK on the grids to display them
        """

        typewriter('This is your home grid.\n')
        sleep(0.7)
        self.homegrid.print()
        sleep(0.7)
        typewriter('Now please arrange your ships on the grid, one by one.\n')
        sleep(0.7)

        for ship_type, (decks_number, ships_number) in SHIPS_DETAILS.items():
            for i in range(ships_number):
                print('Please arrange your {}. It is the {} one from {} in total.'.\
                      format(ship_type, NUMERIC[i], ships_number))
                for deck in range(decks_number):
                    square_index = self.new_valid_deck_index(self.ships[ship_type][i])

                    self.ships[ship_type][i].append(square_index)
                    self.homegrid[square_index] = DECK
                    self.homegrid.print()

        typewriter('Perfect. You are all set.\n')

    def is_square_empty(self, square_index):
        """True, if empty, False, if not"""
        if self.homegrid[square_index] == DECK:
            return False
        else:
            return True

    def is_sunk(self, square_index):
        ship = self.find_ship(square_index)

        for deck in ship:
            if self.homegrid[deck] != HIT:
                return False
        return True

    def find_ship(self, square_index):
        for ship_type, ships in self.ships.items():
            for ship in ships:
                if square_index in ship:
                    return ship

    def is_deck_settable(self, current_ship: list, square_index: int):
        for ship_type, ships in self.ships.items():
            for ship in ships:
                if ship != [] and ship != current_ship:
                    environs = []
                    for deck in ship:
                        for offset in Grid.offset_values(deck):
                            environs.append(deck + offset)
                    if square_index in ship or square_index in environs:
                        return False

        return True

    def is_deck_appendable(self, ship: list, deck: int):
        if len(ship) == 0:
            return True

        elif len(ship) == 1:
            if (deck % 10 == ship[0] % 10) and (abs(deck - ship[0]) == 10):
                return True
            elif (deck // 10 == ship[0] // 10) and (abs(deck - ship[0]) == 1):
                return True
            else:
                return False

        else:
            if ship[0] % 10 == ship[-1] % 10 == deck % 10:
                if abs(deck - ship[0]) == 10 or abs(deck - ship[-1]) == 10:
                    return True
            elif ship[0] // 10 == ship[-1] // 10 == deck // 10:
                if abs(deck - ship[0]) == 1 or abs(deck - ship[-1]) == 1:
                    return True
            else:
                return False

    def new_valid_deck_index(self, ship):
        square_index = Grid.check_index(input('Add a deck to the next square: '))

        while not self.is_square_empty(square_index) or \
              not self.is_deck_settable(ship, square_index) or \
              not self.is_deck_appendable(ship, square_index):

            if not self.is_square_empty(square_index):
                print('You already have a ship deck there.')
            
            elif not self.is_deck_appendable(ship, square_index):
                print('Ship decks must go in line.')

            elif not self.is_deck_settable(ship, square_index):
                print('Ships cannot touch each other.')

            square_index = Grid.check_index(input('Choose a square: '))

        return square_index
