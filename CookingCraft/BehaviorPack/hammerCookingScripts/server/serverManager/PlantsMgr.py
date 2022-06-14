'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:03:38
LastEditTime: 2022-06-14 14:29:09
'''
import random
import copy
import mod.server.extraServerApi as serverApi
from hammerCookingScripts.common.commonManager.PlantsCommonMgr import PlantsCommonManager
from hammerCookingScripts import logger

compFactory = serverApi.GetEngineCompFactory()


class PlantsManager(object):
    def __init__(self):
        object.__init__(self)

    @classmethod
    def CanPlant(cls, seedName, biomeName, blockName):
        """能否种植，需要满足两个条件: 生态和土地

        Args:
            seedName (str): 农作物种子名
            biomeName (str): 生态名
            blockName (str): 农作物种植的方块名

        Returns:
            bool: 能否种植
        """
        return cls.JudgeBlock(seedName, blockName) and cls.JudgeBiome(
            seedName, biomeName)

    @classmethod
    def CanGrow(cls, plantBlockName, blockPos, dimension, levelId, playerId):
        """判断是否能生长

        Args:
            plantBlockName (str): 正在生长的农作物 block 全称
            blockPos (tuple): (x,y,z)
            dimension (int): 维度编号
            levelId (int): levelId
            playerId (int): playerId

        Returns:
            bool: 能否生长
        """
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(plantBlockName)
        growConditions = PlantsCommonManager.GetPlantGrowthConditions(seedName)
        logger.debug(seedName)
        # 判断光照
        plantLightRequire = growConditions.get("brightness", None)
        if plantLightRequire:
            comp = compFactory.CreateBlockInfo(playerId)
            lightLevel = comp.GetBlockLightLevel(blockPos, dimension)
            if plantLightRequire[
                    0] > lightLevel or lightLevel > plantLightRequire[1]:
                return False
        # 判断天气
        plantWeatherRequire = growConditions.get("weather", None)
        if plantWeatherRequire:
            if plantWeatherRequire == "rain":
                comp = serverApi.GetEngineCompFactory().CreateWeather(levelId)
                isRain = comp.IsRaining()
                if not isRain:
                    return False
            if plantWeatherRequire == "thunder":
                comp = serverApi.GetEngineCompFactory().CreateWeather(levelId)
                isThunder = comp.IsThunder()
                if not isThunder:
                    return False
        # 判断海拔
        plantAltitudeRequire = growConditions.get("altitude", None)
        if plantAltitudeRequire:
            blockAltitude = blockPos[1]
            if plantAltitudeRequire[
                    0] > blockAltitude or blockAltitude > plantAltitudeRequire[
                        1]:
                return False
        # 判断发芽条件
        plantSproutRequire = growConditions.get("sprout", None)
        if plantSproutRequire and PlantsCommonManager.GetPlantStageId(
                plantBlockName) == 0:
            comp = serverApi.GetEngineCompFactory().CreateWeather(levelId)
            if plantSproutRequire == "rain":
                isRaining = comp.IsRaining()
                if not isRaining:
                    return False
            if plantSproutRequire == "thunder":
                isThunder = comp.IsThunder()
                if not isThunder:
                    return False
        # 判断特殊条件
        plantSpecialCondition = growConditions.get("special", None)
        if plantSpecialCondition:
            if not cls.JudgeSpecialGrowCondition(plantSpecialCondition,
                                                 blockPos, levelId, dimension):
                return False
        return True

    @classmethod
    def CanHarvest(cls, blockName):
        """判断多次收获的农作物是否可以收获

        Args:
            blockName (str): 农作物生长 block 全名

        Returns:
            bool: 能否收获
        """
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(blockName)
        if cls.IsMultiHarvestPlant(seedName) and cls.IsHarvestStage(blockName):
            return True
        return False

    @classmethod
    def JudgeBiome(cls, seedName, biomeName):
        """判断生态

        Args:
            seedName (str): 农作物种子名
            biomeName (str): MC 生态名

        Returns:
            bool: 该生态可否种植
        """
        plantBiomeSet = PlantsCommonManager.GetSeedBiomeSet(seedName)
        if plantBiomeSet and biomeName in plantBiomeSet:
            return True
        return False

    @classmethod
    def JudgeBlock(cls, seedName, blockName):
        """判断土地/篱笆

        Args:
            seedName (str): 农作物种子名
            blockName (str): block 名

        Returns:
            bool: 该土地(block)上能否种植
        """
        plantLandList = PlantsCommonManager.GetSeedPlantLandList(seedName)
        if blockName in plantLandList:
            return True
        return False

    @classmethod
    def JudgeSpecialGrowCondition(cls, specialCondition, blockPos, levelId,
                                  dimension):
        """判断特殊的生长条件

        Args:
            specialCondition (dict): 特殊条件
            blockPos (tuple): (x,y,z)
            levelId (int): levelId
            dimension (int): dimension

        Returns:
            bool: 能否生长
        """
        waterDis = specialCondition.get("water", None)
        if waterDis:
            logger.debug("111")
            blockComp = compFactory.CreateBlockInfo(levelId)
            posX, posY, posZ = blockPos
            y = posY
            for x in range(posX - waterDis, posX + waterDis + 1):
                for z in range(posZ - waterDis, posZ + waterDis + 1):
                    blockDic = blockComp.GetBlockNew((x, y, z), dimension)
                    if blockDic.get("name") == "minecraft:water":
                        return True
            return False
        return True

    @staticmethod
    def IsMultiHarvestPlant(seedName):
        """判断植物是否可以多次收获

        Args:
            seedName (str): 种子全名
        """
        harvestCount = PlantsCommonManager.GetPlantHarvestCount(seedName)
        if harvestCount == 1:
            return False
        return True

    @staticmethod
    def IsHarvestStage(blockName):
        """判断是否可以收获：生长到最后一阶段

        Args:
            blockName (str): 农作物生长的 block 名

        Returns:
            bool: 是否可以收获
        """
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(blockName)
        stageCount = PlantsCommonManager.GetPlantStageCount(seedName)
        stageId = PlantsCommonManager.GetPlantStageId(blockName)
        if stageCount == (stageId + 1):
            return True
        return False

    @staticmethod
    def GetPlantLootItem(seedName):
        lootTable = PlantsCommonManager.GetPlantLootTable(seedName)
        try:
            countList = lootTable.get("count", None)
            logger.debug(countList)
        except:
            logger.error("{0} lootTable 的 count 不可以缺失".format(seedName))
        lootItem = copy.deepcopy(lootTable)
        lootItem["count"] = random.randint(countList[0], countList[1])
        return lootItem

    @staticmethod
    def CanChangeStage(plantBlockName, tickCount):
        """判断农作物能否进入下一阶段

        Args:
            plantBlockName (str): 农作物 block 全称
            tickCount (int): 当前通过的 tick 数

        Returns:
            bool: 能否生长到下一 block 状态
        """
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(plantBlockName)
        stageId = PlantsCommonManager.GetPlantStageId(plantBlockName)
        plantTickNum = PlantsCommonManager.GetPlantStageTickNum(
            seedName, stageId)
        if tickCount >= plantTickNum:
            return True
        return False

    @staticmethod
    def IsClimbingPlant(seedName):
        """判断植物是否需要攀藤

        Args:
            seedName (str): 种子全名

        Returns:
            bool: 是否需要攀登
        """
        plantLandList = PlantsCommonManager.GetSeedPlantLandList(seedName)
        if "cookingcraft:fence_post" in plantLandList:
            return True
        return False
