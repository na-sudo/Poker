

import numpy as np
import pandas as pd



suit = np.zeros((13,13),dtype=int)
for i in range(13):
    for j in range(13):
        if i<j:
            suit[i,j] = 1

offsuit = np.zeros((13,13),dtype=int)
for i in range(13):
    for j in range(13):
        if i>j:
            offsuit[i,j] = 1

pair = np.zeros((13,13),dtype=int)
for i in range(13):
    for j in range(13):
        if i==j:
            pair[i,j] = 1

probability = np.zeros((13,13), dtype=np.float)
print(probability)
for i in range(13):
    for j in range(13):
        if i==j:
            probability[i,j] = 0.453
        elif i<j:
            probability[i,j] = 0.302
        elif i>j:
            probability[i,j] = 0.905


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


'''
BTNopen = np.array(
    ([0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0,0,0,0,0,0],)
     , dtype=int)
'''




def main():
    print('BTNopen')
    act_str = input('BB 3bet or call :')
    if act_str == '3bet' or act_str == '3':
        act = 3
        a = np.where(BTNopen==3, 1, 0)
        b = np.where(BBvsBTN>=3, 1, 0)
    else:
        act = 2
        a = np.where(BTNopen>=2, 1, 0)
        b = np.where(BBvsBTN==2, 1, 0)
    print('BTN')
    print(a)
    print('BB')
    print(b)
    a_prb = a*probability
    b_prb = b*probability

    li = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    '''
    # don't use pandas for print.
    print('   BTN  BB')
    for i in range(13):
        print(
            '{} :{:3} {:3}'.format(
                li[i],
                np.round(np.sum(a_prb, axis=0)[i] + np.sum(a_prb, axis=1)[i] - np.diag(a_prb)[i], 2),
                np.round(np.sum(b_prb, axis=0)[i] + np.sum(b_prb, axis=1)[i] - np.diag(b_prb)[i], 2)
            ),
        )
    '''
    # use pandas for print.
    a_hit = np.sum(a_prb, axis=0) + np.sum(a_prb, axis=1) - np.diag(a_prb)
    b_hit = np.sum(b_prb, axis=0) + np.sum(b_prb, axis=1) - np.diag(b_prb)
    df = pd.DataFrame({'BTN':a_hit, 'BB':b_hit}, index=li)
    print(df)




if __name__ == '__main__':
    main()