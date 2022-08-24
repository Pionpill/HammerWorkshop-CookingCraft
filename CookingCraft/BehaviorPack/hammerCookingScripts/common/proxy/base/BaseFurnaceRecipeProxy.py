'''
Description: 基础炉子配方代理类，基础炉子配方名(recipeName)即为原材料名字(materials)
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-22 16:00:57
LastEditTime: 2022-08-24 22:51:20
'''
from hammerCookingScripts.common.proxy.base.BaseRecipeProxy import \
    BaseRecipeProxy
from hammerCookingScripts.common.data.recipe import coalFuels, goldFuels
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils


class BaseFurnaceRecipeProxy(BaseRecipeProxy):

    def __init__(self, blockName):
        BaseRecipeProxy.__init__(self, blockName)
        if blockName in ["cookingcraft:mill", "cookingcraft:squeezer"]:
            self._fuelDict = goldFuels
        else:
            self._fuelDict = coalFuels

    def GetBurnDuration(self, itemName):
        # type: (str) -> int
        """获取燃料耐久度"""
        return self._fuelDict.get(itemName, 0) * 20

    def GetFuelsSlotNum(self):
        # type: () -> int
        """烘焙炉有 1 个燃料槽"""
        return 1
