'''
Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-01 23:27:30
LastEditTime: 2022-08-03 15:24:33
'''
import mod.client.extraClientApi as clientApi
from mod.client.ui.controls.buttonUIControl import ButtonUIControl
from hammerCookingScripts.client.controller import UIController, SystemController
from hammerCookingScripts.common import modConfig
from hammerCookingScripts.common.utils import workbenchUtils

ScreenNode = clientApi.GetScreenNodeCls()
compFactory = clientApi.GetEngineCompFactory()


class CloseButtonUIControl(object):
    UINode = None
    blockName = None

    @classmethod
    def GetCloseButtonUIController(cls, blockName, uiPath):
        # type: (ScreenNode, str) -> ButtonUIControl
        """获得一个关闭按钮的控制器"""
        cls.blockName = blockName
        cls.UINode = UIController.GetUINode(blockName)
        closeBtnController = ScreenNode.GetBaseUIControl(uiPath).asButton()
        closeBtnController.AddTouchEventParams({"isSallow": True})
        closeBtnController.SetButtonTouchUpCallback(cls.__OnCloseBthTouchUp)
        return closeBtnController

    @classmethod
    def __OnCloseBthTouchUp(cls, args):
        # type: (dict) -> None
        """
        1. 向服务端传递界面关闭事件
        2. 关闭UI界面
        """
        clientSystem = SystemController.GetModClientSystem(
            modConfig.ClientSystemName_Workbench)
        eventData = {"playerId": clientSystem.GetPlayerId()}
        clientSystem.NotifyToServer(modConfig.CloseInventoryEvent, eventData)
        # 如果是工作台需要返回物品
        if workbenchUtils.IsWorkbenchBlock(cls.blockName):
            eventData = clientSystem.CreateEventData()
            eventData["pos"] = cls.UINode.pos
            eventData["dimensionId"] = cls.UINode.dimensionId
            eventData["playerId"] = clientSystem.GetPlayerId()
            eventData["blockName"] = cls.UINode.blockName
            clientSystem.NotifyToServer(modConfig.CloseCraftingTableEvent,
                                        eventData)
        # 延迟 0.1s 关闭界面
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(0.1, cls.UINode.CloseUI())
