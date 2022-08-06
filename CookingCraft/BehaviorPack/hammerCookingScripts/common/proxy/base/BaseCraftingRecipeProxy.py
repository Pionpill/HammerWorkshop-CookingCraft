'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-21 23:40:29
LastEditTime: 2022-08-06 13:56:48
'''
from hammerCookingScripts.common.proxy.base.BaseRecipeProxy import \
    BaseRecipeProxy
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils


class BaseCraftingRecipeProxy(BaseRecipeProxy):
    def __init__(self, recipes):
        BaseRecipeProxy.__init__(self, recipes)

    def GetMaterialsSlotNum(self):
        # type: () -> int
        """默认 9 个原材料槽，子类可以重写"""
        return 9

    def GetResultsSlotNum(self):
        # type: () -> int
        """默认 1 个产品槽，子类可以重写"""
        return 1

    def GetLastUsedRecipeMaterials(self):
        if self._lastUsedRecipeName:
            return self._GetRecipeMaterials(self._lastUsedRecipeName)
        return None

    def MatchRecipe(self, blockItems, matchNum=9):
        # type: (dict, int) -> dict
        """匹配配方，返回配方结果; 默认匹配 9 次"""
        for recipeName in self._recipe.GetAllRecipeName():
            materials = self._GetRecipeMaterials(recipeName)
            matchCount = 0
            for slotName, materialItem in materials.items():
                matchCount += 1
                blockItem = blockItems.get(slotName)
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
