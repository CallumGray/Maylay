class Move:
    def __init__(self, name:str, damage: int, KBGrowth: int, baseKB: int, setKB: int = 0, angle: int = 361):
        self.name = name
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
        'nair':Move('Nair',12,100,10),
        'bair':Move('Bair',15,100,0),
        'shine':Move('Shine',5, 100, 0, 80, 0),
        'upsmash':Move('UpSmash',18,112,30,0,80),
        'uptilt1':Move('UpTilt Grnd',12,140,18,0,110),
        'uptilt2':Move('UpTilt Air',9,140,18,0,84),
        'dtilt':Move('DownTilt',10,125,25,0,70),
        'jab':Move('Jab',4,100,0,0,70),
        'dash':Move('Dash Atk',7,90,35,0,72)
    }
}