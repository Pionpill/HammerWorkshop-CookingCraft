'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-28 12:49:47
LastEditTime: 2022-05-25 22:25:08
'''
from hammerCookingScripts.server.serverManager.WorkbenchMgrBase import WorkbenchMgrBase
from hammerCookingScripts.common.commonManager.CookingRecipeMgr import CookingRecipeManager
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger


class CookingTableManager(WorkbenchMgrBase):
    def __init__(self):
        WorkbenchMgrBase.__init__(self)
        self.materialSlotNumList = list(range(9))
        self.outSlotNumList = [9]
        self.blockName = modConfig.CookingTable_Block_Name
        self.cookingRecipeMgr = CookingRecipeManager()
        self.items = [
            None, None, None, None, None, None, None, None, None, None
        ]

    def GetMaterialSlotNum(self):
        """获取原料槽的数量"""
        return 9

    def Tick(self):
        """cookingTable 并没有需要 tick 的事件

        Returns:
            bool: 无 tick 事件
        """
        return False

    def CanSet(self, slotName, item):
        """判断 UI 能否放置 Item

        Args:
            slotName (str): 带前缀的 slot 名
            
        Returns:
            bool: 布尔值
        """
        # 原料槽可放置
        if self.IsOutSlot(slotName):
            return False
        return True

    def GetStateData(self):
        """厨务台并没有状态信息"""
        return None

    def GetRecipeResult(self, blockItems):
        """获取合成结果

        Args:
            blockItems (dict): 9个原料槽的物品信息，key: slotName value: itemDict

        Returns:
            dict: key: slotName value: itemDict
        """
        resultItem = self.cookingRecipeMgr.GetResult(blockItems)
        if not resultItem:
            self.items[9] = None
            return {"crafting_slot9": None}
        self.items[9] = resultItem
        return {"crafting_slot9": resultItem}

    def HandleGetResult(self):
        """更新获取结果槽物品后 self.items 信息

        Returns:
            dict: blockItems: key: slotName  value: itemDict
        """
        newItems = self.GetBlockItems()
        lastUsedRecipe = self.cookingRecipeMgr.GetLastUsedRecipe()
        if lastUsedRecipe:
            for slotName, recipeItemDict in lastUsedRecipe.items():
                if recipeItemDict is None:
                    continue
                slotNum = self.GetSlot(slotName)
                recipeItemCount = recipeItemDict.get("count")
                if not newItems[slotNum]:
                    break
                selfItemCount = newItems[slotNum].get("count")
                if recipeItemCount > selfItemCount:
                    break
                if recipeItemCount == selfItemCount:
                    newItems[slotNum] = None
                else:
                    newItems[slotNum]["count"] = selfItemCount - recipeItemCount
        newItems[9] = None
        blockItems = {}
        index = 0
        for itemDict in self.items:
            blockItems["crafting_slot" + (str)(index)] = itemDict
            index += 1
        return blockItems
