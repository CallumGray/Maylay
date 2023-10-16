class Move:
    def __init__(self, damage: int, KBGrowth: int, baseKB: int, setKB: int = 0, angle: int = 361):
        self.damage = damage
        self.KBGrowth = KBGrowth
        self.baseKB = baseKB
        self.setKB = setKB
        self.angle = angle
