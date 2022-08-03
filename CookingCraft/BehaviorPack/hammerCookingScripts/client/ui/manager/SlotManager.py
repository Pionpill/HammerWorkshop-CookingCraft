'''
Description: 槽管理，专用于 UI 中的物品槽
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-02 19:57:53
LastEditTime: 2022-08-03 00:54:18
'''
# -*- coding:utf-8 -*-
from hammerCookingScripts import logger
from hammerCookingScripts.common.utils import workbenchUtils


class SlotManager(object):
    def __init__(self):
        object.__init__(self)
        # key: slotName (str|int)  value: path, item
        self.__slotsInfo = {}
        # key: path (str) value: slotName
        self.__pathsInfo = {}

    def GetSlotPath(self, slotName):
        # type: (str|int) -> str
        """获取 slot 的UI路径"""
        return self.__GetSlotInfo(slotName).get("path")

    def GetSlotItem(self, **kwargs):
        # type: (dict) -> str
        """获取 slot 对应的物品信息, 键: slotName, slotPath"""
        for key, value in kwargs.values():
            if key.lower() in ["slotname", "name"]:
                return self.__GetSlotInfo(value).get("item")
            if key.lower() in ["slotpath", "path"]:
                slotName = self.GetSlotName(value)
                return self.__GetSlotInfo(slotName).get("item")

    def __GetSlotInfo(self, slotName):
        # type: (str|int) -> dict
        """获取 slot 的信息，包括 slotPath, item 两个键"""
        slotInfo = self.__slotsInfo.get(slotName)
        if slotInfo is None:
            logger.debug("{0} 不存在对应的物品信息或未初始化".format(slotName))
            return
        return slotInfo

    def SetSlotPath(self, slotName, slotPath):
        # sourcery skip: class-extract-method
        # type: (str|int, str) -> None
        """设置 slot 的UI路径"""
        slotInfo = self.__slotsInfo.get(slotName)
        if slotInfo is None:
            self.__slotsInfo[slotName] = {}
        self.__slotsInfo[slotName]["path"] = slotPath
        self.__pathsInfo[slotPath] = slotName

    def SetSlotItem(self, slotName, slotItem):
        # type: (str|int, str) -> None
        """设置 slot 对应的物品信息"""
        slotInfo = self.__slotsInfo.get(slotName)
        if slotInfo is None:
            self.__slotsInfo[slotName] = {}
        self.__slotsInfo[slotName]["item"] = slotItem

    def SetSlotInfo(self, slotName, **kwargs):
        # type: (str|int, dict) -> None
        """设置 slot 的信息, 支持的键: slotPath, slotItem, slotInfo(path, item)"""
        for key, value in kwargs.items():
            if key.lower() in ["slotinfo", "info"]:
                self.SetSlotPath(slotName, value[0])
                self.SetSlotItem(slotName, value[1])
                return
            if key.lower() in ["slotpath", "path"]:
                self.SetSlotPath(slotName, value)
            if key.lower() in ["slotitem", "item"]:
                self.SetSlotItem(slotName, value)

    def GetSlotName(self, slotPath):
        # type: (str) -> str|int
        """根据 UI 路径获取 slotName"""
        return self.__pathsInfo.get(slotPath)

    def GetAllSlotPath(self):
        return [
            self.GetSlotPath(slotName) for slotName in self.__slotsInfo.keys()
        ]

    def GetAllSlotPathButResult(self):
        return self.GetAllInventorySlotPath() + self.GetAllMaterialSlotPath(
        ) + self.GetAllFuelSlotPath()

    def GetAllInventorySlotPath(self):
        return [
            self.GetSlotPath(slotName) for slotName in self.__slotsInfo.keys()
            if isinstance(slotName, int)
        ]

    def GetAllMaterialSlotPath(self):
        return [
            self.GetSlotPath(slotName) for slotName in self.__slotsInfo.keys()
            if not isinstance(slotName, int)
            and workbenchUtils.GetMaterialSlotPrefix() in slotName
        ]

    def GetAllResultSlotPath(self):
        return [
            self.GetSlotPath(slotName) for slotName in self.__slotsInfo.keys()
            if not isinstance(slotName, int)
            and workbenchUtils.GetResultSlotPrefix() in slotName
        ]

    def GetAllFuelSlotPath(self):
        return [
            self.GetSlotPath(slotName) for slotName in self.__slotsInfo.keys()
            if not isinstance(slotName, int)
            and workbenchUtils.GetFuelSlotPrefix() in slotName
        ]

    def __str__(self):
        return self.__pathsInfo.__str__()


if __name__ == "__main__":
    testManager = SlotManager()
    testManager.SetSlotInfo("result_slot0", info=("d:/", "1"))
    testManager.SetSlotInfo("material_slot1", info=("d:/1", "2"))
    testManager.SetSlotInfo(3, info=("d:/2", "3"))
    print(testManager.GetSlotName("d:/1"))
