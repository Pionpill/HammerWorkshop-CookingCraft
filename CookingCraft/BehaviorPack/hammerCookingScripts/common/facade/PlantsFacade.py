'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-15 20:48:28
LastEditTime: 2022-07-17 13:54:47
'''
from hammerCookingScripts.common.factory import PlantsFactory
from hammerCookingScripts.common.utils import plantsUtils


class PlantsFacade(object):
    def __init__(self):
        object.__init__(self)

    @classmethod
    def GetPlantProxy(cls, seedName):
        # type: (str) -> PlantsFactory
        return PlantsFactory.GetPlantProxy(seedName)

    @staticmethod
    def GetPlantsUtils():
        # type: () -> plantsUtils
        return plantsUtils
