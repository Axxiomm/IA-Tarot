COLOR_MAP = {2: 'PIQUE', 4: 'TREFLE', 1: 'COEUR', 3: 'CARREAU', 0: 'ATOUT'}

BID_SPACE = {0: 'PASSE', 1: 'PETITE', 2: 'GARDE', 3: 'GARDE_SANS', 4: 'GARDE_CONTRE'}


def card_list() -> list:
    cardList = [(i, j) for i in range(1, 15) for j in range(1,5)]
    cardList += [(i, 0) for i in range(22)]
    return cardList


def card_to_str(card: tuple) -> str:
    value, color = card
    if color != 0 and value > 14:
        return "INVALID_CARD"
    elif color == 0:
        if value != 0:
            return str(value) + " " + COLOR_MAP[color]
        else:
            return "Excuse"
    else:
        if value == 11: tete = 'Valet'
        elif value == 12: tete = 'Cavalier'
        elif value == 13: tete = 'Dame'
        elif value == 14: tete = 'Roi'
        else: tete = str(value)

        return tete + " " + COLOR_MAP[color]


def card_to_int(card: tuple) -> int:
    # couleur * 14 + carte
    return card[0] if card[1] == 0 else 21+14*(card[1]-1)+card[0]


def card_to_png_path(card: tuple) -> str:
    name = ''

    if card[1] == 0:
        name = str(card[0] + 55)
    elif card[1] == 4:
        name = str(card[0] - 1)
    elif card[1] == 2:
        name = str(card[0] + 13)
    elif card[1] == 1:
        name = str(card[0] + 27)
    elif card[1] == 3:
        name = str(card[0] + 41)

    if card == (0,0):
        name = '77'

    if len(name) == 1:
        name = '0'+name

    return name + '.png'




def print_prise(prise: int) -> str:
    return BID_SPACE[prise]


def who_can_call(hand: list) -> list:
    listCard = hand[:]
    listCallable = [(14, 1), (14, 2), (14, 3), (14, 4)]

    if listCard.count(14) == 4:
        listCallable += [(13, 1), (13, 2), (13, 3), (13, 4)]
        if listCard.count(13) == 4:
            listCallable += [(12, 1), (12, 2), (12, 3), (12, 4)]
            if listCard.count(12) == 4:
                listCallable += [(11, 1), (11, 2), (11, 3), (11, 4)]

    return listCallable


def removable_cards(hand: list, dog: list) -> list:
    listCard = [card for card in hand if card[1] != 0 and card[0] != 14]

    return listCard if len(listCard) >= 3 else hand


def legal_move(fold: list, _hand: list, restrictedColor = None) -> list:
    hand = _hand[:]

    if restrictedColor is not None:
        hand = [e for e in hand if e[1] != restrictedColor and e[0] != 14]

    if not fold or (fold[0] == (0, 0) and len(fold) == 1):
        return hand

    firstCardColor = fold[0][1]
    if fold[0] == (0, 0):
        firstCardColor = fold[1][1]

    legal = []

    if firstCardColor == 0:
        for card in hand:
            if card[1] == 0 and card[0] > fold[analyse_fold(fold)[0]][0]:
                legal.append(card)

    else:
        for card in hand:
            if card[1] == firstCardColor:
                legal.append(card)

    if legal:
        return legal + [(0, 0)] if (0, 0) in hand else legal
    else:
        for card in hand:
            if card[1] == 0 and card[0] > fold[analyse_fold(fold)[0]][0]:
                legal.append(card)

    if legal:
        return legal + [(0,0)] if (0,0) in hand else legal
    else:
        for card in hand:
            if card[1] == 0:
                legal.append(card)

    return legal if legal else hand


def analyse_fold(foldorigin: list, petitImmprenable: bool = False) -> tuple:
    fold = foldorigin[:]

    firstCardColor = fold[0][1]

    score = 0
    for card in fold:
        score += card_value(card)
    if (1, 0) in fold and petitImmprenable:
        score -= 4.5

    for i, card in enumerate(fold):

        if card[1] != firstCardColor and card != (0, 0):
            fold[i] = (-1, card[1])
        if card[1] == 0 and card != (0, 0):
            fold[i] = (card[0] + 100, card[1])

    return fold.index(max(fold, key=lambda tup: tup[0])), score


def card_value(card):
    if card[1] == 0:
        return 4.5 if card[0] == 1 or card[0] == 21 else 0.5
    else:
        if card[0] <= 10: return 0.5
        elif card[0] == 11: return 1.5
        elif card[0] == 12: return 2.5
        elif card[0] == 13: return 3.5
        elif card[0] == 14: return 4.5

    return 0


def print_hand(hand: list) -> None:
    print('------------------MAIN------------------')

    listCard = hand[:]
    listCard.sort(key=lambda tup: tup[0])
    listCard.sort(key=lambda tup: tup[1])


    for card in listCard:
        print(card_to_str(card))

    print('----------------------------------------')


def sort_hand(hand: list) -> list:
    listCard = hand[:]
    listCard.sort(key=lambda tup: tup[0])
    listCard.sort(key=lambda tup: tup[1])
    return listCard

def analyse_hand(hand: list) -> (int, int, list, int):
    score = 0
    bout = 0
    color_count = [0]*5
    highTrump = 0

    for card in hand:
        score += card_value(card)
        if card in [(1, 0), (21, 0), (0, 0)]:
            bout += 1
        color_count[card[1]] += 1
        if card[0]>15:
            highTrump += 1

    return score, bout, color_count, highTrump


def print_state(state: dict) -> None:
    print("la phase " + state["phase"] + " est en cour")
    print("le plis actuel est " + str(state["fold"]))
    print("le preneur actuel est agent " + str(state["taker"][0]) + " et a pris " + BID_SPACE[state["taker"][1]])
    print("le chien actuel est " + str(state["dog"]))
    print("les cartes vues sont " + str(state["cardsSeen"]))
    print("le score attaque est " + str(state["scoreTaker"]))
    print("le score defense est " + str(state["scoreDefence"]))
    print("le nombre de bout en attaque est " + str(state["boutTaker"]))
    print("le nombre de bout en defense est " + str(state["boutDefence"]))
    print("le petit est imprenable" if state["petitImprenable"] else "le petit est prenable")
