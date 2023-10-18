import time

from matplotlib.colors import ListedColormap,LinearSegmentedColormap

import characterModule as charMod
import stageModule as stageMod
import physicsModule as phys
from moveModule import Move

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

upsmash = Move(18,112,30,0,80)
nair = Move(12, 100, 10)
shine = Move(5, 100, 0, 80, 0)

def trajectoryPlotExample():
    worldSteps = phys.knockbackWorldSteps(yoshis, 0, 0, nair, fox, 120, 0, True, False, True, True, False)
    xs, ys, actionable, frameState = phys.getWorldPlotData(worldSteps)

    dataframe = pd.DataFrame({'xs': xs, 'ys': ys, 'actionable': actionable, 'frameState': frameState})
    print(dataframe)
    palette = {True: 'pink', False: 'red'}
    markers = {'normal': '.', 'hitstunEnd': 'D', 'dead': 'X'}

    graph = sns.scatterplot(data=dataframe, x='xs', y='ys', hue='actionable', palette=palette, style='frameState',
                            markers=markers)
    graph.legend().remove()
    graph.axvline(yoshis.left)
    graph.axvline(yoshis.right)
    graph.axhline(yoshis.top)
    graph.axhline(yoshis.bottom)
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


def heatmapExample():
    print("Heatmap of where bair kills puff!")

    stage = yoshis
    char = puff
    move = nair

    pointcount = 0

    xs = [x for x in range(0,int(stage.right), 20)]
    ys = [y for y in range(0,int(stage.top/2),20)]

    zs = np.zeros((len(ys),len(xs)))

    # iterate through points on the stage and where they kill
    for xn,x in enumerate(xs):
        for yn,y in enumerate(ys):
            pointcount+=1
            highestSurvivalPercent = phys.findHighestSurvivalPercent(stage,x,y,move,char,0,False,False,True)
            zs[yn][xn] = (highestSurvivalPercent)

    print(pointcount)

    cmap = LinearSegmentedColormap.from_list("custom",["red","orange","yellow","green"])
    fig, ax = plt.subplots()
    mesh = ax.pcolor(xs,ys, zs,cmap=cmap,vmin=50,vmax=150)
    plt.colorbar(mesh,ax=ax)
    plt.show()


def start():
    heatmapExample()


if __name__ == '__main__':
    start()
