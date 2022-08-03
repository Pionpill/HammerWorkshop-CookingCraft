'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-17 15:46:37
LastEditTime: 2022-07-30 16:26:28
'''
import mod.server.extraServerApi as serverApi

compFactory = serverApi.GetEngineCompFactory()
minecraftEnum = serverApi.GetMinecraftEnum()


def GetBlockName(levelId, pos, dimensionId):
    # type: (int, tuple, int) -> str
    """通过位置获取方块名"""
    blockDict = compFactory.CreateBlockInfo(levelId).GetBlockNew(
        pos, dimensionId)
    return blockDict.get("name")


def GetBlockEntityData(pos, dimensionId, id):
    # type: (tuple, int, int) -> dict
    """
    获取方块信息字典
    id 可以是 playerId, levelId
    """
    blockEntityComp = compFactory.CreateBlockEntityData(id)
    return blockEntityComp.GetBlockEntityData(dimensionId, pos)


def GetBlockInfo(pos, id):
    # type: (tuple, int) -> Dict
    """获取方块信息数据"""
    blockComp = compFactory.CreateBlockInfo(id)
    return blockComp.GetBlockNew(pos)
