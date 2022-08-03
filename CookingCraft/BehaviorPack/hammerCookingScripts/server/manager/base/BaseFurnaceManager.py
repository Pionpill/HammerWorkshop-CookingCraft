'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-26 16:32:09
LastEditTime: 2022-08-02 21:19:35
'''
from copy import deepcopy

from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.server.manager.base.BaseWorkbenchManager import \
    BaseWorkbenchManager
from hammerCookingScripts.common.utils import workbenchUtils


class BaseFurnaceManager(BaseWorkbenchManager):
    def __init__(self, blockName):
        BaseWorkbenchManager.__init__(self, blockName)
        self.fuelSlotPrefix = workbenchUtils.GetFuelSlotPrefix()
        self.slotNum = {
            self.materialSlotPrefix: self.proxy.GetMaterialsSlotNum(),
            self.resultSlotPrefix: self.proxy.GetResultsSlotNum(),
            self.fuelSlotPrefix: self.proxy.GetFuelsSlotNum()
        }
        self.fuelsItems = {
            self.fuelSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.fuelSlotPrefix))
        }
        self.UIInit = False
        self.burnInterval = modConfig.BURN_INTERVAL * 20
        self.burnTime = 0  # 剩余可燃烧时间，单位 tick
        self.burnDuration = 0  # 可燃烧总时间，单位 tick
        self.producingProgress = 0

    def ConvertFromBlockEntityData(self, entityDict):
        # type: (dict) -> None
        """将 BlockEntity 各槽位的数据存入管理类"""
        for slotName, itemDict in entityDict:
            self._ConvertToItemData(slotName, itemDict)

    def ConvertToBlockEntityData(self):
        # type: () -> dict
        """将管理类的数据转换为 BlockEntityData 数据"""
        blockEntityDict = deepcopy(self.materialsItems)
        blockEntityDict.update(self.fuelsItems)
        blockEntityDict.update(self.resultsItems)
        return blockEntityDict

    def UpdateItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """更新方块的物品数据"""
        self._ConvertToItemData(slotName, itemDict)

    def CanSlotSet(self, *slotName):
        # type: (str) -> bool
        """判断槽位是否可以放置物品"""
        return all(
            slot.startswith(self.materialSlotPrefix)
            or slot.startswith(self.fuelSlotPrefix) for slot in slotName)

    def Tick(self):
        # type: () -> bool
        """管理类 tick，如果需要更新 UI 返回 True"""
        shouldRefresh = False
        lastBurn = self.IsBurning()
        if self.IsBurning():
            self.burnTime -= 1
        # 可烧炼且燃烧时间为0时尝试 消耗燃料获取燃烧时间
        if self.burnTime == 0 and self._CanProduce():
            shouldRefresh = self.__BurnNewFuel()
        # 燃烧中并且可烧炼增加烧炼进度
        if self.IsProducing():
            self.producingProgress += 1
            if self.producingProgress == self.burnInterval:
                self.Produce()
                shouldRefresh = True
        elif self.producingProgress > 0:
            shouldRefresh = True
            self.producingProgress = 0
        if lastBurn != self.IsBurning():
            shouldRefresh = True
        return shouldRefresh

    def IsBurning(self):
        # type: () -> bool
        """判断是否在燃烧"""
        return self.burnTime > 0

    def GetUIBurnProgress(self):
        # type: () -> int
        """计算客户端 UI 的 burnProgress"""
        return int((self.burnDuration - self.burnTime) * 3 / 2)

    def GetUIProducingProgress(self):
        """计算客户端 UI 的 cookingProgress
        """
        return int(self.producingProgress * 3 / 2)

    def IsUIInit(self):
        # type: () -> bool
        """判断 UI 是否已初始化"""
        return self.UIInit

    def UIInit(self):
        # type: () -> None
        """打开 UI: 记录 UI 已经被开启过"""
        self.UIInit = True

    def IsProducing(self):
        # type: () -> bool
        """是否正在生产物品"""
        return self.IsBurning() and self._CanProduce()

    def __BurnNewFuel(self):
        # type: () -> bool
        """Tick: 燃烧燃料"""
        shouldRefresh = False
        keyName, self.burnTime = self.GetFuelBurnDuration()
        self.burnDuration = self.burnTime
        if self.IsBurning():
            self._ItemReduce(keyName)
            shouldRefresh = True
        return shouldRefresh

    def GetFuelBurnDuration(self):  # sourcery skip: use-named-expression
        # type: () -> tuple
        """遍历 fuelsItems 获取燃料可燃烧 tick 数 (keyName: str, duration: int)"""
        for i in range(self.slotNum.get(self.fuelSlotPrefix)):
            keyName = self.fuelSlotPrefix + str(i)
            itemDict = self.fuelsItems.get(keyName)
            if itemDict:
                itemName = itemDict.get("newItemName")
                return (keyName, self.proxy.GetBurnDuration(itemName))

    def _ConvertToItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """
        更新方块的物品数据
        仅提取 prefix 符合的数据
        """
        slotPrefix = self._GetSlotPrefix(slotName)
        if slotPrefix == self.materialSlotPrefix:
            self.materialsItems[slotName] = itemDict
        elif slotPrefix == self.fuelSlotPrefix:
            self.fuelsItems[slotName] = itemDict
        elif slotPrefix == self.resultSlotPrefix:
            self.resultsItems[slotName] = itemDict
        else:
            logger.info("不存在该槽位前缀名: {0}".format(slotPrefix))
            return

    def _ItemReduce(self, slotName, count=1):
        # type: (str,int) -> None
        """管理类物品数据自减，默认自减1"""
        slotPrefix = self._GetSlotPrefix(slotName)
        if slotPrefix == self.materialSlotPrefix:
            itemDict = self.materialsItems
        elif slotPrefix == self.fuelSlotPrefix:
            itemDict = self.fuelsItems
        elif slotPrefix == self.resultSlotPrefix:
            itemDict = self.resultsItems
        else:
            raise KeyError
        if itemDict[slotName]["count"] >= count:
            itemDict[slotName]["count"] -= count
            if itemDict[slotName]["count"] == 0:
                itemDict[slotName] = None
        else:
            logger.debug("{0} 数量不足以自减 {1}".format(slotName, count))
