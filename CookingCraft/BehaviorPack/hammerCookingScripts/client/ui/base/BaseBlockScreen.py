'''
Description: BlockUI 方块界面，UI 必须包含以下基本结构
|- main
    |- main_panel
        |- close_button
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-14 20:32:05
LastEditTime: 2022-08-03 15:26:09
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.client.factory import UIFactory

ScreenNode = clientApi.GetScreenNodeCls()
compFactory = clientApi.GetEngineCompFactory()


class BaseBlockScreen(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.mainPanelPath = "/main_panel"
        self.closeBthPath = "{0}/close_button".format(self.mainPanelPath)
        self.blockName = None  # 子类赋值
        self.isShow = False

    def Create(self):
        """创建关闭按钮控件"""
        UIFactory.GetCloseButtonUIControl(self.blockName, self.closeBthPath)
        self.SetShowCondition(True)

    def GetShowCondition(self):
        # type: () -> None
        """获取 UI 状态: 是否处于显式状态"""
        return self.isShow

    def SetShowCondition(self, condition):
        # type: (bool) -> None
        """设置 UI 状态: 是否处于显式状态"""
        self.isShow = condition

    def ShowBlockUI(self):
        """显示 UI，并开启血量条等原版 UI"""
        if self.GetShowCondition():
            return
        clientApi.HideHudGUI(True)
        clientApi.SetInputMode(1)
        clientApi.SetResponse(False)
        self.SetScreenVisible(True)
        self.SetShowCondition(True)

    def CloseUI(self):
        self.SetLayer("", clientApi.GetMinecraftEnum().UiBaseLayer.PopUpLv1)

        if not self.GetShowCondition():
            return
        clientApi.HideHudGUI(False)
        clientApi.SetInputMode(0)
        clientApi.SetResponse(True)
        self.SetScreenVisible(False)
        self.SetShowCondition(False)
