'''
Description: 基础的植物种植等预定义好的管理类
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:07:47
LastEditTime: 2022-06-01 22:15:48
'''
from abc import abstractmethod
from random import seed
from hammerCookingScripts import logger
from hammerCookingScripts.common.commonConfig.plantsConfig import SEEDS_INFO


class PlantsCommonManager(object):
    seedsInfo = SEEDS_INFO

    @classmethod
    def JudgeBiome(cls, seedName, biomeName):
        """判断生态

        Args:
            seedName (str): 农作物种子名
            biomeName (str): MC 生态名

        Returns:
            bool: 该生态可否种植
        """
        plantBiomeSet = cls.GetSeedBiomeSet(seedName)
        if plantBiomeSet and biomeName in plantBiomeSet:
            return True
        return False

    @classmethod
    def JudgeLand(cls, seedName, landName):
        """判断土地

        Args:
            seedName (str): 农作物种子名
            landName (str): block 名

        Returns:
            bool: 该土地(block)上能否种植
        """
        plantLandList = cls.GetSeedPlantLandList(seedName)
        if landName in plantLandList:
            return True
        return False

    @classmethod
    def GetSeedInfo(cls, seedName):
        """获取种子种植信息

        Args:
            seedName (str): 种子全名

        Returns:
            set: 种子对应的信息
        """
        seedInfo = cls.seedsInfo.get(seedName, None)
        if not seedInfo:
            logger.error("没有注册 {0} 的种植信息".format(seedName))
            return
        return seedInfo

    @classmethod
    def GetSeedBiomeSet(cls, seedName):
        """通过种子名获取生长生态

        Args:
            seedName (str): 种子全称

        Returns:
            set : 可种植的生态集合
        """
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("plantBiome")

    @classmethod
    def GetSeedPlantLandList(cls, seedName):
        """通过种子名获取生长所需土地

        Args:
            seedName (str): 种子全称

        Returns:
            set : 可种植的方块集合
        """
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("plantLandList")

    @classmethod
    def GetPlantStageNum(cls, seedName):
        """通过种子名获取生长植株状态数

        Args:
            seedName (str): 种子全称

        Returns:
            int : 状态数量
        """
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("stageNum")

    @classmethod
    def GetPlantStageTickNum(cls, seedName, stageId):
        """获取农作物对应 stage 下需要 tick 的数量

        Args:
            seedName (str): 种子全称
            stageId (int): 农作物的生长状态

        Returns:
            int: 需要随机 tick 的数量
        """
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("tickList")[stageId]

    @classmethod
    def GetPlantGrowthConditions(cls, seedName):
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("growthConditions")

    @classmethod
    def GetPlantNextStageName(cls, currentBlockName):
        """获取农作物下一阶段 block 名

        Args:
            currentBlockName (str): 现阶段农作物全名

        Returns:
            str: 下一阶段农作物全名
        """
        stageId = int(currentBlockName.split("_")[-1])
        seedName = cls.GetPlantSeedNameByStage(currentBlockName)
        seedStageNum = cls.GetPlantStageNum(seedName)
        if stageId + 1 >= seedStageNum:
            logger.error("{0} stage 超出范围".format(currentBlockName))
            return
        return PlantsCommonManager.GetPlantStageNameBySeed(
            seedName, stageId + 1)

    @staticmethod
    def GetPlantFirstStageName(seedName):
        """根据农作物种子名获取种下时 block 名

        Args:
            seedName (str): 农作物种子全称

        Returns:
            str: 农作物第一阶段 block 名
        """
        plantName = seedName.split("_")[0]
        firstStageName = plantName + "_stage_0"
        return firstStageName

    @staticmethod
    def GetPlantSeedNameByStage(stageBlockName):
        seedName = stageBlockName.split("_")[0] + "_seeds"
        return seedName

    @staticmethod
    def GetPlantStageNameBySeed(seedName, stageId):
        return seedName.split("_")[0] + "_stage_" + str(stageId)

    @staticmethod
    def GetPlantStageId(stageBlockName):
        return int(stageBlockName.split("_")[-1])
