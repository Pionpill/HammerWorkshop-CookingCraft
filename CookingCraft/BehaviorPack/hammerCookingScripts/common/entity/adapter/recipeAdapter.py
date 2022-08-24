# -*- coding:utf-8 -*-
'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 00:16:40
LastEditTime: 2022-08-25 00:38:29
'''
from hammerCookingScripts import logger


def CookingTableRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str, dict) -> dict
    """cookingcraft:cooking_table 的配方调试器"""
    return __CraftingRecipeAdapter(recipeName,
                                   rawRecipeDict,
                                   materialSlotNum=13)


def ButcherTableRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str, dict) -> dict
    """cookingcraft:cooking_table 的配方调试器"""
    return __CraftingRecipeAdapter(recipeName,
                                   rawRecipeDict,
                                   materialSlotNum=13)


def BakingRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:baking_furnace 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict)


def FryerRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:baking_furnace 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict)


def GrillRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:baking_furnace 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict)


def MillRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:mill 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict, 1, 2)


def PanRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:pan 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict, 11, 1)


def SqueezerRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:squeezer 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict, 3, 1)


def SteamerRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:food_steamer 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict)


def StewRecipeAdapter(recipeName, rawRecipeDict):
    # type: (str,dict) -> dict
    """cookingcraft:stew_pot 的配方调试器"""
    return __FurnaceRecipeAdapter(recipeName, rawRecipeDict, 7)


def __CraftingRecipeAdapter(recipeName,
                            rawRecipeDict,
                            materialSlotNum=9,
                            resultSlotNum=1):
    # sourcery skip: use-fstring-for-concatenation
    # type: (str, dict,int,int) -> dict
    """烹饪桌单个配方调试器:补全数据(槽位的None 与 物品的 count，newAuxValue)"""
    materialsDict = rawRecipeDict.get("materials")
    resultsDict = rawRecipeDict.get("results")
    # 结果槽转换为键值对形式
    if resultsDict.get("result_slot0") is None:
        resultsDict = {"result_slot0": resultsDict}
    if materialsDict is None or resultsDict is None:
        logger.error("{0} 缺失 ，materials 或 results 键".format(recipeName))
    for id in range(materialSlotNum):
        if materialsDict.get("material_slot" + str(id)) is None:
            addDict = {"material_slot" + str(id): None}
            materialsDict.update(addDict)
    # 原材料字典: 省略的槽位补 None
    newMaterialsDict = __FormSlotDict("material_slot", materialSlotNum,
                                      materialsDict)
    # 原结果字典: 省略的地方补充默认值
    newResultsDict = __FormSlotDict("result_slot", resultSlotNum, resultsDict)
    return {"materials": newMaterialsDict, "results": newResultsDict}


def __FurnaceRecipeAdapter(recipeName,
                           rawRecipeDict,
                           materialSlotNum=1,
                           resultSlotNum=1):
    # type: (str,dict,int,int) -> dict
    """熔炉单个配方调试器:补全数据，自动将配方名转换为原材料"""
    materialsDict = rawRecipeDict.get("materials")
    if materialsDict is None:
        materialsDict = {"material_slot0": {"newItemName": recipeName}}
    resultsDict = rawRecipeDict.get("results")
    if resultsDict is None:
        resultsDict = {"result_slot0": rawRecipeDict}
    newMaterialsDict = __FormSlotDict("material_slot", materialSlotNum,
                                      materialsDict)
    newResultsDict = __FormSlotDict("result_slot", resultSlotNum, resultsDict)
    return {"materials": newMaterialsDict, "results": newResultsDict}


def __FormSlotDict(slotName, slotNum, oriItemDict):
    # type: (str, int, dict) -> dict
    """创建新的原材料或结果字典 {slotName: itemDict}"""
    slotTuple = ["{0}{1}".format(slotName, str(n)) for n in range(slotNum)]
    newItemDict = dict.fromkeys(slotTuple)
    for slotName, itemDict in oriItemDict.items():
        if itemDict is None:
            continue
        newItemDict[slotName] = __FormNewItemDict(itemDict)
    return newItemDict


def __FormNewItemDict(oldItemDict=None, recipeName=None):
    # type: (str,dict) -> dict
    """将原物品字典中省略的部分补充"""
    if oldItemDict is None:
        return {
            "newItemName": recipeName,
            "newAuxValue": 0,
            "count": 1,
        }
    elif isinstance(oldItemDict, str):
        return {
            "newItemName": oldItemDict,
            "newAuxValue": 0,
            "count": 1,
        }
    newItemName = oldItemDict.get("newItemName")
    if newItemName is None:
        logger.error("{0} 中存在丢失 newItemName 的情况".format(recipeName))
    return {
        "newItemName": newItemName,
        "newAuxValue": oldItemDict.get("newAuxName", 0),
        "count": oldItemDict.get("count", 1),
    }
