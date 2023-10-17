import characterModule as charMod
import stageModule as stageMod
import physicsModule as phys
from moveModule import Move

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

pd.set_option('display.max_rows', None)

'''
    PLOTTING STUFF
'''

def start():
    fox = charMod.getCharacter('fox')
    yoshis = stageMod.getStage('yoshis')

    upsmash = Move(18,112,30,0,80)
    nair = Move(12, 100, 10)
    shine = Move(5, 100, 0, 80, 0)

    worldSteps = phys.knockbackWorldSteps(yoshis, 0, 0, nair, fox, 120, 0, True, False, True, True, False)
    xs, ys, actionable, frameState = phys.getWorldPlotData(worldSteps)

    dataframe = pd.DataFrame({'xs':xs, 'ys':ys, 'actionable':actionable,'frameState':frameState})
    print(dataframe)
    palette = {True:'pink',False:'red'}
    markers = {'normal':'.','hitstunEnd':'D','dead':'X'}

    graph = sns.scatterplot(data=dataframe,x='xs',y='ys',hue='actionable', palette=palette, style='frameState',markers=markers)
    graph.legend().remove()
    graph.axvline(yoshis.left)
    graph.axvline(yoshis.right)
    graph.axhline(yoshis.top)
    graph.axhline(yoshis.bottom)
    plt.show()


if __name__ == '__main__':
    start()
