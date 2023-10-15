class Character:
    def __init__(self, weight: int, fallSpeed: float, gravity: float, driftMax: float, driftAcc: float,
                 airFriction: float, djSetY: float, djInitX: float, djInitY: [float]):
        self.weight = weight
        # fall speed is terminal velocity
        self.fallSpeed = fallSpeed
        # gravity is max fall speed
        self.gravity = gravity
        # driftmax is air speed max
        self.driftMax = driftMax
        # driftacc is air acceleration
        self.driftAcc = driftAcc
        self.airFriction = airFriction
        self.djSetY = djSetY
        self.djInitX = djInitX
        self.djInitY = djInitY


# Make sure djInitY is given as an array!
characters = {
    'fox': {
        'NTSCweight': 75,
        'PALweight': 73,
        'gravity': 0.23,
        'terminalVelocity': 2.8,
        'driftAcc': 0.08,
        'driftMax': 0.83,
        'djInitX': 0.90,
        'djInitY': [4.416],
        'airFriction': 0.02,
        'djSetY': False,
        'traction': 0.08
    },
    'puff': {
        'NTSCweight': 60,
        'PALweight': 60,
        'gravity': 0.064,
        'terminalVelocity': 1.3,
        'driftAcc': 0.28,
        'driftMax': 1.35,
        'djInitX': 0.292,
        'djInitY': [1.65],
        'airFriction': 0.05,
        'djSetY': False,
        'traction': 0.09
    }
}


def getCharacter(name: str) -> Character:
    d = characters.get(name)

    if d:
        return Character(d.get('NTSCweight'), d.get('terminalVelocity'), d.get('gravity'), d.get('driftMax'), d.get('driftAcc'), d.get('airFriction'),
                     d.get('djSetY'), d.get('djInitX'), d.get('djInitY'))
    else:
        print(name,"does not exist!")
        return None