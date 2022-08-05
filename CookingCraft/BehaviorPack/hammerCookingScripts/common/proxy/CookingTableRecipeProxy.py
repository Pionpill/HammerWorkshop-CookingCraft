'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 16:14:17
LastEditTime: 2022-08-06 00:36:14
'''
from hammerCookingScripts.common.data.recipe import cookingRecipes
from hammerCookingScripts.common.proxy.base import BaseCraftingRecipeProxy
from hammerCookingScripts import logger


class CookingTableRecipeProxy(BaseCraftingRecipeProxy):
    def __init__(self):
        BaseCraftingRecipeProxy.__init__(self, cookingRecipes)

    def MatchRecipe(self, blockItems, matchNum=9):
        # type: (dict, int) -> dict
        """匹配配方，返回配方结果; 默认匹配 9 次"""
        return BaseCraftingRecipeProxy.MatchRecipe(self, blockItems, matchNum)
