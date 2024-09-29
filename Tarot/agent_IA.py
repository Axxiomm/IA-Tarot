import player
import utils
import random


def ask_agent_IA(gameState, agent: player.PlayerObject, nbAgent):

    hand = agent.get_hand()

    if gameState["phase"] == 'contract':
        return analyse_take(hand)

    if gameState["phase"] == 'choose_king':
        king = analyse_king(hand)
        return utils.who_can_call(hand).index(king)

    if gameState["phase"] == 'dog':
        if len(hand) == 18:pass
        return 0

    if gameState["phase"] == 'main_phase':
        return 0

    return 0


def analyse_take(hand):

    handAnalysed = utils.analyse_hand(hand)

    if (counter(handAnalysed, 15, 2, 4, 1, 8, 4)
            or counter(handAnalysed, 0, 3, 0, 0, 15, 0)):  #GARDE CONTRE
        return 4

    if counter(handAnalysed, 15, 2, 4, 1, 0, 3):  #GARDE SANS
        return 3

    if (counter(handAnalysed, 10, 2, 3, 0, 5, 0)
            or counter(handAnalysed, 20, 1, 4, 0, 5, 2)):  #GARDE
        return 2

    if counter(handAnalysed, 15, 1, 3, 0, 4, 0):  #PETITE
        return 1

    return 0  #PASSE


def analyse_king(hand):
    choices = utils.who_can_call(hand)
    choices = [choice for choice in choices if choice not in hand]

    #http://www.tarotjeu.com/lappel-au-roi/

    colorCounter = utils.analyse_hand(hand)[2][1:]

    king = 0  #au cas ou rien ne sorte

    if (1, 0) in hand and random.random() > 0.5:
        king = colorCounter.index(min(colorCounter))

    else:
        mid = colorCounter[:]
        mid[mid.index(min(mid))] = -1
        mid[mid.index(max(mid))] = -1
        random.shuffle(mid)
        for i, _ in enumerate(mid):
            if i != -1:
                king = i

    king = (choices[0][0], king+1)  #mettre choices[0][0] pour appeler une dame si il n'y a pas de roi dans choices

    return king if king in choices else analyse_king(hand+[king])



def counter(handAnalysed, scoreMin, boutMin, longueMin, nbcutMin, nbTrumpMin, nbHighTrumpMin):
    score, bout, color_count, highTrump = handAnalysed
    return (score >= scoreMin
            and bout >= boutMin
            and max(color_count[1:]) >= longueMin
            and color_count.count(0) >= nbcutMin
            and color_count[0] >= nbTrumpMin
            and highTrump >= nbHighTrumpMin)


