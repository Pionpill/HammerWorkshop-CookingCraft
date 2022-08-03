'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-23 17:57:59
LastEditTime: 2022-07-31 16:56:39
'''
from hammerCookingScripts.common.factory import WorkbenchFactory
from hammerCookingScripts.common.factory import UIController
from hammerCookingScripts.common.proxy import UIProxy
from hammerCookingScripts.common.proxy.base import BaseFurnaceRecipeProxy


class WorkbenchFacade(object):
    @staticmethod
    def GetWorkbenchProxy(blockName):
        # type: (str) -> BaseFurnaceRecipeProxy
        return WorkbenchFactory.GetWorkbenchProxy(blockName)

    @staticmethod
    def GetUIProxy():
        # type: () -> UIProxy
        return UIController.GetUIProxy()
