'''
Description: 工作台基类，定义一些基础通用的方法
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 22:40:39
LastEditTime: 2022-08-25 18:22:23
'''
from abc import abstractmethod
from copy import deepcopy

from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.common.facade import WorkbenchFacade
from hammerCookingScripts.common.utils import itemUtils, workbenchUtils


class BaseWorkbenchManager(object):

    def __init__(self, blockName):
        object.__init__(self)
        self._blockName = blockName
        self.proxy = WorkbenchFacade.GetWorkbenchProxy(self._blockName)

        self.materialSlotPrefix = workbenchUtils.GetMaterialSlotPrefix()
        self.resultSlotPrefix = workbenchUtils.GetResultSlotPrefix()
        self.slotNum = {
            self.materialSlotPrefix: self.proxy.GetMaterialsSlotNum(),
            self.resultSlotPrefix: self.proxy.GetResultsSlotNum()
        }
        self.materialsItems = {
            self.materialSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.materialSlotPrefix))
        }
        self.resultsItems = {
            self.resultSlotPrefix + str(i): None
            for i in range(self.slotNum.get(self.resultSlotPrefix))
        }
        self.dataInit = False  # 第一次创建管理类需要初始化数据

    def IsDataInit(self):
        # type: () -> bool
        """判断数据是否已初始化"""
        return self.dataInit

    def DataInit(self, blockEntityData):
        self.ConvertFromBlockEntityData(blockEntityData)
        self.dataInit = True

    def GetBlockName(self):
        # type: () -> str
        """获取方块名"""
        return self._blockName

    @abstractmethod
    def Tick(self):
        # type: () -> bool
        """管理类 tick，如果需要更新 UI 返回 True"""
        raise NotImplementedError

    @abstractmethod
    def CanSlotSet(self, slotName):
        # type: (str) -> bool
        """判断槽位是否可以放置物品"""
        raise NotImplementedError

    def ConvertFromBlockEntityData(self, entityDict):
        # type: (dict) -> None
        """将 BlockEntity 各槽位的数据存入管理类"""
        if entityDict:
            for slotName in self.GetAllSlotName():
                self._ConvertToItemData(slotName, entityDict[slotName])

    @abstractmethod
    def UpdateItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """更新方块的物品数据"""

    @abstractmethod
    def ConvertToSlotData(self):
        # type: () -> dict
        """将管理类的数据转换为 BlockEntityData 数据"""
        raise NotImplementedError

    @abstractmethod
    def GetAllSlotName(self):
        # type: () -> list
        """获取所有槽名，用于作为字典的键"""
        raise NotImplementedError

    @abstractmethod
    def _ConvertToItemData(self, slotName, itemDict):
        # type: (str,dict) -> None
        """
        更新方块的物品数据
        仅提取 prefix 符合的数据
        """
        raise NotImplementedError

    def _IsEmptySlotDict(self, slotDict):
        # type: (dict) -> bool
        """判断槽位字典中是否有物品"""
        return all(itemDict is None for _, itemDict in slotDict.items())

    def _GetSlotPrefix(self, slotName):
        # type: (str) -> tuple
        """获取槽的前缀名"""
        count = 0
        for char in slotName:
            if char in "0123456789":
                break
            count += 1
        return slotName[:count]

    def _CanProduce(self):
        """
        判断是否可以生产:
        存在原材料 and 存在原材料对应的配方 and 生成槽没可以增加物品
        """
        if not self.materialsItems:
            return False
        recipeResultsItems = self.proxy.MatchRecipe(self.materialsItems)
        return bool(not self.resultsItems or
                    self.__CanResultsSlotAdd()) if recipeResultsItems else False

    def _ItemReduce(self, slotName, count=1):
        # type: (str,int) -> None
        """管理类物品数据自减，默认自减1"""
        slotPrefix = self._GetSlotPrefix(slotName)
        if slotPrefix == self.materialSlotPrefix:
            itemDict = self.materialsItems
        elif slotPrefix == self.resultSlotPrefix:
            itemDict = self.resultsItems
        else:
            raise KeyError
        item = itemDict[slotName]
        if not item:
            return
        if item["count"] >= count:
            item["count"] -= count
            if item["count"] == 0:
                item = None
        else:
            logger.debug("{0} 数量不足以自减 {1}".format(slotName, count))

    def Produce(self):
        # type: () -> None
        """
        消耗原材料产生生成物
        仅判断原料槽与生成槽，如果是 furnace 需要格外判断燃料槽
        修改 self.materialsItems 和 self.resultsItems
        """
        self.producingProgress = 0
        if not self._CanProduce():
            return
        self._ConsumeMaterialsItems()
        self._ProduceResultsItems()

    def __CanResultsSlotAdd(self):
        # type: () -> bool
        """判断产物是否能添加到结果槽"""
        recipeResultsItems = self.proxy.GetLastUsedRecipeResults()
        if not recipeResultsItems:
            return False
        for slotName, itemDict in recipeResultsItems.items():
            resultsItem = self.resultsItems.get(slotName)
            if resultsItem and not itemUtils.IsSameItem(resultsItem, itemDict):
                return False
        # 判断结果槽物品是否到达上限
        for slotName, itemDict in self.resultsItems.items():
            if itemDict is None:
                continue
            if itemDict.get("count") >= recipeResultsItems.get(slotName).get(
                    "maxStackSize", modConfig.MAX_STACK_SIZE):
                return False
        return True

    def _ConsumeMaterialsItems(self):
        # type: () -> None
        """原材料表物品消耗"""
        recipeMaterialsItems = self.proxy.GetLastUsedRecipeMaterials()
        if recipeMaterialsItems is None:
            return
        for slotName, itemDict in recipeMaterialsItems.items():
            if itemDict is None:
                continue
            count = itemDict.get("count")
            self._ItemReduce(slotName, count)

    def _ProduceResultsItems(self):
        # type: () -> None
        """将配方生成物添加到 self.resultsItems 中"""
        recipeResultsItems = self.proxy.GetLastUsedRecipeResults()
        for slotName, itemDict in recipeResultsItems.items():
            if not self.resultsItems.get(slotName):
                self.resultsItems[slotName] = itemDict
            else:
                self.resultsItems[slotName]["count"] += 1
