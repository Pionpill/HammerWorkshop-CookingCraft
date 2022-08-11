'''
Description: 基础炉子配方代理类，基础炉子配方名(recipeName)即为原材料名字(materials)
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-22 16:00:57
LastEditTime: 2022-08-11 17:01:10
'''
from hammerCookingScripts.common.proxy.base.BaseRecipeProxy import \
    BaseRecipeProxy
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils


class BaseFurnaceRecipeProxy(BaseRecipeProxy):

    def __init__(self, recipes, fuelDict):
        BaseRecipeProxy.__init__(self, recipes)
        self._fuelDict = fuelDict

    def GetBurnDuration(self, itemName):
        # type: (str) -> int
        """获取燃料耐久度"""
        if self.__IsFuelItem(itemName):
            return self._fuelDict.get(itemName, 0) * 20

    def GetMaterialsSlotNum(self):
        # type: () -> int
        """烘焙炉有 1 个原料槽"""
        return 1

    def GetResultsSlotNum(self):
        # type: () -> int
        """烘焙炉有 1 个结果槽"""
        return 1

    def GetFuelsSlotNum(self):
        # type: () -> int
        """烘焙炉有 1 个燃料槽"""
        return 1

    def MatchRecipe(self, blockItems, matchNum=1):
        # type: (dict, int) -> dict
        """获取配方结果，默认的只有一个材料槽，如果有多个原材料槽需要重写该方法"""
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

    def __IsFuelItem(self, itemName):
        # type: (str) -> bool
        """判断物品是否是燃料"""
        return itemName in self._fuelDict
