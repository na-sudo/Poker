

import numpy as np


class Poker():
    def __init__(self):
        self.hand = np.zeros((4,13), dtype=int)
        self.board = np.zeros((4,13), dtype=int)
        self.RANK_INT = list(range(9))
        self.RANK_TEXT = [
            'high card', 'a pair', 'two pair', 'three of a kind', 'straight',
            'flush', 'full house', 'quads', 'straight flush']
        self.SUIT = ['c', 'd', 'h', 's']
        self.NUMBER = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J',
                       'Q', 'K', 'A']

    def str2arr(self, cards):
        arr = np.zeros((4,13), dtype=int)
        for i in range(0, len(cards), 2):
            s = self.SUIT.index(cards[i+1])
            n = self.NUMBER.index(cards[i])
            arr[s, n] = 1
        return arr

    def set_hand(self, cards :str):
        self.hand = self.str2arr(cards)

    def set_board(self, cards :str):
        self.board = self.str2arr(cards)

    def handrank(self, hand='hand string'):
        if hand == 'hand string':
            hand = self.hand
        else:
            pass
        res = [0, 0]
        total = hand + self.board

        total_num = np.sum(total, axis=0)
        if np.max(total_num, axis=0) == 4:
            buffer1 = np.where(total_num == 4)[0][-1]
            buffer2 = np.where(total_num != 4)[0][-1]
            res = [7, buffer1*100 + buffer2]
        elif np.max(total_num, axis=0) == 3:
            buffer1 = np.where(total_num == 3)[0][-1]
            buffer2 = np.where(total_num >= 2)
            if len(buffer2) >= 2:
                buffer2.remove(buffer1)
                buffer3 = buffer2[-1]
                res = [6, ibuffer1*100 + buffer3]
            else:
                buffer3 = sum(np.where(total_num == 1)[0][-2:])
                res = [3, buffer1*100 + buffer3]
        elif np.max(total_num, axis=0) == 2:
            buffer1 = np.where(total_num == 2)[0]
            buffer2 = np.where(total_num >= 1)[0]
            if len(buffer1) >= 2:
                for i in buffer1[-2:]:
                    buffer2.remove(i)
                res = [2, sum(buffer1[-2:])*100 + buffer2[-1]]
            else:
                buffer2.remove(buffer1[-1])
                res = [1, buffer1[0]*100 + sum(buffer2[-3:])]
        else:
            buffer1 = np.where(total_num == 1)[0]
            res = [0, sum(buffer1[-3:])]

        total_suit = np.sum(total, axis=1)
        if res[0]<=3:
            if np.max(total_suit, axis=0) >= 5:
                flush = total[total_suit == np.max(total_suit, axis=0)]
                res = [5, sum(flush[-5:])]
                buffer1 = flush
            else:
                buffer1 = np.array(np.where(total_num > 0, 1, 0))
            buffer1 = np.concatenate([buffer1, buffer1], 0)[:14]
            buffer1 = buffer1[::-1]
            for i in range(len(buffer1)-4):
                if np.sum(buffer1[i:i+5]) == 5:
                    if res[0]==5:
                        res = [8, 14-i]
                    else:
                        res = [4, 14-i]
                    break
        return res


if __name__ == '__main__':
    po = Poker()
    po.set_hand(input('hand(ex: AdKh): '))
    po.set_board(input('board(ex: QhJhTh4c8s): '))
    result = po.handrank()
    print(po.RANK_TEXT[result[0]], result)
