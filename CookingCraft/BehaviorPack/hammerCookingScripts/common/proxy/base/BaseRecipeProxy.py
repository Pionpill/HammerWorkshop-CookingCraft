'''
Description: 配方的基类，所有配方都必须拥有原材料(materials)，结果(results) 键
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-21 23:26:14
LastEditTime: 2022-08-25 13:25:36
'''
from abc import abstractmethod
from hammerCookingScripts import logger
from hammerCookingScripts.common.entity import Recipe
from hammerCookingScripts.common.utils import workbenchUtils
from hammerCookingScripts.common.data.recipe import *


class BaseRecipeProxy(object):

    def __init__(self, blockName):
        # type: (dict, str) -> None
        """传入配方字典与对应的调试器"""
        object.__init__(self)
        self._blockName = blockName
        if blockName == "cookingcraft:cooking_table":
            self._recipe = Recipe(cookingRecipes)
        elif blockName == "cookingcraft:butcher_table":
            self._recipe = Recipe(butcherRecipes)
        elif blockName == "cookingcraft:baking_furnace":
            self._recipe = Recipe(bakingRecipes)
        elif blockName == "cookingcraft:fryer":
            self._recipe = Recipe(fryerRecipes)
        elif blockName in ["cookingcraft:grill", "cookingcraft:simple_grill"]:
            self._recipe = Recipe(grillRecipes)
        elif blockName == "cookingcraft:mill":
            self._recipe = Recipe(millRecipes)
        elif blockName == "cookingcraft:pan":
            self._recipe = Recipe(panRecipes)
        elif blockName == "cookingcraft:squeezer":
            self._recipe = Recipe(squeezerRecipes)
        elif blockName == "cookingcraft:food_steamer":
            self._recipe = Recipe(steamerRecipes)
        elif blockName in [
                "cookingcraft:stew_pot", "cookingcraft:simple_stew_pot"
        ]:
            self._recipe = Recipe(stewRecipes)
        self._lastUsedRecipeName = None

    def _GetRecipeResults(self, recipeName):
        # type: (dict) -> dict
        """根据配方名获取配方结果"""
        return self._recipe.GetRecipeResults(recipeName)

    def _GetRecipeMaterials(self, recipeName):
        # type: (str) -> dict
        """根据配方名获取配方原材料"""
        return self._recipe.GetRecipeMaterials(recipeName)

    def GetLastUsedRecipeMaterials(self):
        # type: () -> dict
        if self._lastUsedRecipeName:
            return self._GetRecipeMaterials(self._lastUsedRecipeName)
        return None

    def GetLastUsedRecipeResults(self):
        # type: () -> dict
        if self._lastUsedRecipeName:
            return self._GetRecipeResults(self._lastUsedRecipeName)
        return None

    def _IsSameMaterialItem(self, recipeItem, blockItem):
        """比较两个配方物品是否相同"""
        if not recipeItem and not blockItem:
            return True
        if not recipeItem or not blockItem:
            return False
        if recipeItem.get("newItemName") != blockItem.get("newItemName"):
            return False
        if recipeItem.get("newAuxValue") != blockItem.get("newAuxValue"):
            return False
        return recipeItem.get("count") >= blockItem.get("count")

    def MatchRecipe(self, blockItems):
        # type: (dict, int) -> dict
        """获取配方结果，默认的只有一个材料槽，如果有多个原材料槽需要重写该方法"""
        matchNum = workbenchUtils.GetMaterialsSlotNum(self._blockName)
        for recipeName in self._recipe.GetAllRecipeName():
            materials = self._GetRecipeMaterials(recipeName)
            matchCount = 0
            flexibleSlotNum = workbenchUtils.GetFlexibleMaterialsSlotNum(
                self._blockName)
            for slotName, materialItem in materials.items():
                matchCount += 1
                blockItem = blockItems.get(slotName)
                if workbenchUtils.GetMaterialSlotIndex(
                        slotName) >= flexibleSlotNum and materialItem is None:
                    if matchCount == matchNum:
                        self._lastUsedRecipeName = recipeName
                        return self._GetRecipeResults(recipeName)
                    continue
                if not self._IsSameMaterialItem(blockItem, materialItem):
                    break
                if matchCount == matchNum:
                    self._lastUsedRecipeName = recipeName
                    return self._GetRecipeResults(recipeName)
        self._lastUsedRecipeName = None
        return {
            workbenchUtils.GetResultSlotPrefix() + str(id): None
            for id in range(self.GetResultsSlotNum())
        }

    @abstractmethod
    def GetMaterialsSlotNum(self):
        # type: () -> int
        return workbenchUtils.GetMaterialsSlotNum(self._blockName)

    @abstractmethod
    def GetResultsSlotNum(self):
        # type: () -> int
        return workbenchUtils.GetResultsSlotNum(self._blockName)
