import ameisen

class Clemeisen(ameisen.BaseAmeise):

    def on_hatching(self):
        self.think('Ich lebe')

    def on_tick(self) -> None:
        self.think('Ich ticke')