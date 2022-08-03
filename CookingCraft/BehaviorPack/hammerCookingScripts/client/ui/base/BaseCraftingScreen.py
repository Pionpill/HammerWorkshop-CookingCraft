'''
Description: 厨务台界面的 UI，新增以下 UI 控件:
|- main
    |- crafting_panel
        |- crafting_slot0
        |- crafting_slot1
        |- ......
        |- crafting_slot9
        |- arrow_image

Description: your project
version: 1.0
Author: Pionpill
LastEditors: Pionpill
Date: 2022-08-03 14:36:13
LastEditTime: 2022-08-03 15:53:54
'''
from hammerCookingScripts.client.ui.base.BaseInventoryScreen import BaseInventoryScreen
from hammerCookingScripts.client.controller import SystemController
from hammerCookingScripts.common import modConfig


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
