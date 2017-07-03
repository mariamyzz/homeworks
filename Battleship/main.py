# -*- coding: utf-8 -*-

from models import *


def game_init():
    """creates players and their ships"""
    
    def create_player(turn):
        print("\033c")
        typewriter(('Please enter the name of the {} player: ').format(NUMERIC[turn]))
        player = Player(input())
        typewriter("Perfect! " + player.name + ", let's have your ships arranged.\n")
        player.arrange_home_ships()

        return player

    typewriter('Hi!\n')
    typewriter('Welcome to the Russian version of the Battleship game.\n')
    sleep(0.5)

    player1, player2 = create_player(0), create_player(1)

    typewriter("Let's get started.\n")
    sleep(1.0)
    print("\033c")

    return player1, player2


def make_a_shot(assailant, opponent: Player):
    """returns True if hit"""
    print("\033c")
    typewriter(assailant.name + ", this is your foe's grid.\n")
    sleep(0.5)
    assailant.foegrid.print()
    typewriter('Choose a square to shoot: ')

    shot_square_index = opponent.homegrid.check_index(input())

    while opponent.homegrid[shot_square_index] == OFF or \
          opponent.homegrid[shot_square_index] == HIT:
        print('You already made this shot.')
        shot_square_index = opponent.homegrid.check_index(input('Try another square: '))

    if opponent.homegrid[shot_square_index] == DECK:
        assailant.foegrid[shot_square_index] = HIT
        opponent.homegrid[shot_square_index] = HIT
        typewriter('Hit!')

        if opponent.is_sunk(shot_square_index):
            typewriter('\nYou have just sunk the whole ship. ')
            sleep(0.7)

            for ship_deck in opponent.find_ship(shot_square_index):
                for offset in Grid.offset_values(ship_deck):
                    if ship_deck + offset not in opponent.find_ship(shot_square_index):
                        opponent.homegrid[ship_deck + offset] = OFF
                        assailant.foegrid[ship_deck + offset] = OFF

        typewriter('\nYou make one more shot.')
        sleep(0.5)

        return True

    else:
        assailant.foegrid[shot_square_index] = OFF
        opponent.homegrid[shot_square_index] = OFF
        typewriter('Miss. Now {}\'s turn.'.format(opponent.name))
        sleep(0.7)

        return False


def shooting_turns(player1, player2):
    """invokes 'make_a_shot' function in turns for each"""
    while (player1.homegrid.count(HIT) != 20) or (player2.homegrid.count(HIT) != 20):
        while make_a_shot(player1, player2):
            continue
        while make_a_shot(player2, player1):
            continue

    if player1.homegrid.count(HIT) == 20:
        typewriter(player2.name + 'won!')
    else:
        typewriter(player1.name + 'won!')


def main():
    player1, player2 = game_init()
    shooting_turns(player1, player2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        typewriter('\nSee you next time!')
