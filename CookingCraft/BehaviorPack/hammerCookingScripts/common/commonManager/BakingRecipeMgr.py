'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-18 16:16:04
LastEditTime: 2022-05-22 09:16:57
'''
from hammerCookingScripts.common.commonManager.RecipeMgrBase import RecipeManagerBase
from hammerCookingScripts.common.commonRecipe.bakingRecipes import bakingRecipes, bakingFuel
from hammerCookingScripts import logger


class BakingRecipeManager(RecipeManagerBase):
    def __init__(self):
        RecipeManagerBase.__init__(self)
        self.__recipes = bakingRecipes
        self.__fuel = bakingFuel

    def IsFuelItem(self, item):
        return item in self.__fuel

    def GetResult(self, materials):
        """获取熔炼结果

        Args:
            materials (itemDict): 单个物品字典

        Returns:
            dict: itemDict
        """
        return self.__recipes.get(materials)

    def GetBurnDuration(self, fuelItem):
        """获取燃料燃烧事件

        Args:
            fuelItem (str): 燃料名称

        Returns:
            int: 燃料事件
        """
        return self.__fuel.get(fuelItem, 0) * 20
