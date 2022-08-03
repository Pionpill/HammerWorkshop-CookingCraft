'''
Description: 植物系统工厂类
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-11 22:15:04
LastEditTime: 2022-07-27 15:49:56
'''
from hammerCookingScripts.common.proxy import PlantProxy


class PlantsFactory(object):
    PlantProxyDict = {}

    @classmethod
    def GetPlantProxy(cls, seedName):
        # type: (str) -> PlantProxy
        """获取植物代理类"""
        if not cls.PlantProxyDict.get(seedName, None):
            cls.PlantProxyDict[seedName] = PlantProxy(seedName)
        return cls.PlantProxyDict.get(seedName)
