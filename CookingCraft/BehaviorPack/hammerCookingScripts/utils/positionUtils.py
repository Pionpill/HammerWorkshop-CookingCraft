'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-17 14:25:36
LastEditTime: 2022-07-17 17:44:41
'''
from math import sqrt
from hammerCookingScripts.utils.enumUtils import RelativePosition


def JudgeBasicPosition(oriPos, targetPos):
    # type: (tuple,tuple) -> int
    """简单判断两个方块的位置(相邻:side, 上面:above, 下面:below)"""
    delta_x = abs(oriPos[0] - targetPos[0])
    delta_y = oriPos[1] - targetPos[1]
    delta_z = abs(oriPos[2] - targetPos[2])
    if __IsAbove(delta_x, delta_y, delta_z):
        return RelativePosition.above
    elif __IsBelow(delta_x, delta_y, delta_z):
        return RelativePosition.below
    elif __IsSide_flat(delta_x, delta_y, delta_z):
        return RelativePosition.side_flat
    elif __IsSide_space(delta_x, delta_y, delta_z):
        return RelativePosition.side_space
    dis = sqrt(delta_x**2 + delta_y**2 + delta_z**2)
    if dis < 1.5:
        return RelativePosition.around_side
    elif dis < 2:
        return RelativePosition.around_space


def GetRelativePosition(posTuple, relativePosName):
    # type: (tuple,str) -> tuple
    """获取方块的临近位置"""
    x, y, z = posTuple[0], posTuple[1], posTuple[2]
    if relativePosName == "above":
        return (x, y + 1, z)
    elif relativePosName == "below":
        return (x, y - 1, z)


def __IsAbove(delta_x, delta_y, delta_z):
    return delta_x + delta_z == 0 and delta_y == 1


def __IsBelow(delta_x, delta_y, delta_z):
    return delta_x + delta_z == 0 and delta_y == -1


def __IsSide_flat(delta_x, delta_y, delta_z):
    return delta_x + delta_z == 1 and delta_y == 0


def __IsSide_space(delta_x, delta_y, delta_z):
    return delta_x + delta_z + abs(delta_y) == 1
