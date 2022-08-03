# -*- coding:utf-8 -*-
'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 13:49:19
LastEditTime: 2022-08-01 01:05:40
'''
from hammerCookingScripts.common.data.ui import UI_DEFS
from hammerCookingScripts import logger


class UI(object):
    """ui类，提供ui相关的数据信息"""
    def __init__(self):
        # type: (str) -> None
        object.__init__(self)
        self._data = UI_DEFS

    def GetUIData(self, blockName):
        uiData = self._data.get(blockName)
        if not uiData:
            logger.debug("{0} 没有对应的 UI 信息".format(blockName))
            return None
        return uiData

    def GetName(self, blockName):
        return self.GetUIData(blockName).get("name")

    def GetClassPath(self, blockName):
        return self.GetUIData(blockName).get('classPath')

    def GetScreenDef(self, blockName):
        return self.GetUIData(blockName).get('screenDef')

    def GetAllUIBlockName(self):
        return UI_DEFS.keys()
