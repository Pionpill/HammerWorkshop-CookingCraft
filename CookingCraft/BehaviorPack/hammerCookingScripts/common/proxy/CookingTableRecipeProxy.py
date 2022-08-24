'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 16:14:17
LastEditTime: 2022-08-24 15:13:24
'''
from hammerCookingScripts.common.data.recipe import cookingRecipes
from hammerCookingScripts.common.proxy.base import BaseCraftingRecipeProxy
from hammerCookingScripts.common.utils import workbenchUtils
from hammerCookingScripts import logger


class CookingTableRecipeProxy(BaseCraftingRecipeProxy):

    def __init__(self):
        BaseCraftingRecipeProxy.__init__(self, cookingRecipes)

    def MatchRecipe(self, blockItems, matchNum=13):
        # type: (dict, int) -> dict
        """匹配配方，返回配方结果; 匹配 13 次, 调料槽匹配时特殊处理"""
        for recipeName in self._recipe.GetAllRecipeName():
            materials = self._GetRecipeMaterials(recipeName)
            matchCount = 0
            for slotName, materialItem in materials.items():
                matchCount += 1
                blockItem = blockItems.get(slotName)
                if workbenchUtils.GetMaterialSlotIndex(
                        slotName) > 8 and materialItem is None:
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

    def GetMaterialsSlotNum(self):
        # type: () -> int
        """厨务台有 13 个原料槽"""
        return 13

    def GetResultsSlotNum(self):
        # type: () -> int
        """厨务台有 1 个产品槽"""
        return 1
