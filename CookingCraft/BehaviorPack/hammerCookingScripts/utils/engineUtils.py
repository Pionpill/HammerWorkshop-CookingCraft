'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-17 21:43:48
LastEditTime: 2022-07-17 22:04:52
'''
from time import time


def coolDown(playerId, coolDict, coolTime=0.25):
    # type: (int, dict, float) -> bool
    """交互冷却"""
    if not coolDict.get(playerId):
        coolDict[playerId] = time()
        return True
    elif time() - coolDict[playerId] < coolTime:
        return False
    else:
        coolDict[playerId] = time()
        return True
