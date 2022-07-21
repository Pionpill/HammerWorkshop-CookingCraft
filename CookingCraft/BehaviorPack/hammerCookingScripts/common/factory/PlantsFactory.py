'''
Description: 植物系统工厂类
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 22:15:04
LastEditTime: 2022-07-19 23:17:39
'''
from hammerCookingScripts.common.proxy import PlantProxy
from hammerCookingScripts.common.entity import Plant


class PlantsFactory(object):
    PlantEntityDict = {}
    PlantProxyDict = {}

    def __init__(self):
        object.__init__(self)

    @classmethod
    def GetPlantProxy(cls, seedName):
        # type: (str) -> PlantProxy
        if not cls.PlantProxyDict.get(seedName, None):
            cls.PlantProxyDict[seedName] = PlantProxy(seedName)
        return cls.PlantProxyDict.get(seedName)
