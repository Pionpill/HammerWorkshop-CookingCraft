'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-01 23:37:32
LastEditTime: 2022-08-02 20:49:44
'''
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from hammerCookingScripts.client.ui.component import CloseButtonUIControl
from hammerCookingScripts.client.ui.manager import SlotManager


class UIFactory(object):
    @staticmethod
    def GetCloseButtonUIControl(blockName, uiPath):
        # type: (str,str) -> ButtonUIControl
        """
        获得一个关闭按钮控制器，按下后:
        1. 向服务器传送对应的界面关闭事件(根据 blockName)
        2. 关闭客户端 UI 界面
        """
        return CloseButtonUIControl.GetCloseButtonUIController(
            blockName, uiPath)

    @staticmethod
    def GetSlotManager():
        return SlotManager()
