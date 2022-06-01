'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-27 17:25:21
LastEditTime: 2022-05-25 21:51:28
'''

from abc import abstractmethod
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig


class WorkbenchMgrBase(object):
    def __init__(self):
        object.__init__(self)
        self.items = None
        self.materialSlotList = None
        self.outSlotList = None
        self.blockName = None

    def UpdateSlotData(self, slotName, item):
        slot = self.GetSlot(slotName)
        self.items[slot] = item

    def GetBlockName(self):
        return self.blockName

    def UpdateBlockData(self, itemList):
        """更新工作台物品数据

        Args:
            itemList (dict): 物品信息字典
        """
        self.items = itemList

    def GetBlockItems(self):
        return self.items

    def GetSlot(self, slotName):
        """根据槽名获取熔炉槽num

        Args:
            slotName (str): 槽位名，一般为 crafting_slot

        Returns:
            int: 槽位名对应的 num
        """
        if isinstance(slotName, str):
            if not slotName.startswith(
                    modConfig.WORKBENCH_SLOT_PREFIX.get(self.blockName)):
                return -1
            return int(
                slotName[len(modConfig.WORKBENCH_SLOT_PREFIX.get(self.blockName)
                             ):])
        return -1

    @abstractmethod
    def Tick(self):
        """工作台 tick 事件，需要在子类完成

        Returns:
            bool: 有 UI 或者数据需要更新时，返回 True
        """
        return False

    def IsMaterialSlot(self, slotName):
        """判断是否是原材料槽

        Args:
            slotName (str): 带前缀的 slot 名
            
        Returns:
            bool: 布尔值
        """
        slotNum = self.GetSlot(slotName)
        if slotNum in self.materialSlotNumList:
            return True
        return False

    def IsOutSlot(self, slotName):
        """判断是否是输出槽

        Args:
            slotName (str): 带前缀的 slot 名
            
        Returns:
            bool: 布尔值
        """
        slotNum = self.GetSlot(slotName)
        if slotNum in self.outSlotNumList:
            return True
        return False

    @abstractmethod
    def CanSet(self, slotId, item):
        """判断 UI 能否放置 Item

        Args:
            slotId (str): slot 编号
        """
        pass

    @abstractmethod
    def GetStateData(self):
        """获取状态信息

        Returns:
            dict: 除了数据信息以外，如果工作台有状态信息需要传给UI界面更新，应在这里返回
        """
        pass
