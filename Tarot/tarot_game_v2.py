import random

import utils
import player
import agent_IA

class TarotGame:

    def __init__(self, beginner, whoIsReal=[True]*5):
        print("Lancement de la partie")

        self.beginner = beginner  # who begin
        self.cardList = utils.card_list()
        self.actualTaker = (0, 0)
        self.cardsSeen = []  # liste des cartes vue par tout le monde
        self.scoreTaker = 0
        self.scoreDefence = 0
        self.boutTaker = 0
        self.boutDefence = 0
        self.king = (14, 1)
        self.fold = None
        self.firstTurn = True
        self.petitImprenable = False
        # Battage des cartes
        random.shuffle(self.cardList)


        # Création des agents -> [[hand], int score, bool is_beginner, bool team (True = Taker), [played_card], bool isreal]
        self.agents = [player.PlayerObject(self.cardList[15 * i:15 + 15 * i],
                                           0,
                                           False,
                                           False,
                                           [],
                                           whoIsReal[i])
                       for i in range(5)]

        self.dog = self.cardList[75:78]

        for agent in self.agents:
            atout = [e for e in agent.get_hand() if e[1] == 0]
            if atout == [(1, 0)]:
                self.petitImprenable = True

        # détermination de la personne qui commence le tour
        self.agents[self.beginner].set_beginner()

        # initialisation du jeu en phase "contract"
        self.gamePhase = "contract"

    def _ask_agent(self, nbAgent, _str, callableCards):

        if self.agents[nbAgent].is_real():

            for nb, card in enumerate(callableCards):
                print(f"{nb}: {utils.card_to_str(card)}")

            try:
                choice = int(input(_str))
            except:
                choice = -1
        else:
            choice = agent_IA.ask_agent_IA(self.get_state(), self.agents[nbAgent], nbAgent)

        return choice
    def _turn_contract(self):

        actualTaker = (0, 0)

        for nbTurnContract in range(5):
            print("----------------------------------------")
            print(f"Agent {(self.beginner + nbTurnContract) % 5}?\n")

            valid = False
            while not valid:
                prise = self._ask_agent((self.beginner + nbTurnContract) % 5,
                                        "0:passe\n1:petite\n2:Garde\n3:Garde Sans\n4:Garde Contre",
                                        [])

                if prise > actualTaker[1] and prise <= 5:
                    valid = True
                    print(f"Agent {(self.beginner + nbTurnContract) % 5} choisi la {utils.print_prise(prise)}")
                    actualTaker = ((self.beginner + nbTurnContract) % 5, prise)
                elif prise == 0 or prise <= actualTaker[1]:
                    valid = True
                    print(f"Agent {(self.beginner + nbTurnContract) % 5} passe")
                else:
                    print("choix invalide")

        return actualTaker

    def _choose_king(self):
        print("----------------------------------------")
        print(f"Agent {self.actualTaker[0]}?\n")

        king = None

        callableCards = utils.who_can_call(self.agents[self.actualTaker[0]].get_hand())

        valid = False

        while not valid:
            call = self._ask_agent(self.actualTaker[0], "Apeller :", callableCards)

            for nb, card in enumerate(callableCards):
                if call == nb:
                    king = card
                    valid = True
                    print(f"Agent {self.actualTaker[0]} apelle le " + utils.card_to_str(king))
                    break

            if not valid:
                print("choix invalide")

        return king

    def _choose_dog(self):
        print("----------------------------------------")
        print(f"Agent {self.actualTaker[0]}?\n")
        print("Chien :")

        for card in self.dog:
            print(utils.card_to_str(card))
            self.cardsSeen.append(card)

        self.agents[self.actualTaker[0]].add_dog(self.dog)

        newDog = []

        print("Constituer le chien :")
        for _ in range(3):
            removableCards = utils.removable_cards(self.agents[self.actualTaker[0]].get_hand(), self.dog)

            valid = False

            while not valid:
                dog = self._ask_agent(self.actualTaker[0], "Mettre dans le chien :", removableCards)

                for nb, card in enumerate(removableCards):
                    if dog == nb:
                        newDog.append(card)
                        self.agents[self.actualTaker[0]].pop_card(card)
                        valid = True
                        break

                if not valid:
                    print("choix invalide")

        return newDog

    def _play_card(self, nbCardPlayed, fold):
        print("----------------------------------------")
        print(f"Agent {(self.beginner + nbCardPlayed) % 5}?\n")
        print("Plis actuel :")
        for e in fold:
            print(utils.card_to_str(e))
        if not fold:
            print("Pas de carte\n")

        # print hand
        utils.print_hand(self.agents[(self.beginner + nbCardPlayed) % 5].get_hand())

        restrictedColor = self.king[1] if self.firstTurn else None
        playableCard = utils.legal_move(fold, self.agents[(self.beginner + nbCardPlayed) % 5].get_hand(), restrictedColor=restrictedColor)
        playedCard = None

        valid = False

        while not valid:
            call = self._ask_agent((self.beginner + nbCardPlayed) % 5, "Jouer :", playableCard)

            for nb, card in enumerate(playableCard):
                if call == nb:
                    playedCard = card
                    print(f"Agent {(self.beginner + nbCardPlayed) % 5} joue " + utils.card_to_str(playedCard))
                    valid = True
                    break

            if not valid:
                print("choix invalide")

        # remove card from agent's hand
        self.agents[(self.beginner + nbCardPlayed) % 5].pop_card(playedCard)

        # add to its played card and global seen card
        self.agents[(self.beginner + nbCardPlayed) % 5].add_played_card([fold, playedCard])
        self.cardsSeen.append(playedCard)

        return fold + [playedCard]

    def get_state(self):
        return {"phase": self.gamePhase,
                "fold": self.fold,
                "taker": self.actualTaker,
                "dog": self.dog,
                "cardsSeen": self.cardsSeen,
                "scoreTaker": self.scoreTaker,
                "scoreDefence": self.scoreDefence,
                "boutTaker": self.boutTaker,
                "boutDefence": self.boutDefence,
                "petitImprenable": self.petitImprenable,
                "agents": self.agents,
                "beginner": self.beginner
        }

    def play_step(self):

        if self.gamePhase == "contract":
            self.actualTaker = self._turn_contract()

            # set taker agent to team taker
            self.agents[self.actualTaker[0]].change_team()

            # stop game if no taker, else continue to king phase
            if self.actualTaker[1] == 0:
                self.gamePhase = 'end'
            else:
                self.gamePhase = 'choose_king'

        elif self.gamePhase == 'choose_king':
            self.king = self._choose_king()

            # set king agent to team taker
            for i, agent in enumerate(self.agents):
                if self.king in agent.get_hand():
                    self.agents[i].change_team()

            self.gamePhase = 'dog'

        elif self.gamePhase == 'dog':
            self.dog = self._choose_dog()

            self.gamePhase = 'main_phase'

        elif self.gamePhase == 'main_phase':

            self.fold = []
            for nbCardPlayed in range(5):
                self.fold = self._play_card(nbCardPlayed, self.fold)

            self.firstTurn = False

            winCardID, score = utils.analyse_fold(self.fold, self.petitImprenable)

            self.agents[(self.beginner + winCardID) % 5].add_score(score)

            if self.agents[(self.beginner + winCardID) % 5].team():
                self.scoreTaker += score
            else:
                self.scoreDefence += score

            if (0, 0) in self.fold:
                excuseID = self.fold.index((0, 0))

                self.agents[(self.beginner + excuseID) % 5].add_score(4.5)
                if self.agents[(self.beginner + excuseID) % 5].team():
                    self.scoreTaker += 4.5
                    self.boutTaker += 1
                else:
                    self.scoreDefence += 4.5
                    self.boutDefence += 1

            if (1, 0) in self.fold:
                if self.petitImprenable:
                    petitID = self.fold.index((1, 0))

                    self.agents[(self.beginner + petitID) % 5].add_score(4.5)
                    if self.agents[(self.beginner + petitID) % 5].team():
                        self.scoreTaker += 4.5
                        self.boutTaker += 1
                    else:
                        self.scoreDefence += 4.5
                        self.boutDefence += 1
                else:
                    if self.agents[(self.beginner + winCardID) % 5].team():
                        self.boutTaker += 1
                    else:
                        self.boutDefence += 1

            if (21, 0) in self.fold:
                if self.agents[(self.beginner + winCardID) % 5].team():
                    self.boutTaker += 1
                else:
                    self.boutDefence += 1

            self.beginner += winCardID
            self.beginner = self.beginner % 5

            if int(self.scoreTaker + self.scoreDefence) == 90:
                self.gamePhase = 'end'


if __name__ == "__main__":

    #Pour créer une partie :
    #T = TarotGame(quicommence: int entre 0 et 4, [liste des joueurs 1 = réel (joue avec la console, 0 = IA]
    #Creation d'une partie avec 1 joueur réel et des IA
    T = TarotGame(0, [1,0,0,0,0])

    #affichage des mains. T.get_state() renvoie l'entiereté de l'état du jeu, dont les agents
    for i, agent in enumerate(T.get_state()["agents"]):
        print(f"agent {i}")
        utils.print_hand(agent.get_hand())

    utils.print_state(T.get_state())
    #for i, agent in enumerate(T.get_state()[10]):
    #    print(f"agent {i}")
    #    agent.print_agent_state()

    #boucle principale
    #TODO trouver moyen de finir la partie (il suffit d'analyser les mains jusqu'a qu'elles soient toute vide)
    while True:
        T.play_step()

