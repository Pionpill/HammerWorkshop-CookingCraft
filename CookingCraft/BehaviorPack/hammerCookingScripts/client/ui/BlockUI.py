'''
Description: BlockUI 方块界面，UI 必须包含以下基本结构
|- main
    |- main_panel
        |- close_button
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-04-14 20:32:05
LastEditTime: 2022-05-27 16:30:14
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts import logger
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.client.clientManager.ClientSystemManager import ClientSystemManager

ScreenNode = clientApi.GetScreenNodeCls()
compFactory = clientApi.GetEngineCompFactory()


class BlockUI(ScreenNode):
    """BlockUI 提供基础的 Block 的 UI 功能，请勿实例化"""
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.mainPanelPath = "/main_panel"
        self.closeBthPath = self.mainPanelPath + "/close_button"
        self.isShow = False
        self.clientSysMgr = ClientSystemManager()

    def Create(self):
        """创建关闭按钮控件
        """
        closeBthUIControl = self.GetBaseUIControl(self.closeBthPath).asButton()
        closeBthUIControl.AddTouchEventParams({"isSallow": True})
        closeBthUIControl.SetButtonTouchUpCallback(self.OnCloseBthClicked)
        self.isShow = True

    def Destroy(self):
        pass

    def OpenUI(self):
        self.ShowBlockUI()

    def CloseUI(self):
        self.SetLayer("", clientApi.GetMinecraftEnum().UiBaseLayer.PopUpLv1)
        self.HideUI()

    def ShowBlockUI(self):
        """显示 UI，并开启血量条等原版 UI
        """
        if self.isShow:
            return
        clientApi.HideHudGUI(True)
        clientApi.SetInputMode(1)
        clientApi.SetResponse(False)
        self.SetScreenVisible(True)
        self.isShow = True

    def HideUI(self):
        """显示 UI，并关闭血量条等原版 UI
        """
        if not self.isShow:
            return
        clientApi.HideHudGUI(False)
        clientApi.SetInputMode(0)
        clientApi.SetResponse(True)
        self.SetScreenVisible(False)
        self.isShow = False

    def OnCloseBthClicked(self, event):
        """关闭按钮点击回调函数，向服务端传递界面关闭事件并关闭UI界面

        Args:
            event (dict): 回调函数事件信息
        """
        clientSystem = self.clientSysMgr.GetModClientSystem(
            modConfig.ClientSystemName_Workbench)
        eventData = clientSystem.CreateEventData()
        eventData["playerId"] = clientSystem.GetPlayerId()
        clientSystem.NotifyToServer(modConfig.CloseInventoryEvent, eventData)
        # 延迟 0.1s 关闭界面
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(0.1, self.CloseUI)
