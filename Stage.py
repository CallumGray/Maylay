class Stage:
    def __init__(self, top: int, bottom: int, left:float, right:float):
        self.top = top
        self.bottom = bottom
        self.left = left
        self.right = right

# Inside Stage area (solid parts) to ignore
#Boundaries
#Platform Data

stages = {
    'yoshis':{
        'top': 168,
        'bottom': -91,
        'left': -175.7,
        'right': 173.6
    },
    'pokemon':{
        'top': 180,
        'bottom': -111,
        'left': -230,
        'right': 230
    },
    'finalDestination':{
        'top': 188,
        'bottom': -140,
        'left': -246,
        'right': 246
    },
    'fod':{
        'top': 202.5 ,
        'bottom': -146.25,
        'left': -198.75,
        'right': 198.75
    },
    'battlefield':{
        'top': 200,
        'bottom': -108.8,
        'left': -224,
        'right': 224
    },
    'dreamland':{
        'top': 250,
        'bottom': -123,
        'left': -255,
        'right': 255
    }
}

def getStage(name: str) -> Stage:
    d = stages.get(name)

    if d:
        return Stage(d.get('top'), d.get('bottom'), d.get('left'), d.get('right'))
    else:
        print(name,"does not exist!")
        return None

'''

surfaces.bf = [
    [[-68.4, 0], [68.4, 0]], 
    [[-57.6, 27.2], [-20.0, 27.2]], 
    [[20, 27.2], [57.6, 27.2]], 
    [[-18.8, 54.4], [18.8, 54.4]]
];

surfaces.fd = [
    [[-85.56570, 0], [85.56570, 0]]
];

surfaces.dl = [
    [[-77.2713, 0.0089], [77.2713, 0.0089]], 
    [[-61.3929, 30.1422], [-31.7254, 30.1422]], 
    [[31.7036, 30.2426], [63.0745, 30.2426]], 
    [[-19.0181, 51.4254], [19.0171, 51.4254]]
];

surfaces.ps = [
    [[-87.75, 0], [87.75, 0]], 
    [[-55, 25], [-25, 25]], 
    [[25, 25], [55, 25]]
];

surfaces.ys = [
    [[-56, 0], [56, 0]], 
    [[-59.5, 23.45], [-28, 23.45]], 
    [[28, 23.45], [59.5, 23.45]], 
    [[-15.75, 42], [15.75, 42]]
];

surfaces.fo = [
    [[-63.34755, 0.00288], [63.34755, 0.00288]], 
    [[-14.25, 42.75], [14.25, 42.75]]
];

'''