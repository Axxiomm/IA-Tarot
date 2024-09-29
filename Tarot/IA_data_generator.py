import utils
import random
import tkinter as tk
from PIL import Image, ImageTk
import os
import csv

COLOR_MAP = {2: 'PIQUE', 4: 'TREFLE', 1: 'COEUR', 3: 'CARREAU', 0: 'ATOUT'}

BID_SPACE = {0: 'PASSE', 1: 'PETITE', 2: 'GARDE', 3: 'GARDE_SANS', 4: 'GARDE_CONTRE'}


class MainWindow:  #Creation de la fenetre principale
    def __init__(self, master):

        self.master = master
        self.frame = tk.Frame(self.master)

        self.cardFrame = tk.Frame(self.frame)

        self.chooseDog = [(-1, -1)]*3
        self.chooseKing = ''
        self.chooseContract = ''
        self.hand = []
        self.dog = []

        self._cardCounter = 0

        self.cardButton = [tk.Button()] * 18
        self.cardButtonTuple = [(0, 0)] * 18

        for i in range(18):
            self.cardButton[i] = tk.Button(self.cardFrame, text='CARD', width=7, height=6, command=lambda m=i: self.clicked_card(m))
            self.cardButton[i].grid(row=0, column=i, padx=9, pady=9)

        self.contractButton = [tk.Button()]*5

        self.chooseFrame = tk.Frame(self.frame)

        for i in range(5):
            self.contractButton[i] = tk.Button(self.chooseFrame, text=BID_SPACE[i], width=15, height=3, command=lambda m=i: self.clicked_contract(m))
            self.contractButton[i].grid(row=0, column=i, padx=9, pady=9)

        self.kingButton = [tk.Button()]*4

        for i in range(4):
            self.kingButton[i] = tk.Button(self.chooseFrame, text=COLOR_MAP[i+1], width=15, height=3, command=lambda m=i: self.clicked_king(m))
            self.kingButton[i].grid(row=1, column=i, padx=9, pady=9)

        self.chooseFrame.grid(row=1, column=0)
        self.cardFrame.grid(row=0, column=0)

        generate = tk.Button(self.frame, text='valider', command=self.write_choose)
        generate.grid(row=2, column=0)

        self.frame.pack()

    def clicked_card(self, i):
        self.chooseDog[self._cardCounter % 3] = self.cardButtonTuple[i]
        self._cardCounter += 1

        self.print_choose()

    def clicked_contract(self, i):
        self.chooseContract = self.contractButton[i]['text']

        self.print_choose()

    def clicked_king(self, i):
        self.chooseKing = self.kingButton[i]['text']

        self.print_choose()

    def run(self):
        cards = utils.card_list()
        random.shuffle(cards)

        self.chooseDog = [(-1, -1)] * 3
        self.chooseKing = ''
        self.chooseContract = ''

        self.hand, self.dog = cards[0:15], cards[15:18]

        fullSortedHand = utils.sort_hand(self.hand+self.dog)

        for i, card in enumerate(fullSortedHand):
            cardpng = ImageTk.PhotoImage(Image.open(resource_path("card_png\\"+utils.card_to_png_path(card))).resize((33, 60)))

            self.cardButton[i].config(image=cardpng,
                                      width=35, height=63)
            self.cardButton[i].image = cardpng

            self.cardButtonTuple[i] = card
            if card in self.dog:
                self.cardButton[i].config(background='red')
            else:
                self.cardButton[i].config(background='white')

    def write_choose(self):
        with open(resource_path('data.csv'), 'a', newline='') as file:
            writer = csv.writer(file)

            king = {v: k for k, v in COLOR_MAP.items()}[self.chooseKing]
            bid = {v: k for k, v in BID_SPACE.items()}[self.chooseContract]

            handInt = [str(utils.card_to_int(card)) for card in self.hand]
            dogInt = [str(utils.card_to_int(card)) for card in self.dog]
            chooseDogInt = [str(utils.card_to_int(card)) for card in self.chooseDog]

            writer.writerow([handInt, dogInt, chooseDogInt, str(king), str(bid)])

            print('ok')

            self.run()

    def print_choose(self):
        print(self.chooseDog)
        print(self.chooseContract)
        print(self.chooseKing)


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == '__main__':



    root = tk.Tk()
    app = MainWindow(root)
    root.title("IA TAROT")

    app.run()

    root.mainloop()

