

import numpy as np
import pandas as pd

from poker import Poker

pair = np.eye(13, dtype=bool)
#print(pair)
suit = ~np.tri(13, dtype=bool)
#print(suit)
offsuit = np.tri(13, dtype=bool) ^ np.eye(13, dtype=bool)
#print(offsuit)

probability = pair * 0.453 + suit * 0.302 + offsuit * 0.905


BTNopen = np.array(
    ([9,9,3,3,3,3,2,2,2,3,3,2,4],
     [9,9,3,3,3,2,2,2,2,2,2,4,4],
     [3,3,9,3,3,2,2,2,2,0,0,0,0],
     [3,2,2,3,3,3,2,2,0,0,0,0,0],
     [4,2,2,2,3,3,2,2,0,0,0,0,0],
     [2,2,0,2,2,3,2,2,0,0,0,0,0],
     [2,0,0,0,0,0,3,2,2,0,0,0,0],
     [2,0,0,0,0,0,0,3,2,2,0,0,0],
     [2,0,0,0,0,0,0,0,3,3,2,0,0],
     [2,0,0,0,0,0,0,0,0,3,3,0,0],
     [2,0,0,0,0,0,0,0,0,0,3,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,3,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,3],)
     , dtype=int)

#print(BTNopen)

BBvsBTN = np.array(
    ([4,9,4,4,3,3,2,2,2,3,3,3,3],
     [9,9,4,3,3,2,2,2,2,2,2,2,2],
     [3,3,9,4,3,2,2,0,0,0,0,0,0],
     [3,2,2,9,3,2,2,0,0,0,0,0,0],
     [2,2,2,2,4,2,2,2,0,0,0,0,0],
     [2,0,0,0,0,4,2,2,0,0,0,0,0],
     [2,0,0,0,0,0,2,2,2,0,0,0,0],
     [0,0,0,0,0,0,0,2,2,2,0,0,0],
     [0,0,0,0,0,0,0,0,2,2,2,0,0],
     [0,0,0,0,0,0,0,0,0,2,2,0,0],
     [0,0,0,0,0,0,0,0,0,0,2,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,2,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,2],)
     , dtype=int)


def main():
    po = Poker()

    hero_pos = input('HERO (BTN or BB):')
    if hero_pos == 'BTN' or hero_pos == 'btn':
        hero_pos = 'BTN'
        villan_pos = 'BB'

    else:
        hero_pos = 'BB'
        villan_pos = 'BTN'

    act_str = input('BB 3bet or call :')
    if act_str == '3bet' or act_str == '3':
        act = 3
        if hero_pos == 'BTN':
            hero = np.where(BTNopen==3, 1, 0)
            villan = np.where(BBvsBTN>=3, 1, 0)
        else:
            villan = np.where(BTNopen==3, 1, 0)
            hero = np.where(BBvsBTN>=3, 1, 0)
    else:
        act = 2
        if hero == 'BTN':
            hero = np.where(BTNopen>=2, 1, 0)
            villan = np.where(BBvsBTN==2, 1, 0)
        else:
            hero = np.where(BTNopen>=2, 1, 0)
            villan = np.where(BBvsBTN==2, 1, 0)

    print('hero')
    print(hero)
    print('villan')
    print(villan)
    hero_prb = po.set_player(hero)
    villan_prb = po.set_player(villan)

    po.set_board(input('flop board(ex: QhJhTh): '))
    hero_df = po.create_df(hero_prb)
    villan_df = po.create_df(villan_prb)
    print('hero_df', hero_pos)
    print(hero_df)
    print('villan_df', villan_pos)
    print(villan_df)



if __name__ == '__main__':
    main()