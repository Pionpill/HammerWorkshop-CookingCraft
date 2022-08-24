'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-24 14:54:38
'''

from hammerCookingScripts import logger
from hammerCookingScripts.server.manager.base import BaseCraftingManager


class CraftingManager(BaseCraftingManager):

    def __init__(self, blockName):
        BaseCraftingManager.__init__(self, blockName)

    def Reset(self):
        # type: () -> None
        """厨务台重置时，四个调料原材料槽(9-12)无需重置"""
        for i in range(self.slotNum.get(self.materialSlotPrefix) - 4):
            self.materialsItems[self.materialSlotPrefix + str(i)] = None
        self.resultsItems = {
            self.resultSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.resultSlotPrefix))
        }

    def GetMaterialsItems(self, part=False):
        # type: (bool) -> dict
        """"""
        if not part:
            return super().GetMaterialsItems()
        itemDict = {}
        for i in range(self.slotNum.get(self.materialSlotPrefix) - 4):
            key = self.materialSlotPrefix + str(i)
            itemDict[key] = self.materialsItems.get(key)
        return itemDict
