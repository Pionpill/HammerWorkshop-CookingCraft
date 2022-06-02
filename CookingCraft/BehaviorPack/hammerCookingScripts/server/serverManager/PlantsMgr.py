'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:03:38
LastEditTime: 2022-06-02 12:13:34
'''
'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:03:38
LastEditTime: 2022-05-31 13:05:35
'''
import mod.server.extraServerApi as serverApi
from hammerCookingScripts.common.commonManager.PlantsCommonMgr import PlantsCommonManager
from hammerCookingScripts import logger

compFactory = serverApi.GetEngineCompFactory()


class PlantsManager(object):
    def __init__(self):
        object.__init__(self)

    @classmethod
    def CanPlant(self, seedName, biomeName, landName):
        """能否种植，需要满足两个条件: 生态和土地

        Args:
            seedName (str): 农作物种子名
            biomeName (str): 生态名
            landName (str): 农作物种植的方块名

        Returns:
            bool: 能否种植
        """
        return PlantsCommonManager.JudgeLand(
            seedName, landName) and PlantsCommonManager.JudgeBiome(
                seedName, biomeName)

    @classmethod
    def CanGrow(self, plantBlockName, blockPos, dimension, levelId, playerId):
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
        return True

    @classmethod
    def CanChangeStage(self, plantBlockName, tickCount):
        """判断农作物能否进入下一阶段

        Args:
            plantBlockName (str): 农作物 block 全称
            tickCount (int): 当前通过的 tick 数

        Returns:
            bool: 能否生长到下一 block 状态
        """
        seedName = PlantsCommonManager.GetPlantSeedNameByStage(plantBlockName)
        stageId = PlantsCommonManager.GetPlantStageId(plantBlockName)
        plantTickList = PlantsCommonManager.GetPlantStageTickNum(
            seedName, stageId)
        if tickCount >= plantTickList:
            return True
        return False
