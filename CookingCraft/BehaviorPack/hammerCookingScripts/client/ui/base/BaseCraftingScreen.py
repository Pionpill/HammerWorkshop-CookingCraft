'''
Description: 厨务台界面的 UI，新增以下 UI 控件:
|- main
    |- crafting_panel
        |- material_slot0
        |- material_slot1
        |- ......
        |- result_slot0
        |- arrow_image

Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-03 14:36:13
LastEditTime: 2022-08-03 15:53:54
'''
import mod.client.extraClientApi as clientApi
from hammerCookingScripts.client.ui.base.BaseInventoryScreen import BaseInventoryScreen
from hammerCookingScripts.client.controller import SystemController
from hammerCookingScripts.common import modConfig
from hammerCookingScripts import logger

compFactory = clientApi.GetEngineCompFactory()


class BaseCraftingScreen(BaseInventoryScreen):

    def __init__(self, namespace, name, param):
        BaseInventoryScreen.__init__(self, namespace, name, param)
        self.craftingPanelPath = "/crafting_panel"

    def ShowUI(self, workbenchData):
        # type: (dict) -> None
        """显式 UI 并更新工作台数据"""
        BaseInventoryScreen.ShowInventoryUI(self, workbenchData)
        self.UpdateWorkbenchUI(workbenchData)

    def UpdateWorkbenchUI(self, workbenchData):
        # type: (dict) -> None
        """更新工作台数据"""
        slotItems = workbenchData["workbenchSlotData"]
        for slotName, itemDict in slotItems.items():
            slotPath = "{0}/{1}".format(self.craftingPanelPath, slotName)
            self.slotManager.SetSlotInfo(slotName,
                                         slotInfo=(slotPath, itemDict))
            self._SetSlotUI(slotPath, itemDict)

    def _OnCloseBthTouchUp(self, args):
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
        eventData["pos"] = self.pos
        eventData["dimensionId"] = self.dimensionId
        eventData["playerId"] = clientSystem.GetPlayerId()
        eventData["blockName"] = self.blockName
        clientSystem.NotifyToServer(modConfig.CloseCraftingTableEvent,
                                    eventData)
        # 延迟 0.1s 关闭界面
        gameComp = compFactory.CreateGame(clientApi.GetLevelId())
        gameComp.AddTimer(0.1, self.CloseUI())
