import math

from characterModule import Character
import characterModule as charMod

from stepModule import Step, WorldStep
import stepModule as stepMod

from stageModule import Stage
import stageModule as stageMod

from moveModule import Move

'''
KNOCKBACK
'''


# Calculates knockback value of an attack
def getKnockback(move: Move, character: Character, percentBeforeHit: float, isCrouched: bool = False) -> float:
    p: float = percentBeforeHit + move.damage
    d: int = move.damage

    if move.setKB > 0:
        p = 10
        d = move.setKB

    w: int = character.weight
    s: float = move.KBGrowth / 100
    b: int = move.baseKB
    r: float = 2 / 3 if isCrouched else 1

    A: float = (p / 10) + (p * d) / 20
    B: float = 280 / (w + 100)

    return ((((A * B) + 18) * s) + b) * r


'''
HITSTUN
'''


def getHitstun(knockback: float) -> int:
    return int(knockback * 0.4)


'''
LAUNCH SPEEDS
'''


def getLaunchSpeed(knockback: float) -> float:
    return knockback * 0.03


def getHorizontalVelocity(launchSpeed: float, angle: float) -> float:
    return launchSpeed * math.cos(math.radians(angle))


def getVerticalVelocity(launchSpeed: float, angle: float) -> float:
    return launchSpeed * math.sin(math.radians(angle))


def getHorizontalDecay(angle: float) -> float:
    return 0.051 * math.cos(math.radians(angle))


def getVerticalDecay(angle: float) -> float:
    return 0.051 * math.sin(math.radians(angle))


'''
LAUNCH ANGLES
'''


def getAngle(move: Move, knockback: float, grounded: bool = False) -> float:
    # Not sakurai angle stuff
    if move.angle != 361:
        return move.angle

    # Sakurai angle stuff
    if not grounded:
        return 45

    if knockback < 32:
        return 0

    if knockback > 32.1:
        return 44

    interp = (knockback - 32) / (32.1 - 32)
    return 44 * interp


'''
TUMBLE
'''

TUMBLE_THRESHOLD: int = 80


def calculateEarliestTumble(move: Move, character: Character, isCrouched: bool = False) -> int:
    s: float = move.KBGrowth / 100
    d: int = move.damage
    w: int = character.weight
    b: int = move.baseKB
    r: float = 2 / 3 if isCrouched else 1

    numerator: float = TUMBLE_THRESHOLD - 18 * s * r - b * r
    denominatorA: float = (1 / 10) + (d / 20)
    denominatorB: float = (280 * s * r) / (w + 100)

    result: int = math.ceil((numerator - d * (denominatorA * denominatorB)) / (denominatorA * denominatorB))
    return 0 if result < 0 else result


def setTumble(move: Move, character: Character, isCrouched: bool) -> int:
    result = getKnockback(move, character, None, isCrouched)
    return 0 if result > TUMBLE_THRESHOLD else None


# Calculates earliest percent a move will cause tumble
def getEarliestTumble(move: Move, character: Character, isCrouched: bool = False) -> int:
    if move.setKB > 0:
        return setTumble(move, character, isCrouched)
    else:
        return calculateEarliestTumble(move, character, isCrouched)


'''
SIMULATION
'''


# A step is (x, y, kbxv, kbyv, charxv, charyv)
# -18 < DI < 18
def knockbackSteps(move: Move, character: Character, percentBeforeHit, DI: float = 0, grounded=False, isCrouched=False,
                   fadeIn=True, doubleJump=False) -> ([Step], [Step]):
    hitstunSteps: [Step] = []
    actionableSteps: [Step] = []

    knockback: float = getKnockback(move, character, percentBeforeHit, isCrouched)
    launchSpeed: float = getLaunchSpeed(knockback)
    hitstun: int = getHitstun(knockback)
    launchAngle = getAngle(move, knockback, grounded)
    launchAngle = max(0., launchAngle + DI)

    x: float = 0
    y: float = 0

    charxv: float = 0
    charyv: float = 0

    kbxv: float = getHorizontalVelocity(launchSpeed, launchAngle)
    kbyv: float = getVerticalVelocity(launchSpeed, launchAngle)

    xDecay: float = getHorizontalDecay(launchAngle)
    yDecay: float = getVerticalDecay(launchAngle)

    gravityFrames: int = int(character.fallSpeed / character.gravity)
    lastFrameGravityValue: float = character.fallSpeed % character.gravity

    # Hitstun frames
    for i in range(hitstun):
        # Sideways knockback
        if not kbxv == 0:
            if kbxv > 0:
                kbxv = max(kbxv - xDecay, 0)
            else:
                kbxv = min(kbxv - xDecay, 0)

        # Vertical knockback
        if not kbyv == 0:
            if kbyv > 0:
                kbyv = max(kbyv - yDecay, 0)
            else:
                kbyv = min(kbyv - yDecay, 0)

        # Move character by gravity
        if i < gravityFrames:
            charyv -= character.gravity
        elif i == gravityFrames:
            charyv -= lastFrameGravityValue

        x = x + charxv + kbxv
        y = y + charyv + kbyv

        step = Step(x, y, kbxv, kbyv, charxv, charyv)
        hitstunSteps.append(step)

    # Actionable steps

    hasDoubleJumped: bool = False
    e: int = 0
    gravityFramesLeft = max(gravityFrames - hitstun, 0)

    # Simulates frames until knockback has fully decayed
    while abs(kbxv) > 0 or abs(kbyv) > 0:
        if kbxv != 0:
            if kbxv > 0:
                kbxv = max(kbxv - xDecay, 0)

            else:
                kbxv = min(kbxv - xDecay, 0)

        if kbyv != 0:
            if kbyv > 0:
                kbyv = max(kbyv - yDecay, 0)

            else:
                kbyv = min(kbyv - yDecay, 0)

        # Apply gravity
        if gravityFramesLeft > 1:
            charyv -= character.gravity
        elif gravityFramesLeft == 1:
            charyv -= lastFrameGravityValue

        gravityFramesLeft -= 1

        if (doubleJump and not hasDoubleJumped):
            if character.djSetY:
                charyv = character.djInitY[e]
                e += 1
                # djsetx and djxvalues stuff ignored here because they're just for ness?! (Very stupid)
            else:
                charyv = character.djInitY[e]

            if fadeIn:
                if x > 0:
                    charxv = -character.djInitX
                elif x < 0:
                    charxv = character.djInitX

            hasDoubleJumped = True

        if hasDoubleJumped:
            charyv -= character.gravity
            charyv = max(-character.fallSpeed, charyv)

        if fadeIn:
            if x > 0:
                if charxv < -character.driftMax:
                    charxv += character.airFriction
                    charxv = min(charxv, -character.driftMax)
                else:
                    charxv -= character.driftAcc
                    charxv = max(charxv, -character.driftMax)

            elif (x < 0):
                if charxv > character.driftMax:
                    charxv -= character.airFriction
                    charxv = max(charxv, -character.driftMax)

                else:
                    charxv += character.driftAcc
                    charxv = min(charxv, character.driftMax)

        x = x + charxv + kbxv
        y = y + charyv + kbyv

        step = Step(x, y, kbxv, kbyv, charxv, charyv)
        actionableSteps.append(step)

    return (hitstunSteps, actionableSteps)


def isDead(stage: Stage, worldX: float, worldY: float, kbyv: float):
    return worldX >= stage.right or worldX <= stage.left or worldY <= stage.bottom or (
                worldY >= stage.top and kbyv >= 2.4)


# returns steps relative to a starting position within a stage (giving death info)
def knockbackWorldSteps(stage: Stage, x: float, y: float, move: Move, character: Character, percentBeforeHit,
                        DI: float = 0, grounded: bool = False, isCrouched: bool = False, fadeIn: bool = True,
                        doubleJump: bool = True, hitRight:bool = True) -> [WorldStep]:
    worldSteps: [WorldStep] = []

    hitstunSteps, actionableSteps = knockbackSteps(move, character, percentBeforeHit, DI, grounded, isCrouched, fadeIn,
                                                   doubleJump)

    hitstunFrames = len(hitstunSteps)

    # 1 if right, -1 if left
    d = -1 + hitRight * 2

    # frame
    for frame, hs in enumerate(hitstunSteps, 1):
        worldX = x + d*hs.x
        worldY = y + hs.y
        kbxv = d*hs.kbxv
        kbyv = hs.kbyv
        charxv = d*hs.charxv
        charyv = hs.charyv

        if isDead(stage, worldX, worldY, kbyv):
            worldStep = WorldStep(worldX, worldY, kbxv, kbyv, charxv, charyv, frame, False, True)
            worldSteps.append(worldStep)
            return worldSteps
        else:
            worldStep = WorldStep(worldX, worldY, kbxv, kbyv, charxv, charyv, frame, False, False)
            worldSteps.append(worldStep)

    for frame, acs in enumerate(actionableSteps, hitstunFrames+1):
        worldX = x + d*acs.x
        worldY = y + acs.y
        kbxv = d*acs.kbxv
        kbyv = acs.kbyv
        charxv = d*acs.charxv
        charyv = acs.charyv

        if isDead(stage, worldX, worldY, kbyv):
            worldStep = WorldStep(worldX, worldY, kbxv, kbyv, charxv, charyv, frame, True, True)
            worldSteps.append(worldStep)
            return worldSteps
        else:
            worldStep = WorldStep(worldX, worldY, kbxv, kbyv, charxv, charyv, frame, True, False)
            worldSteps.append(worldStep)

    return worldSteps

'''

    STARTING THE PROGRAM

'''


def start():
    fox = charMod.getCharacter('fox')
    yoshis = stageMod.getStage('yoshis')

    nair = Move(12, 100, 10)
    shine = Move(5, 100, 0, 80, 0)

    worldSteps = knockbackWorldSteps(yoshis,0,0,nair,fox,80,0,True,False,True,True,False)
    lastHitstunFrame = stepMod.getLastHitstunFrame(worldSteps)
    lastHitstunFrame.printStep('Last hitstun step')
    lastHitstunFrame.printStep('Last hitstun step 2')
    lastHitstunFrame.printStep()


if __name__ == '__main__':
    start()
