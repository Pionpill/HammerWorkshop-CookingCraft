'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 19:44:58
LastEditTime: 2022-07-19 15:58:13
'''
from copy import deepcopy
from random import randint
from hammerCookingScripts.common.entity import Plant
from hammerCookingScripts.common.utils import plantsUtils
from hammerCookingScripts import logger


class PlantProxy(object):
    def __init__(self, seedName):
        object.__init__(self)
        self.seedName = seedName
        self.plant = Plant(seedName)
        self.stageCount = None
        self.multiPlant = None
        self.lootItem = None

    # tickList
    def GetTickNum(self, stageId):
        # type: (int) -> int
        """获取生长阶段需要 tick 的次数"""
        return self.plant.GetTickList()[stageId]

    def GetStageCount(self):
        # type: () -> int
        """获取植物的生长状态总数"""
        if self.stageCount is None:
            self.stageCount = len(self.plant.GetTickList()) + 1
        return self.stageCount

    def IsLastStage(self, blockName):
        # type: (int) -> bool
        """判断植物是否是最后的生长状态"""
        stageId = plantsUtils.GetStageId(blockName)
        stageCount = self.GetStageCount()
        if stageCount == (stageId + 1):
            return True
        return False

    # harvestCount
    def GetHarvestCount(self):
        # type: () -> int
        """获取植物可收获的次数"""
        return self.plant.GetHarvestCount()

    def IsMultiPlant(self):
        # type: () -> bool
        """判断是否是多次种植植被"""
        if self.multiPlant is None:
            self.multiPlant = self.GetHarvestCount() != 1
        return self.multiPlant

    # harvestBlock
    def GetHarvestBlock(self):
        # type:() -> str/None
        """收获后回到的状态方块名"""
        blockName = self.plant.GetHarvestBlock()
        if blockName is None:
            logger.warn("{0} 不可以多次收获".format(self.seedName))
        return blockName

    # plantLandList
    def JudgeLand(self, blockName):
        # type: (str) -> bool
        """判断土地能否种植"""
        return blockName in self.plant.GetPlantLandList()

    def IsClimbingPlant(self):
        # type: () -> bool
        """判断是否是攀藤植物"""
        plantLandList = self.plant.GetPlantLandList()
        return any(
            plantsUtils.IsFence(plantLand) for plantLand in plantLandList)

    # plantBiome
    def JudgeBiome(self, biomeName):
        # type: (str) -> bool
        """判断生态能够种植"""
        return biomeName in self.plant.GetPlantBiome()

    # brightness
    def JudgeBrightness(self, brightness):
        # sourcery skip: use-named-expression
        # type: (int) -> bool
        """判断光照，如果没有，直接返回 True"""
        rangeTuple = self.plant.GetGrowthBrightness()
        if rangeTuple:
            return rangeTuple[0] <= brightness <= rangeTuple[1]
        return True

    # altitude
    def JudgeAltitude(self, altitude):
        # sourcery skip: use-named-expression
        # type: (int) -> bool
        """判断海拔"""
        rangeTuple = self.plant.GetGrowthAltitude()
        if rangeTuple:
            return rangeTuple[0] <= altitude <= rangeTuple[1]
        return True

    # weather
    def JudgeWeather(self, weatherList):
        # sourcery skip: use-named-expression
        # type: (iter) -> bool
        """判断天气"""
        growthWeather = self.plant.GetGrowthWeather()
        if growthWeather:
            return growthWeather in weatherList
        return True

    # sprout
    def JudgeSprout(self, sproutList):
        # sourcery skip: use-named-expression
        # type: (iter) -> bool
        """判断发芽条件"""
        growthSprout = self.plant.GetGrowthSprout()
        if growthSprout:
            return growthSprout in sproutList
        return True

    # special(growth)
    def GetGrowthSpecial(self):
        # type: () -> dict
        """获取特殊的生长条件"""
        return self.plant.GetGrowthSpecial()

    # special(plant)
    def GetPlantSpecial(self):
        # type: () -> dict
        """获取特殊的种植条件"""
        return self.plant.GetPlantSpecial()

    # lootTable
    def GetLootItem(self):
        # type: () -> dict
        """获取多次收获植被的掉落物"""
        if not self.plant.GetLootTable():
            logger.warn("{0} 没有掉落物表".format(self.seedName))
            return
        if self.lootItem is None:
            countList = self.plant.GetLootItemCount()
            lootItem = deepcopy(self.plant.GetLootTable())
            lootItem["count"] = randint(countList[0], countList[1])
            self.lootItem = lootItem
        return self.lootItem
