'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-27 21:10:53
LastEditTime: 2022-08-24 21:49:06
'''
from hammerCookingScripts import logger

FURNACE_LIST = [
    "cookingcraft:baking_furnace", "cookingcraft:mill", "cookingcraft:squeezer",
    "cookingcraft:fryer", "cookingcraft:pan", "cookingcraft:grill",
    "cookingcraft:simple_grill", "cookingcraft:stew_pot",
    "cookingcraft:simple_stew_pot", "cookingcraft:food_steamer"
]
CRAFTING_LIST = ["cookingcraft:cooking_table", "cookingcraft:butcher_table"]


def IsFurnaceBlock(blockName):
    # type: (str) -> bool
    """判断方块是否是熔炉"""
    return blockName in FURNACE_LIST


def IsCraftingBlock(blockName):
    # type: (str) -> bool
    """判断方块是否是工作台"""
    return blockName in CRAFTING_LIST


def IsWorkbenchBlock(blockName):
    return blockName in FURNACE_LIST or blockName in CRAFTING_LIST


def GetMaterialSlotPrefix():
    # type: () -> str
    return "material_slot"


def GetResultSlotPrefix():
    # type: () -> str
    return "result_slot"


def GetFuelSlotPrefix():
    # type: () -> str
    return "fuel_slot"


def GetMaterialSlotIndex(materialSlotName):
    return int(materialSlotName[13:])


def IsMaterialSlot(slotName):
    return False if isinstance(slotName,
                               int) else GetMaterialSlotPrefix() in slotName


def IsFuelSlot(slotName):
    return False if isinstance(slotName,
                               int) else GetFuelSlotPrefix() in slotName


def IsResultSlot(slotName):
    return False if isinstance(slotName,
                               int) else GetResultSlotPrefix() in slotName


def GetFlexibleMaterialsSlotNum(blockName):
    if IsCraftingBlock(blockName):
        return 9
    elif IsFurnaceBlock(blockName):
        return 6 if blockName == "cookingcraft:pan" else GetMaterialsSlotNum(
            blockName)


def GetMaterialsSlotNum(blockName):
    if IsCraftingBlock(blockName):
        return 13
    elif IsFurnaceBlock(blockName):
        if blockName == "cookingcraft:squeezer":
            return 3
        elif blockName == "cookingcraft:pan":
            return 11
        elif blockName in [
                "cookingcraft:stew_pot", "cookingcraft:simple_stew_pot"
        ]:
            return 7
        return 1
    logger.error("获取工作台: {0} 原材料槽错误".format(blockName))


def GetResultsSlotNum(blockName):
    return 2 if blockName == "cookingcraft:mill" else 1


def HaveFlexibleMaterialSlot(blockName):
    return bool(IsCraftingBlock(blockName) or blockName == "cookingcraft:pan")
