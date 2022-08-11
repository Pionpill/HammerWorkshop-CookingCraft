'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 16:58:49
LastEditTime: 2022-08-11 16:22:43
'''
from hammerCookingScripts.common.data.recipe import bakingRecipes, cookingRecipes, millRecipes
from hammerCookingScripts.common.entity.adapter import recipeAdapter
from hammerCookingScripts import logger


class Recipe(object):

    def __init__(self, recipes):
        # type: (dict) -> None
        object.__init__(self)
        self.__recipes = recipes
        self.__InitRecipeAdapter()

    def __InitRecipeAdapter(self):
        if self.__recipes == bakingRecipes:
            self.__recipeAdapter = recipeAdapter.BakingFurnaceRecipeAdapter
        elif self.__recipes == cookingRecipes:
            self.__recipeAdapter = recipeAdapter.CookingTableRecipeAdapter
        elif self.__recipes == millRecipes:
            self.__recipeAdapter = recipeAdapter.MillRecipeAdapter
        else:
            logger.error("{0} 没有对应的转换器".format(self.__recipes))

    def __GetRecipe(self, recipeName):  # sourcery skip: use-named-expression
        # type: (str) -> dict
        """根据配方名获取配方字典, 并转换为 materials: xx results:xx 格式"""
        rawRecipe = self.__recipes.get(recipeName)
        if rawRecipe:
            return self.__recipeAdapter(recipeName, rawRecipe)
        return

    def GetRecipeResults(self, recipeName):
        # type: (dict) -> dict
        """根据配方名获取配方结果"""
        if self.__GetRecipe(recipeName) is None:
            return
        return self.__GetRecipe(recipeName).get("results", None)

    def GetRecipeMaterials(self, recipeName):
        # type: (str) -> dict
        """根据配方名获取配方原材料"""
        if self.__GetRecipe(recipeName) is None:
            return
        return self.__GetRecipe(recipeName).get("materials", None)

    def GetAllRecipeName(self):
        # type: () -> list
        return self.__recipes.keys()
