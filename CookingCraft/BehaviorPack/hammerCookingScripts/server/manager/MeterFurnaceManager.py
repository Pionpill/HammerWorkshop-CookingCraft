'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-25 00:04:11
LastEditTime: 2022-08-25 18:25:53
'''
from copy import deepcopy

from hammerCookingScripts.server.manager import FurnaceManager
from hammerCookingScripts import logger


class MeterFurnaceManager(FurnaceManager):

    def __init__(self, blockName):
        FurnaceManager.__init__(self, blockName)
        self.meterItems = {
            "meter_material_slot": None,
            "meter_result_slot": None
        }
        self.liquidAmount = 0
        if blockName in ["cookingcraft:fryer"]:
            self.liquidType = "oil"
        elif blockName in [
                "cookingcraft:stew_pot", "cookingcraft:simple_stew_pot",
                "cookingcraft:food_steamer"
        ]:
            self.liquidType = "water"

    def GetLiquidAmount(self):
        return self.liquidAmount

    def GetAllSlotName(self):
        # type: () -> list
        """获取所有槽名，用于作为字典的键"""
        return self.materialsItems.keys() + self.resultsItems.keys(
        ) + self.fuelsItems.keys() + self.meterItems.keys()

    def ConvertToSlotData(self):
        # type: () -> dict
        """将管理类的数据转换为 dict 数据"""
        slotData = deepcopy(self.materialsItems)
        slotData.update(self.fuelsItems)
        slotData.update(self.resultsItems)
        slotData.update(self.meterItems)
        slotData.update({"liquidAmount": self.liquidAmount})
        return slotData

    def Tick(self):
        # type: () -> bool
        """管理类 tick，如果需要更新 UI 返回 True"""
        shouldRefresh = False
        lastBurn = self.IsBurning()
        if self.IsBurning():
            self.burnTime -= 1
        # 可烧炼且燃烧时间为0时尝试 消耗燃料获取燃烧时间
        if self.burnTime == 0 and self._CanProduce():
            shouldRefresh = self._BurnNewFuel()
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
        if self.__MeterAdd():
            shouldRefresh = True
        return shouldRefresh

    def Produce(self):
        FurnaceManager.Produce(self)
        self.liquidAmount -= 1

    def _CanProduce(self):
        return False if self.liquidAmount == 0 else FurnaceManager._CanProduce(
            self)

    def __MeterAdd(self):
        # type: () -> bool
        """计量器添加液体"""
        meterMaterialItem = self.meterItems.get("meter_material_slot")
        meterResultItem = self.meterItems.get("meter_result_slot")
        if not meterMaterialItem or meterMaterialItem.get("count") == 0:
            return False
        if self.liquidType == "oil":
            return self.__OilMeterAdd()
        elif self.liquidType == "water" and (
                meterResultItem is None
                or meterResultItem.get("newItemName") == "minecraft:bucket"):
            return self.__WaterMeterAdd()

    def __WaterMeterAdd(self):
        meterMaterialItem = self.meterItems.get("meter_material_slot")
        meterMaterialItemName = meterMaterialItem.get("newItemName")
        if meterMaterialItemName != "minecraft:water_bucket":
            return False

        meterResultItem = self.meterItems.get("meter_result_slot")
        resultCount = 0 if meterResultItem is None else meterResultItem.get(
            "count")
        bucketItem = {
            "newItemName": "minecraft:bucket",
            "count": resultCount,
            "newAuxValue": 0
        }
        if self.liquidAmount <= 90 and meterMaterialItem.get(
                "count") >= 1 and resultCount < 16:
            meterMaterialItem["count"] -= 1
            if meterMaterialItem["count"] == 0:
                self.meterItems["meter_material_slot"] = None
            bucketItem["count"] += 1
            self.meterItems["meter_result_slot"] = bucketItem
            self.liquidAmount += 10
            return True
        return False

    def __OilMeterAdd(self):
        meterMaterialItem = self.meterItems.get("meter_material_slot")
        meterMaterialItemName = meterMaterialItem.get("newItemName")
        meterMaterialCount = meterMaterialItem.get("count")
        if meterMaterialItemName != "cookingcraft:food_oil":
            return False
        maxConsumeAmount = 100 - self.liquidAmount
        if meterMaterialCount > maxConsumeAmount:
            meterMaterialItem[
                "count"] = meterMaterialItem["count"] - maxConsumeAmount
            self.liquidAmount = self.liquidAmount + maxConsumeAmount
        elif meterMaterialCount == maxConsumeAmount:
            meterMaterialItem["count"] = 0
            self.liquidAmount = self.liquidAmount + maxConsumeAmount
        else:
            self.meterItems["meter_material_slot"] = None
            self.liquidAmount = self.liquidAmount + meterMaterialCount
        return True

    def ConvertFromBlockEntityData(self, entityDict):
        # type: (dict) -> None
        """将 BlockEntity 各槽位的数据存入管理类"""
        if entityDict:
            for slotName in self.GetAllSlotName():
                self._ConvertToItemData(slotName, entityDict[slotName])
            entityLiquidAmount = entityDict["liquidAmount"]
            if entityLiquidAmount:
                self.liquidAmount = entityLiquidAmount

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
        elif slotPrefix == "meter_material_slot":
            self.meterItems[slotName] = itemDict
        elif slotPrefix == "meter_result_slot":
            self.meterItems[slotName] = itemDict
        else:
            logger.info("不存在该槽位前缀名: {0}".format(slotPrefix))
            return

    def CanSlotSet(self, *slotName):
        # type: (str) -> bool
        """判断槽位是否可以放置物品"""
        return all(
            isinstance(slot, int) or slot.startswith(self.materialSlotPrefix)
            or slot.startswith(self.fuelSlotPrefix) or slot.startswith("meter")
            for slot in slotName)
