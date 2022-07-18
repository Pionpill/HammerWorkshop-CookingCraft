'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-17 15:46:37
LastEditTime: 2022-07-17 19:16:13
'''
import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


def GetBlockName(levelId, blockPos, dimension):
    # type: (int, tuple, int) -> str
    """通过位置获取方块名"""
    blockDict = compFactory.CreateBlockInfo(levelId).GetBlockNew(
        blockPos, dimension)
    return blockDict.get("name")


def GetBlockEntityData(blockPos, dimension, playerId):
    # type: (tuple, int, int) -> dict
    """获取方块信息字典"""
    blockEntityComp = compFactory.CreateBlockEntityData(playerId)
    return blockEntityComp.GetBlockEntityData(dimension, blockPos)
