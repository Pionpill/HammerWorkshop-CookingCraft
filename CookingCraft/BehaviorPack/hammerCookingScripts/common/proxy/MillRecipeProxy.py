'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-11 15:38:56
LastEditTime: 2022-08-11 16:59:53
'''
from hammerCookingScripts.common.data.recipe import millRecipes, millFuels
from hammerCookingScripts.common.proxy.base import BaseFurnaceRecipeProxy


class MillRecipeProxy(BaseFurnaceRecipeProxy):

    def __init__(self):
        BaseFurnaceRecipeProxy.__init__(self, millRecipes, millFuels)

    def GetResultsSlotNum(self):
        # type: () -> int
        """石磨有 2 个原料槽"""
        return 2
