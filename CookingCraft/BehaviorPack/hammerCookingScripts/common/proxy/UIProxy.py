'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-07-31 14:01:54
LastEditTime: 2022-08-01 13:55:38
'''
from hammerCookingScripts.common.entity import UI


class UIProxy(object):
    def __init__(self):
        object.__init__(self)
        self.ui = UI()

    def GetData(self, blockName):
        # type: (str) -> dict
        """获取 UI 信息字典"""
        return self.ui.GetUIData(blockName)

    def GetName(self, blockName):
        # type: (str) -> dict
        """获取 UI 名称, 如果没有，返回 None"""
        return self.ui.GetName(blockName)

    def GetClassPath(self, blockName):
        return self.ui.GetClassPath(blockName)

    def GetScreenDef(self, blockName):
        return self.ui.GetScreenDef(blockName)

    def GetAllUIBlockName(self):
        # type: () -> list
        """获得所有有 UI 界面的 blockName 列表"""
        return self.ui.GetAllUIBlockName()
