'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-18 16:38:05
LastEditTime: 2022-05-25 22:25:05
'''
from hammerCookingScripts.server.serverManager.WorkbenchMgrBase import WorkbenchMgrBase
from hammerCookingScripts.common.commonManager.BakingRecipeMgr import BakingRecipeManager
from hammerCookingScripts.common.commonUtils import itemUtils
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger


class BakingFurnaceManager(WorkbenchMgrBase):
    def __init__(self):
        WorkbenchMgrBase.__init__(self)
        self.bakingRecipeMgr = BakingRecipeManager()
        self.blockName = modConfig.BakingFurnace_Block_Name
        self.materialSlotNumList = [0]
        self.fireSlotNumList = [1]
        self.outSlotNumList = [2]
        self.burnInterval = modConfig.BURN_INTERVAL * 20
        self.items = [None, None, None]
        self.litTime = 0
        self.litDuration = 0
        self.cookingProgress = 0
        self.InitUI = False

    def GetMaterialSlotNum(self):
        return 1

    def Tick(self):
        # 如果有需要更新的UI或者数据时shouldRefresh为True
        shouldRefresh = False
        lastLit = self.IsLit()
        if self.IsLit():
            self.litTime -= 1
        # 可烧炼且燃烧时间为0时尝试消耗燃料获取燃烧时间
        if self.litTime == 0 and self.CanBurn():
            # logger.debug("可烧炼且燃烧时间为0时尝试消耗燃料获取燃烧时间")
            if self.items[1]:
                self.litTime = self.bakingRecipeMgr.GetBurnDuration(
                    self.items[1].get("itemName"))
                self.litDuration = self.litTime
                if self.IsLit():
                    self.items[1]["count"] -= 1
                    if self.items[1]["count"] == 0:
                        self.items[1] = None
                    shouldRefresh = True
        # 燃烧中并且可烧炼增加烧炼进度
        if self.IsCooking():
            self.cookingProgress += 1
            if self.cookingProgress == self.burnInterval:
                self.cookingProgress = 0
                self.Burn()
                shouldRefresh = True
        else:
            if self.cookingProgress > 0:
                shouldRefresh = True
                self.cookingProgress = 0
        if lastLit != self.IsLit():
            shouldRefresh = True
        return shouldRefresh

    def IsLit(self):
        return self.litTime > 0

    def IsCooking(self):
        return self.IsLit() and self.CanBurn()

    def GetLitDuration(self):
        return self.litDuration

    def CanSet(self, slotName, item):
        if self.IsOutSlot(slotName):
            return False
        return True

    def CanBurn(self):
        """判断是否能够烧炼，只有当生成槽没物品或者生成物跟生成槽物品一致且生成槽物品小于最大堆叠数才返回True"""
        if not self.items[0]:
            return False
        resultItem = self.bakingRecipeMgr.GetResult(
            self.items[0].get("itemName"))
        # 配方中没有匹配的生成物返回False
        if not resultItem:
            return False
        # 生成槽为空返回True
        if not self.items[2]:
            return True
        # 生成物与生成槽中物品不是同一个物品返回False
        if not itemUtils.IsSameItem(self.items[2], resultItem):
            return False
        # 生成槽中物品与生成物一致且堆叠数小于最大堆叠数返回True，最大堆叠数在配方中配置，默认为64
        if self.items[2].get("count") < resultItem.get(
                "maxStackSize", modConfig.MAX_STACK_SIZE):
            return True
        return False

    def Burn(self):
        """烧炼过程，消耗原料生成烧炼物"""
        if not self.CanBurn():
            return
        resultItem = self.bakingRecipeMgr.GetResult(
            self.items[0].get("itemName"))
        if not self.items[2]:
            self.items[2] = resultItem
            self.items[2]["count"] = 1
        else:
            self.items[2]["count"] += 1
        self.items[0]["count"] -= 1
        if self.items[0]["count"] == 0:
            self.items[0] = None

    def HandleGetResult(self):
        self.items[2] = None
        blockItems = {}
        index = 0
        for itemDict in self.items:
            blockItems[modConfig.WORKBENCH_SLOT_PREFIX.get(self.blockName) +
                       (str)(index)] = itemDict
            index += 1
        return blockItems

    def CalculateLitProgress(self):
        """计算客户端 UI 的 litProgress

        Returns:
            int: litProgress
        """
        return int((self.litDuration - self.litTime) * 3 / 2)

    def CalculateBurnProgress(self):
        """计算客户端 UI 的 cookingProgress

        Returns:
            int: cookingProgress
        """
        return int(self.cookingProgress * 3 / 2)

    def UIInitCondition(self):
        """返回 UI 初始化情况

        Returns:
            bool: UI 是否已 Init
        """
        return self.InitUI

    def UIInit(self):
        self.InitUI = True
