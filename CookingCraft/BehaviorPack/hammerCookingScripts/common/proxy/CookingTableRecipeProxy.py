'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 16:14:17
LastEditTime: 2022-07-31 17:48:33
'''
from hammerCookingScripts.common.data.recipe import cookingRecipes
from hammerCookingScripts.common.proxy.base import BaseCraftingRecipeProxy


class CookingTableRecipeProxy(BaseCraftingRecipeProxy):
    def __init__(self):
        BaseCraftingRecipeProxy.__init__(self, cookingRecipes)

    def MatchRecipe(self, blockItems, matchNum=9):
        # type: (dict, int) -> dict
        """匹配配方，返回配方结果; 默认匹配 9 次"""
        BaseCraftingRecipeProxy.MatchRecipe(blockItems, matchNum)
