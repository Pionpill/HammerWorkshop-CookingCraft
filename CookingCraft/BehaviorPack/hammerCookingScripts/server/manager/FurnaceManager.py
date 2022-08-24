'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-24 23:11:16
'''
from hammerCookingScripts.server.manager.base import BaseFurnaceManager
from hammerCookingScripts.common.utils import workbenchUtils


class FurnaceManager(BaseFurnaceManager):

    def __init__(self, blockName):
        BaseFurnaceManager.__init__(self, blockName)

    def GetMaterialsItems(self, part=False):
        # type: (bool) -> dict
        """part 设置为 True 可仅获取非调料槽和碗槽的物品"""
        if not part:
            return super().GetMaterialsItems()
        itemDict = {}
        for i in range(
                workbenchUtils.GetFlexibleMaterialsSlotNum(self._blockName)):
            key = self.materialSlotPrefix + str(i)
            itemDict[key] = self.materialsItems.get(key)
        return itemDict
