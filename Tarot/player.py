import utils
class PlayerObject:

    def __init__(self, hand, score, isBeginner, team, playedCard, isReal):
        self.hand = hand
        self.score = score
        self.isBeginner = isBeginner
        self._team = team
        self.playedCard = playedCard
        self.isReal = isReal

    def get_hand(self):
        return self.hand

    def add_dog(self, dog):
        self.hand += dog

    def pop_card(self, card):
        try:
            self.hand.remove(card)
        except:
            print(f"Can't remove {card}")

    def get_score(self):
        return self.score

    def add_score(self, score):
        self.score = score

    def is_beginner(self):
        return self.isBeginner

    def set_beginner(self):
        self.isBeginner = True

    def team(self):
        return self._team

    def change_team(self):
        self._team = True

    def get_played_card(self):
        return self.playedCard

    def add_played_card(self, card):
        self.playedCard.append(card)

    def is_real(self):
        return self.isReal

    def print_agent_state(self, showHand=False):
        if showHand:
            utils.print_hand(self.get_hand())

        # [[hand], int score, bool is_beginner, bool team (True = Taker)]

        print(f"    Score = {self.get_score()}")
        print("    Il commence" if self.isBeginner else "    Il ne commence pas")
        print("    Equipe Preneur" if self._team else "    Equipe defense")
        print("    Joueur humain" if self.isReal else "    Joueur ordi")