class Move:
    def __init__(self, damage: int, KBGrowth: int, baseKB: int, setKB: int = 0, angle: int = 361):
        self.damage = damage
        self.KBGrowth = KBGrowth
        self.baseKB = baseKB
        self.setKB = setKB
        self.angle = angle

def getMove(charname: str,movename:str) -> Move:
    movedict = moves.get(charname)
    return movedict.get(movename)


moves = {
    'fox':{
        'nair':Move(12,100,10),
        'bair':Move(15,100,0),
        'shine':Move(5, 100, 0, 80, 0),
        'upsmash':Move(18,112,30,0,80)
    }
}