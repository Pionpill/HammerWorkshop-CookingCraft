'''
Description: 植物系统工厂类
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 22:15:04
LastEditTime: 2022-07-17 00:18:01
'''
from hammerCookingScripts.common.proxy import PlantProxy
from hammerCookingScripts.common.entity import Plant


class PlantsFactory(object):
    PlantEntityDict = {}
    PlantProxyDict = {}

    def __init__(self):
        object.__init__(self)

    @classmethod
    def GetPlantEntity(cls, seedName):
        # type: (str) -> Plant
        """获取 Plant 类，实例存储在字典中"""
        if not cls.PlantEntityDict.get(seedName, None):
            cls.PlantEntityDict[seedName] = Plant(seedName)
        return cls.PlantEntityDict.get(seedName)

    @classmethod
    def GetPlantProxy(cls, seedName):
        # type: (str) -> PlantProxy
        if not cls.PlantProxyDict.get(seedName, None):
            cls.PlantProxyDict[seedName] = PlantProxy(seedName)
        return cls.PlantProxyDict.get(seedName)
