class Step:
    def __init__(self, x: float, y: float, kbxv:float, kbyv:float, charxv:float, charyv:float):
        self.x = x
        self.y = y
        self.kbxv = kbxv
        self.kbyv = kbyv
        self.charxv = charxv
        self.charyv = charyv

    def printStep(self,name='') -> None:
        if name != '':
            print(name)
            print()
        print('x:',self.x)
        print('y:', self.y)
        print('kbxv:', self.kbxv)
        print('kbyv:', self.kbyv)
        print('charxv:', self.charxv)
        print('charyv:', self.charyv)
        print('- - - - - - - - - - -')

class WorldStep:
    def __init__(self, worldX: float, worldY: float, kbxv: float, kbyv: float, charxv: float, charyv: float, frame:int, isActionable:bool = False, isDead:bool = False):
        self.worldX = worldX
        self.worldY = worldY
        self.kbxv = kbxv
        self.kbyv = kbyv
        self.charxv = charxv
        self.charyv = charyv
        self.frame = frame
        self.isActionable = isActionable
        self.isDead = isDead

    def printStep(self,name='') -> None:
        if name != '':
            print(name)
            print()
        print('x:',self.worldX)
        print('y:', self.worldY)
        print('kbxv:', self.kbxv)
        print('kbyv:', self.kbyv)
        print('charxv:', self.charxv)
        print('charyv:', self.charyv)
        print('frame',self.frame)
        print('Actionable?',self.isActionable)
        print('Dead?',self.isDead)
        print('- - - - - - - - - - -')


