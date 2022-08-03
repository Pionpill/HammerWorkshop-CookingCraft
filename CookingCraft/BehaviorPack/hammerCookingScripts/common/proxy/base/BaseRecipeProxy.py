'''
Description: 配方的基类，所有配方都必须拥有原材料(materials)，结果(results) 键
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-21 23:26:14
LastEditTime: 2022-08-02 21:20:22
'''
from abc import abstractmethod
from hammerCookingScripts.common.entity import Recipe


class BaseRecipeProxy(object):
    def __init__(self, recipes):
        # type: (dict) -> None
        """传入配方字典与对应的调试器"""
        object.__init__(self)
        self._recipe = Recipe(recipes)
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
        # type: (dict, dict) -> bool
        """比较两个配方物品是否相同"""
        if not recipeItem and not blockItem:
            return True
        if not recipeItem or not blockItem:
            return False
        if recipeItem.get("newItemName") != blockItem.get("newItemName"):
            return False
        if recipeItem.get("newAuxValue") != blockItem.get("newAuxValue"):
            return False
        if recipeItem.get("count") < blockItem.get("count"):
            return False
        return True

    @abstractmethod
    def GetMaterialsSlotNum(self):
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def GetResultsSlotNum(self):
        # type: () -> int
        raise NotImplementedError

    @abstractmethod
    def MatchRecipe(self, blockItems, matchNum=1):
        # type: (dict, int) -> dict
        """通过方块 UI 界面的物品匹配合成物"""
        raise NotImplementedError
