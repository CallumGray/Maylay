import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

import physicsModule as phys
from moveModule import Move
from characterModule import Character

crouchPalette = {
    True:'steelblue',
    False:'firebrick'
}

def generateTumbleChart(moves:[Move],character:Character,crouching:bool=False) -> None:

    tumbles = [[move.name, phys.getEarliestTumble(move,character,crouching)] for move in moves]

    tumblesdf = pd.DataFrame(tumbles, columns=['Move', 'Percent'])
    tumblesdf.sort_values('Percent', inplace=True)
    ax = sns.barplot(data=tumblesdf, x='Move', y='Percent', hue=crouching, palette=crouchPalette)
    ax.legend_.remove()
    plt.xlabel("")
    plt.ylabel("")

    for container in ax.containers:
        labels = [int(label) if label > 0 else "" for label in container.datavalues]
        ax.bar_label(container, labels=labels, label_type='center', fontsize=20, color='w')

    plt.show()
    return None

def generateTumbleChartBoth(moves:[Move],character:Character) -> None:

    tumbles = [[move.name, phys.getEarliestTumble(move, character, False), False, phys.getEarliestTumble(move, character, False), None] for move in moves]
    tumblesCC = [[move.name, phys.getEarliestTumble(move, character, True), True, None, phys.getEarliestTumble(move, character, True)] for move in moves]
    tumbles = tumbles + tumblesCC


    tumblesdf = pd.DataFrame(tumbles, columns=['Move', 'Percent', 'Crouching', 'StandPercent', 'CrouchPercent'])
    tumblesdf.sort_values(by=['StandPercent','CrouchPercent'],inplace=True)
    ax = sns.barplot(data=tumblesdf,x='Move',y='Percent',hue='Crouching',palette=crouchPalette)
    ax.legend_.remove()

    for i,container in enumerate(ax.containers):
        color = 'w' #if i == 0 else 'black'
        labels = [int(label) if label > 0 else "" for label in container.datavalues]
        ax.bar_label(container,labels=labels, label_type='center', fontsize=20, color=color)

    plt.show()
    return None
