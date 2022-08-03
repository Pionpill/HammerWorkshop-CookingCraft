'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-27 21:10:53
LastEditTime: 2022-08-03 00:45:02
'''
from hammerCookingScripts import logger

FURNACE_LIST = ["cookingcraft:baking_furnace"]
CRAFTING_LIST = ["cookingcraft:cooking_table"]


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


def IsMaterialSlot(slotName):
    return GetMaterialSlotPrefix() in slotName


def IsFuelSlot(slotName):
    return GetFuelSlotPrefix() in slotName


def IsResultSlot(slotName):
    return GetResultSlotPrefix() in slotName
