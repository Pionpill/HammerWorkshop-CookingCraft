'''
Description: 基础的植物种植等预定义好的管理类
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-05-31 13:07:47
LastEditTime: 2022-06-04 15:45:27
'''
from abc import abstractmethod
from random import seed
from hammerCookingScripts import logger
from hammerCookingScripts.common.commonConfig.plantsConfig import SEEDS_INFO


class PlantsCommonManager(object):
    seedsInfo = SEEDS_INFO

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
        biomeSet = seedInfo.get("plantConditions").get("plantBiome")
        return biomeSet

    @classmethod
    def GetSeedPlantLandList(cls, seedName):
        """通过种子名获取生长所需土地

        Args:
            seedName (str): 种子全称

        Returns:
            set : 可种植的方块集合
        """
        seedInfo = cls.GetSeedInfo(seedName)
        landList = seedInfo.get("plantConditions").get("plantLandList")
        return landList

    @classmethod
    def GetSeedSpecialPlantCondition(cls, seedName):
        """获取特殊种植需求

        Args:
            seedName (str): 农作物种子全称

        Returns:
            dict: 特殊需求
        """
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("plantConditions").get("special", None)

    @classmethod
    def GetPlantStageCount(cls, seedName):
        """通过种子名获取生长植株状态数

        Args:
            seedName (str): 种子全称

        Returns:
            int : 状态数量
        """
        seedInfo = cls.GetSeedInfo(seedName)
        tickList = seedInfo.get("tickList")
        return len(tickList) + 1

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
    def GetSeedSpecialGrowCondition(cls, seedName):
        """获取特殊生长需求

        Args:
            seedName (str): 农作物种子全称

        Returns:
            dict: 特殊需求
        """
        plantGrowConditions = cls.GetPlantGrowthConditions(seedName)
        return plantGrowConditions.get("special", None)

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
        seedStageCount = cls.GetPlantStageCount(seedName)
        if stageId + 1 >= seedStageCount:
            logger.error("{0} stage 超出范围".format(currentBlockName))
            return
        return PlantsCommonManager.GetPlantStageNameById(seedName, stageId + 1)

    @classmethod
    def GetPlantHarvestCount(cls, seedName):
        seedInfo = cls.GetSeedInfo(seedName)
        return seedInfo.get("harvestCount", None)

    @classmethod
    def GetPlantHarvestStage(cls, seedName):
        seedInfo = cls.GetSeedInfo(seedName)
        harvestStage = seedInfo.get("harvestStage", None)
        return cls.GetPlantStageNameById(harvestStage)

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
        """通过生长时block名获取种子名字

        Args:
            stageBlockName (str): 生长的农作物的block名

        Returns:
            str: seedName
        """
        seedName = stageBlockName.split("_")[0] + "_seeds"
        return seedName

    @staticmethod
    def GetPlantStageNameById(seedName, stageId):
        """通过状态 Id 获取种植时 block 名

        Args:
            seedName (str): 种子全名
            stageId (int): 生长状态 id

        Returns:
            str: 农族欧文生长时的 block 全名
        """
        return seedName.split("_")[0] + "_stage_" + str(stageId)

    @staticmethod
    def GetPlantStageId(stageBlockName):
        return int(stageBlockName.split("_")[-1])
