'''
Description: 植物系统管理类，负责判断植物的种植，生长等条件
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:03:38
LastEditTime: 2022-07-18 15:54:51
'''
import mod.server.extraServerApi as serverApi
from hammerCookingScripts.common.facade import PlantsFacade
from hammerCookingScripts import logger

compFactory = serverApi.GetEngineCompFactory()
plantsUtils = PlantsFacade.GetPlantsUtils()


class PlantsManager(object):
    def __init__(self):
        object.__init__(self)

    @classmethod
    def CanPlant(cls, seedName, biomeName, blockName):
        # type: (str, str, str) -> bool
        """能否种植，需要满足两个条件: 生态和土地"""
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        return plantProxy.JudgeBiome(biomeName) and cls.JudgePlantLand(
            seedName, blockName)

    @classmethod
    def JudgePlantLand(cls, seedName, blockName):
        # type: (str, str) -> bool
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        return plantProxy.JudgeLand(blockName)

    @classmethod
    def CanTick(cls, blockName, blockPos, dimension, levelId, playerId):
        # type: (str, tuple, int, int, int) -> bool
        """判断是否能进行 Tick"""
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        # 判断光照与海拔
        if not cls.__JudgeBaseGrowCondition(playerId, blockPos, dimension,
                                            plantProxy):
            return False
        # 判断天气与发芽
        if not cls.__JudgeWeatherGrowCondition(levelId, blockName, plantProxy):
            return False
        # 判断特殊生长条件
        if not cls.__JudgeSpecialGrowCondition(blockPos, levelId, dimension,
                                               plantProxy):
            return False
        return True

    @classmethod
    def CanHarvest(cls, blockName, harvestNum=0):
        # type: (str, int) -> bool
        """判断农作物是否可以右键收获"""
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        if seedName is None:
            return False
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        if plantProxy.GetHarvestBlock() and plantProxy.GetHarvestCount(
        ) >= harvestNum and plantProxy.IsLastStage(blockName):
            return True
        return False

    @classmethod
    def GetHarvestBlock(cls, seedName):
        # type: (str) -> dict
        """收获后返回的状态"""
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        blockName = plantProxy.GetHarvestBlock()
        return {"name": blockName, "aux": 0}

    @staticmethod
    def GetNextBlockStageDict(blockName):
        # type: (str) -> dict
        """获取下一状态植株的信息字典"""
        newBlockName = plantsUtils.GetNextStageName(blockName)
        return {"name": newBlockName, "aux": 0}

    @staticmethod
    def GetPlantLootItem(seedName):
        # type: (str) -> dict
        """获取多次收获植物的掉落表"""
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        return plantProxy.GetLootItem()

    @staticmethod
    def CanGrowNextStage(blockName, tickCount):
        # type: (str, int) -> bool
        """判断农作物能否进入下一阶段, 检查 stage 有没有超范围"""
        seedName = plantsUtils.GetSeedNameByStageBlock(blockName)
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        stageId = plantsUtils.GetStageId(blockName)
        plantTickNum = plantProxy.GetTickNum(stageId)
        seedStageCount = plantProxy.GetStageCount()
        return tickCount >= plantTickNum and stageId + 1 <= seedStageCount

    @staticmethod
    def GetPlantFirstStageDict(seedName):
        # type: (str) -> dict
        """根据种子名获取幼苗字典"""
        plantFirstStageName = plantsUtils.GetFirstStageName(seedName)
        return {"name": plantFirstStageName, "aux": 0}

    @staticmethod
    def IsClimbingPlant(seedName):
        # type: (str) -> bool
        """判断植物是否需要攀藤
        """
        if not plantsUtils.IsModSeed(seedName):
            return
        plantProxy = PlantsFacade.GetPlantProxy(seedName)
        return plantProxy.IsClimbingPlant()

    @classmethod
    def __JudgeBaseGrowCondition(cls, playerId, blockPos, dimension,
                                 plantProxy):
        # type: (int, tuple, int, PlantProxy) -> bool
        """ 判断基础生长条件: 光照与海拔 """
        comp = compFactory.CreateBlockInfo(playerId)
        brightness = comp.GetBlockLightLevel(blockPos, dimension)
        if not plantProxy.JudgeBrightness(brightness):
            return False
        blockAltitude = blockPos[1]
        if not plantProxy.JudgeAltitude(blockAltitude):
            return False
        return True

    @classmethod
    def __JudgeWeatherGrowCondition(cls, levelId, blockName, plantProxy):
        # type: (int, str, PlantProxy) -> bool
        """ 判断天气相关生长条件: 天气与发芽 """
        stageId = plantsUtils.GetStageId(blockName)
        comp = serverApi.GetEngineCompFactory().CreateWeather(levelId)
        weatherList = []
        if comp.IsRaining():
            weatherList.append("rain")
        if comp.IsThunder():
            weatherList.append("thunder")
        if not plantProxy.JudgeWeather(weatherList):
            return False
        if stageId == 0 and not plantProxy.JudgeSprout(weatherList):
            return False
        return True

    @classmethod
    def __JudgeSpecialGrowCondition(cls, blockPos, levelId, dimension,
                                    plantProxy):
        # type: (tuple, int, int, PlantProxy) -> bool
        # sourcery skip: use-named-expression
        """ 判断特殊生长条件 """
        specialGrowthCondition = plantProxy.GetGrowthSpecial()
        if not specialGrowthCondition:
            return True
        waterDis = specialGrowthCondition.get("water", None)
        if waterDis and cls.__JudgeWater(waterDis, levelId, blockPos,
                                         dimension):
            return False
        return True

    @classmethod
    def __JudgeWater(cls, waterDis, levelId, blockPos, dimension):
        # type: (int, int, tuple, int) -> bool
        """ 判断特殊生长条件: 水 """
        blockComp = compFactory.CreateBlockInfo(levelId)
        posX, posY, posZ = blockPos
        y = posY
        for x in range(posX - waterDis, posX + waterDis + 1):
            for z in range(posZ - waterDis, posZ + waterDis + 1):
                blockDic = blockComp.GetBlockNew((x, y, z), dimension)
                if blockDic.get("name") == "minecraft:water":
                    return True
        return False
