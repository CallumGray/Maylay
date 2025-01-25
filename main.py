import time

from matplotlib.colors import LinearSegmentedColormap

import Tumble
import characterModule as charMod
import stageModule as stageMod
import moveModule as moveMod
import physicsModule as phys

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

pd.set_option('display.max_rows', None)

'''
    PLOTTING STUFF
'''

fox = charMod.getCharacter('fox')
puff = charMod.getCharacter('puff')

yoshis = stageMod.getStage('yoshis')
pokemon = stageMod.getStage('pokemon')
fd = stageMod.getStage('finalDestination')
fod = stageMod.getStage('fod')
bf = stageMod.getStage('battlefield')
dreamland = stageMod.getStage('dreamland')

bair = moveMod.getMove('fox','bair')

def trajectoryPlotExample():
    worldSteps = phys.knockbackWorldSteps(bf, 0, 0, bair, puff, 100, 0, True, False, True, True, False)
    xs, ys, actionable, frameState = phys.getWorldPlotData(worldSteps)

    dataframe = pd.DataFrame({'xs': xs, 'ys': ys, 'actionable': actionable, 'frameState': frameState})
    print(dataframe)
    palette = {True: 'pink', False: 'red'}
    markers = {'normal': '.', 'hitstunEnd': 'D', 'dead': 'X'}

    graph = sns.scatterplot(data=dataframe, x='xs', y='ys', hue='actionable', palette=palette, style='frameState',
                            markers=markers)
    graph.legend().remove()
    graph.axvline(bf.left)
    graph.axvline(bf.right)
    graph.axhline(bf.top)
    graph.axhline(bf.bottom)
    plt.show()

def upsmashExample():
    timeStart = time.time()
    yoshisPercent = phys.findHighestSurvivalPercentFixedDI(yoshis, 0, 0, upsmash, fox, 0, -17.46, True, False, True)
    pokemonPercent = phys.findHighestSurvivalPercentFixedDI(pokemon, 0, 0, upsmash, fox, 0, -17.46, True, False, True)
    fdPercent = phys.findHighestSurvivalPercentFixedDI(fd, 0, 0, upsmash, fox, 0, -17.46, True, False, True)
    fodPercent = phys.findHighestSurvivalPercentFixedDI(fod, 0, 0, upsmash, fox, 0, -17.46, True, False, True)
    bfPercent = phys.findHighestSurvivalPercentFixedDI(bf, 0, 0, upsmash, fox, 0, -17.46, True, False, True)
    dreamlandPercent = phys.findHighestSurvivalPercentFixedDI(dreamland, 0, 0, upsmash, fox, 0, -17.46, True, False,
                                                              True)
    timeEnd = time.time()

    print(yoshisPercent)
    print(pokemonPercent)
    print(fdPercent)
    print(fodPercent)
    print(bfPercent)
    print(dreamlandPercent)
    print('Time: ', timeEnd - timeStart)


def heatmapExampleBothDirections():
    print("Heatmap of where bair kills puff!")

    stage = bf
    char = puff
    move = bair

    gap = 5
    xs = [x for x in range(0,int(stage.right)+gap,gap)]
    ys = [y for y in range(0,int(stage.top)+gap,gap)]
    lxs = [x for x in range(-gap,int(stage.left)-gap,-gap)]

    pointsdone = 0
    pointcount = (len(xs)+len(lxs))*len(ys)

    zs = np.zeros((len(ys),len(xs)))
    lzs = np.zeros((len(ys),len(lxs)))

    # iterate through points on the stage and where they kill
    for xn,x in enumerate(xs):
        for yn,y in enumerate(ys):
            pointsdone+=1
            print(pointsdone,'/',pointcount)
            highestSurvivalPercent = phys.findHighestSurvivalPercent(stage,x,y,move,char,0,False,False,True)
            zs[yn][xn] = (highestSurvivalPercent)

    for xn, x in enumerate(lxs):
        for yn, y in enumerate(ys):
            pointsdone += 1
            print(pointsdone, '/', pointcount)
            highestSurvivalPercent = phys.findHighestSurvivalPercent(stage, x, y, move, char, 0, False, False, False)
            lzs[yn][xn] = (highestSurvivalPercent)

    cmap = LinearSegmentedColormap.from_list("custom",['red','orangered','orange','yellow','green','blue'])

    img = plt.imread("stages/bf.png")
    fig, ax = plt.subplots()
    ax.imshow(img,extent=[bf.left,bf.right,bf.bottom,bf.top])
    #ax.imshow(zs,cmap=cmap,interpolation='bicubic',alpha=0.5,extent=[yoshis.left,yoshis.right,yoshis.bottom,yoshis.top])
    mesh = ax.pcolormesh(xs,ys, zs,cmap=cmap,vmin=60,vmax=120, alpha=0.5)
    mesh2 = ax.pcolormesh(lxs,ys,lzs,cmap=cmap,vmin=60,vmax=120,alpha=0.5)

    plt.colorbar(mesh,ax=ax)
    plt.xticks(np.arange(-200,200,50))
    plt.axvline(stage.left)
    plt.axvline(stage.right)
    plt.axhline(stage.top)
    plt.savefig("test.png")

    plt.show()


def foxTumblesPuff():
    moveStrings = ['nair','bair','jab','dash','dtilt','uptilt1', 'uptilt2','upsmash']
    moves = [moveMod.getMove('fox',name) for name in moveStrings]
    Tumble.generateTumbleChart(moves,puff)
    Tumble.generateTumbleChart(moves,puff,True)

def start():

#    foxTumblesPuff()
    trajectoryPlotExample()
    #heatmapExampleBothDirections()

    #x = Tumble.generateTumbleChart([upsmash,nair,shine,bair],fox)
    #y = Tumble.generateTumbleChart([upsmash, nair, shine, bair], fox,True)
    #z = Tumble.generateTumbleChartBoth([upsmash, nair, shine, bair], fox)

if __name__ == '__main__':
    start()
