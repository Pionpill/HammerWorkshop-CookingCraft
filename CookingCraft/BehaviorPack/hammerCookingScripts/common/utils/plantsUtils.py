'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-15 21:13:48
LastEditTime: 2022-07-17 19:22:36
'''
from hammerCookingScripts import logger

SEEDS_NAME = [
    "cookingcraft:herb_seeds", "cookingcraft:pepper", "cookingcraft:rice_fruit",
    "cookingcraft:corn_pieces", "cookingcraft:tomato", "cookingcraft:onion",
    "cookingcraft:banana"
]


def GetSeedNameByStageBlock(blockName):
    # type: (str) -> str
    """通过生长时block名获取种子名字"""
    itemName = blockName.split("_")[0]
    itemName = itemName.split(":")[-1]
    for seedName in SEEDS_NAME:
        if itemName in seedName:
            return seedName


def IsModSeed(itemName):
    # type: (str) -> bool
    """判断物品是否是模组种子"""
    return itemName in SEEDS_NAME


def GetNextStageName(currentBlockName):
    # type: (str) -> str
    """获取农作物下一阶段 block 名，不检查 stage 是否超范围"""
    stageId = GetStageId(currentBlockName)
    seedName = GetSeedNameByStageBlock(currentBlockName)
    return GetStageNameById(seedName, stageId + 1)


def GetFirstStageName(seedName):
    # type: (str) -> str
    """获取首个植物生长状态方块
    Returns:
        str: 首个植株的 BlockName
    """
    return GetStageNameById(seedName, 0)


def GetStageNameById(seedName, stageId):
    # type: (str, int) -> str
    """通过状态 Id 获取种植时 block 名，注意这里不对 id 的范围进行检查，由调用它的方法检查"""
    return seedName.split("_")[0] + "_stage_" + str(stageId)


def GetStageId(blockName):
    # type: (str) -> int
    """通过植物生长状态方块获取状态Id"""
    return int(blockName.split("_")[-1])
