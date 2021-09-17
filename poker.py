

import numpy as np
import pandas as pd

class Poker():
    def __init__(self):
        self.hand = np.zeros((4,13), dtype=int)
        self.board = np.zeros((4,13), dtype=int)
        self.RANK_INT = list(range(9))
        self.RANK_TEXT = [
            'high card', 'a pair', 'two pair', 'three of a kind', 'straight',
            'flush', 'full house', 'quads', 'straight flush']
        self.SUIT = ['c', 'd', 'h', 's']
        self.NUMBER = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']

        self.RANGE_PAIR = np.eye(13, dtype=bool)
        self.RANGE_SUIT = ~np.tri(13, dtype=bool)
        self.RANGE_OFFSUIT = np.tri(13, dtype=bool) ^ np.eye(13, dtype=bool)
        self.PROB = self.RANGE_PAIR * 0.453 + self.RANGE_SUIT * 0.302 + self.RANGE_OFFSUIT * 0.905

    def str2arr(self, cards):
        arr = np.zeros((4,13), dtype=int)
        for i in range(0, len(cards), 2):
            s = self.SUIT.index(cards[i+1].lower())
            n = self.NUMBER.index(cards[i].upper())
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
        print('total')
        print(total)

        total_num = np.sum(total, axis=0)
        if np.max(total_num, axis=0) == 4:
            buffer1 = np.where(total_num == 4)[0][0]
            buffer2 = np.where(total_num >= 1)[0].tolist()
            buffer2.remove(buffer1)
            res = [7, (13 - buffer1)*100 + 13 - buffer2[0]]
        elif np.max(total_num, axis=0) == 3:
            buffer1 = np.where(total_num == 3)[0][0]
            buffer2 = np.where(total_num >= 2)[0].tolist()
            if len(buffer2) >= 2:
                buffer2.remove(buffer1)
                res = [6, (13 - buffer1)*100 + 13 - buffer2[0]]
            else:
                buffer3 = sum(np.where(total_num == 1)[0][:2])
                res = [3, (13 - buffer1)*100 + 13*2 - buffer3]
        elif np.max(total_num, axis=0) == 2:
            buffer1 = np.where(total_num == 2)[0]
            buffer2 = np.where(total_num >= 1)[0].tolist()
            if len(buffer1) >= 2:
                for i in buffer1[:2]:
                    buffer2.remove(i)
                res = [2, (13*2 - sum(buffer1[:2]))*100 + 13 - buffer2[0]]
            else:
                buffer2.remove(buffer1[0])
                res = [1, buffer1[0]*100 + 13*3 - sum(buffer2[:3])]
        else:
            buffer1 = np.where(total_num == 1)[0]
            res = [0, 13*5 - sum(buffer1[:5])]

        total_suit = np.sum(total, axis=1)
        if res[0]<=3:
            if np.max(total_suit, axis=0) >= 5:
                flush = total[total_suit == np.max(total_suit, axis=0)][0]
                flush = np.where(flush == 1)[0]
                res = [5, 13*5 - sum(flush[:5])]
                buffer1 = total[total_suit == np.max(total_suit, axis=0)][0]
                print(buffer1)
            else:
                buffer1 = np.array(np.where(total_num > 0, 1, 0))
                print(buffer1)
            buffer1 = np.concatenate([buffer1, buffer1], 0)[:14]
            buffer1 = buffer1
            for i in range(len(buffer1)-4):
                if np.sum(buffer1[i:i+5]) == 5:
                    if res[0]==5:
                        res = [8, 13-i]
                    else:
                        res = [4, 13-i]
                    break
        return res

    def set_player(self, arr):
        return arr * self.PROB

    def create_df(self, prb):
        hit = np.sum(prb*(~self.RANGE_PAIR), axis=0) + np.sum(prb*(~self.RANGE_PAIR), axis=1)
        df = pd.DataFrame({'hit or pair':hit}, index=self.NUMBER)
        board_sum = np.sum(self.board, axis=0)
        single = np.sum(prb*(~self.RANGE_PAIR), axis=0) + np.sum(prb*(~self.RANGE_PAIR), axis=1)
        df['quads'] = np.diag(prb) * np.where(board_sum==2, 1, 0) + single * np.where(board_sum==3, 1, 0)
        # print('pair', np.diag(prb) * np.where(board_sum==2, 1, 0))
        df['3 of a kind'] = np.diag(prb) * np.where(board_sum==1, 1, 0) + single * np.where(board_sum==2, 1, 0)
        # print('3:', np.diag(prb) * np.where(board_sum==1, 1, 0))
        return df


if __name__ == '__main__':
    po = Poker()
    po.set_hand(input('hand(ex: AdKh): '))
    po.set_board(input('board(ex: QhJhTh4c8s): '))
    result = po.handrank()
    print(po.RANK_TEXT[result[0]], result)
