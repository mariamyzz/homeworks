# -*- coding: utf-8 -*-

from models import *

def game_init():
    """creates players and their ships"""
    typewriter_effect('Hi!\n')
    typewriter_effect('Welcome to the Russian version of the Battleship game.\n')
    sleep(0.5)
    
    typewriter_effect('Please enter the name of the first player: ')
    player1 = Player(input())
    typewriter_effect("Perfect! " + player1.name + ", let's have your ships arranged.\n")
    player1.arrange_home_ships()
    
    typewriter_effect('Please enter the name of the second player: ')
    player2 = Player(input())
    typewriter_effect("Perfect! " + player2.name + ", let's have your ships arranged.\n")
    player2.arrange_home_ships()
    
    typewriter_effect("Let's get started.\n")
    sleep(1)
    print("\033c")

    return player1, player2


def make_a_shot(assailant, opponent: Player):
    """returns True if hit"""
    print("\033c")
    typewriter_effect(assailant.name + ", this is your foe's grid.\n")
    sleep(0.5)
    assailant.foegrid.print()
    typewriter_effect('Choose a square to shoot: ')

    shot_square_index = opponent.homegrid.get_index(input())

    while shot_square_index not in range(101) or opponent.homegrid[shot_square_index] == OFF:
        shot_square_index = opponent.homegrid.get_index(input\
            ('Please enter a valid index, and don\'t repeat yourself: '))

    if opponent.homegrid[shot_square_index] == DECK:
        typewriter_effect('Hit!')
        if opponent.is_sunk(shot_square_index):
            typewriter_effect('\nYou have just sunk the whole ship. ')
            sleep(0.7)
            
            for ship_deck in opponent.find_ship(shot_square_index):
                for offset in Grid.offset_values(ship_deck):
                    if opponent.homegrid[shot_square_index + offset] != HIT:
                        try:
                            opponent.homegrid[shot_square_index + offset] = OFF
                            assailant.foegrid[shot_square_index + offset] = OFF
                        except IndexError:
                            continue


        typewriter_effect('\nYou make one more shot.')
        assailant.foegrid[shot_square_index] = HIT
        opponent.homegrid[shot_square_index] = HIT
        
        return True

    else: 
        typewriter_effect('Miss. Now {}\'s turn.'.format(opponent.name))
        assailant.foegrid[shot_square_index] = OFF
        opponent.homegrid[shot_square_index] = OFF

        return False


def shooting_turns(player1, player2): 
    """invokes 'make_a_shot' function in turns for each"""
    while (player1.homegrid.count(HIT) != 20) or (player2.homegrid.count(HIT) != 20):
        while make_a_shot(player1, player2):
            continue
        while make_a_shot(player2, player1):
            continue
    
    if player1.homegrid.count(HIT) == 20:
        typewriter_effect(player2.name + 'won!')
    else:
        typewriter_effect(player1.name + 'won!')


def main():
    player1, player2 = game_init()
    shooting_turns(player1, player2)


if __name__ == '__main__':
    try: 
        main()
    except KeyboardInterrupt:
        typewriter_effect('\nSee you next time!')
